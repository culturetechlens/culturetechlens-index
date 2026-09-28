#!/usr/bin/env python3
"""
ctl-index.py — CultureTechLens Index scoring pipeline (v1).

Computes the monthly CTL 10 ranking from:
  - Public attention (40%): trailing-30d Wikipedia pageviews, log-normalized
  - Evidence depth  (40%): CTL knowledge-graph documentation, normalized
  - Momentum        (20%): pageview trend, trailing 30d vs prior 30d

Usage:
    python3 ctl-index.py candidates.json --edition 2026-10 --out ./edition-2026-10/

candidates.json format:
    [{"name": "Muddy Waters", "wiki": "Muddy_Waters", "category": "Figures"}, ...]

Outputs: RANKED.md (edition table) and index-scores.csv (full signal breakdown).
Methodology: CTL-IDX-001. No hand-tuned scores — every number is computed.
"""

import csv
import json
import math
import os
import sys
import urllib.parse
import urllib.request
from datetime import date, timedelta

KG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "..", "..", "knowledge-graph")
UA = {"User-Agent": "CultureTechLens-Index/1.0 (research pipeline; contact: culturetechlens@gmail.com)"}


def load_kg():
    with open(os.path.join(KG_DIR, "entities.json")) as f:
        entities = json.load(f)
    with open(os.path.join(KG_DIR, "relationships.json")) as f:
        rels = json.load(f)
    return entities, rels


def load_evidence_json(path):
    """Edition-specific evidence table: {candidate_name: raw_score}.

    Used when the edition's subjects live in a source research package that has
    not yet been ingested into the master knowledge graph. The table is built
    by a transparent, auditable script and stored with the edition.
    """
    with open(path) as f:
        return json.load(f)


def find_entity(entities, name):
    """Match a candidate name against KG entity names and aliases (case-insensitive)."""
    target = name.strip().lower()
    for e in entities:
        names = [e.get("name", "")] + list(e.get("aliases", []) or [])
        if any((n or "").strip().lower() == target for n in names):
            return e
    return None


def evidence_depth(entity, rels):
    """Raw evidence-depth score from the CTL knowledge graph."""
    if entity is None:
        return 0.0, {"verified_rels": 0, "projects": 0, "verified": False}
    eid = entity["id"]
    verified_rels = sum(
        1 for r in rels
        if r.get("verification") == "Verified"
        and (r.get("from") == eid or r.get("to") == eid)
    )
    projects = len(entity.get("project_ids", []) or [])
    verified = entity.get("verification") == "Verified"
    raw = verified_rels * 2.0 + projects * 3.0 + (5.0 if verified else 0.0)
    return raw, {"verified_rels": verified_rels, "projects": projects, "verified": verified}


def pageviews(article, start, end):
    """Daily pageviews summed over [start, end] via the Wikimedia REST API."""
    title = urllib.parse.quote(article.replace(" ", "_"), safe="")
    url = (f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
           f"en.wikipedia/all-access/user/{title}/daily/{start}/{end}")
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.load(resp)
    except Exception as exc:  # API failure -> treat as zero, never crash the run
        print(f"  [warn] pageviews failed for {article}: {exc}", file=sys.stderr)
        return 0
    return sum(item.get("views", 0) for item in data.get("items", []))


def normalize(values):
    """Min-max normalize a list to 0..100. Constant input -> all 50."""
    lo, hi = min(values), max(values)
    if hi == lo:
        return [50.0] * len(values)
    return [100.0 * (v - lo) / (hi - lo) for v in values]


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cand_path = sys.argv[1]
    edition = "PILOT"
    outdir = "."
    evidence_path = None
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == "--edition" and i + 1 < len(args):
            edition = args[i + 1]
        if a == "--out" and i + 1 < len(args):
            outdir = args[i + 1]
        if a == "--evidence-json" and i + 1 < len(args):
            evidence_path = args[i + 1]

    with open(cand_path) as f:
        candidates = json.load(f)
    entities, rels = load_kg()
    evidence_table = load_evidence_json(evidence_path) if evidence_path else None
    if evidence_table:
        print(f"  Using edition evidence table: {evidence_path}")

    today = date.today()
    recent_end = (today - timedelta(days=1)).strftime("%Y%m%d")
    recent_start = (today - timedelta(days=31)).strftime("%Y%m%d")
    prior_end = (today - timedelta(days=31)).strftime("%Y%m%d")
    prior_start = (today - timedelta(days=61)).strftime("%Y%m%d")

    rows = []
    print(f"Scoring {len(candidates)} candidates for edition {edition}...")
    for c in candidates:
        name, wiki = c["name"], c["wiki"]
        print(f"  {name} ...")
        recent = pageviews(wiki, recent_start, recent_end)
        prior = pageviews(wiki, prior_start, prior_end)
        if evidence_table is not None:
            raw_ev = float(evidence_table.get(name, {}).get("raw", 0.0))
            ev_detail = evidence_table.get(name, {}).get("detail", {})
            in_kg = ev_detail.get("in_source_package", False)
        else:
            ent = find_entity(entities, name)
            raw_ev, ev_detail = evidence_depth(ent, rels)
            in_kg = ent is not None
        momentum_raw = (recent - prior) / (prior + 1.0)
        rows.append({
            "name": name, "category": c.get("category", ""),
            "wiki": wiki, "in_evidence": in_kg,
            "pv_recent": recent, "pv_prior": prior,
            "attn_raw": math.log10(1 + recent),
            "ev_raw": raw_ev,
            "mom_raw": max(-1.0, min(1.0, momentum_raw)),
            "ev_detail": ev_detail,
        })

    attn = normalize([r["attn_raw"] for r in rows])
    ev = normalize([r["ev_raw"] for r in rows])
    mom = [(r["mom_raw"] + 1.0) / 2.0 * 100.0 for r in rows]  # -1..1 -> 0..100, 50 = flat

    for r, a, e, m in zip(rows, attn, ev, mom):
        r["attention"] = round(a, 1)
        r["evidence"] = round(e, 1)
        r["momentum"] = round(m, 1)
        r["score"] = round(0.4 * a + 0.4 * e + 0.2 * m, 1)

    rows.sort(key=lambda r: (-r["score"], -r["evidence"], r["name"]))

    os.makedirs(outdir, exist_ok=True)
    md_path = os.path.join(outdir, "RANKED.md")
    csv_path = os.path.join(outdir, "index-scores.csv")

    with open(md_path, "w") as f:
        f.write(f"# CultureTechLens Index — Edition {edition}\n\n")
        f.write("**CULTURETECHLENS** · \"Culture, Clearly Seen.\" · Black Cultural Intelligence\n\n")
        f.write("Methodology: CTL-IDX-001. Scores recomputed monthly; ranks describe the data, they do not crown winners.\n\n")
        f.write("| Rank | Subject | Score | Attention (40%) | Evidence (40%) | Momentum (20%) |\n")
        f.write("|---|---|---|---|---|---|\n")
        for i, r in enumerate(rows, 1):
            f.write(f"| {i} | {r['name']} | {r['score']} | {r['attention']} | {r['evidence']} | {r['momentum']} |\n")

    with open(csv_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["edition", "rank", "name", "category", "in_evidence_source", "score",
                    "attention_40", "evidence_40", "momentum_20",
                    "pageviews_30d", "pageviews_prior_30d", "evidence_detail_json"])
        for i, r in enumerate(rows, 1):
            w.writerow([edition, i, r["name"], r["category"], r["in_evidence"], r["score"],
                        r["attention"], r["evidence"], r["momentum"],
                        r["pv_recent"], r["pv_prior"],
                        json.dumps(r["ev_detail"], sort_keys=True)])

    print(f"\nWrote {md_path} and {csv_path}")
    for i, r in enumerate(rows, 1):
        print(f"  {i}. {r['name']}: {r['score']}")


if __name__ == "__main__":
    main()
