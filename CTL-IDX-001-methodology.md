# CTL-IDX-001 — The CultureTechLens Index: Methodology

**CULTURETECHLENS** · "Culture, Clearly Seen." · Black Cultural Intelligence
Program spec v1.1 — 2026-09-28. Status: METHODOLOGY FINALIZED; Edition 2026-10 published.

*Cite as: CultureTechLens, "The CultureTechLens Index: Methodology (CTL-IDX-001)," 2026-09-28.*

---

## 1. What it is

A monthly, data-driven ranking of cultural figures, moments, artifacts, or places
drawn from Black Chicago's cultural record — published by CultureTechLens NFP as a
citable public source. Each edition ranks one category per month on a transparent,
reproducible 0–100 score.

The Index measures **cultural resonance** — how present a subject is in the
documented record and in current public attention — not worth, greatness, or
moral standing. Rankings describe the data. They do not crown winners.

## 2. Cadence and rotation

- Published monthly, on the first Tuesday of each month.
- One category per edition, rotating: **Figures → Moments → Artifacts → Places → repeat.**
- Each edition ranks exactly **10 subjects** (the "CTL 10").
- Special editions (anniversary months, e.g., Black History Month) permitted; methodology unchanged.

## 3. Scoring model (v1)

**Index Score (0–100)** = weighted composite of three signals:

| Signal | Weight | Source | What it measures |
|---|---|---|---|
| Public attention | 40% | Wikipedia pageviews API, trailing 30 days, log-normalized across the candidate set | How much the public is looking this subject up right now |
| Evidence depth | 40% | The edition's source research package (named in each edition; CTL-KG-CORE-001 once package ingestion is complete): verified + provisional claim counts, verified relationship counts, and full-biography bonus, normalized across the candidate set | How deeply CTL's own research corpus documents the subject |
| Momentum | 20% | Wikipedia pageviews, trailing 30 days vs. prior 30 days | Whether attention is rising or fading |

- Scores rounded to one decimal. Ties broken by evidence depth, then alphabetical.
- Every edition publishes the full signal breakdown per subject — never just the rank.
- Candidate pool: subjects drawn from CTL's verified research corpus (flagship packages, knowledge graph). No subject enters the ranking that CTL has not independently documented.
- Recomputation is scripted (`ctl-index.py`); no hand-tuned scores, ever.

## 4. What the Index does NOT do

- It does not rank living people by "importance" or "greatness." Figure editions are framed as **most documented / most referenced**, and the copy says so explicitly.
- It does not present rank as value. Edition copy uses "highest-scoring in this month's set," never "most important."
- It does not use superlatives the data cannot support ("world's leading," "definitive").
- It does not change methodology mid-year. Annual methodology review each January; changes versioned (v1, v2…).

## 5. Citability standard

Every edition ships with:
- A stable URL (`culturetechlens.com/index/YYYY-MM`; Beehiiv mirror until the site is live).
- A suggested citation string.
- A downloadable CSV of the full scored table (all 10 subjects, all signals).
- A link to this methodology document.
- A version date and a public corrections log.

## 6. Monthly production workflow

1. **Candidate selection** (founder + research lead): 12–15 candidates from the CTL corpus for the month's category.
2. **Data pull** (scripted): pageviews + KG evidence depth → scored table.
3. **Editorial pass**: one-line "why it moved" for each subject; trend arrows vs. prior edition (same category).
4. **Rights review**: imagery only where rights-cleared; Object Biographies and diagrams preferred.
5. **Publish**: site + Beehiiv, first Tuesday of the month, 6:00 AM CT.
6. **Pitch**: embargoed media outreach 3 days prior (see CTL-IDX-002).
7. **Measure**: track citations, pickups, and inbound links; iterate.

## 7. Limitations (published with every edition)

- Wikipedia pageviews skew toward subjects with English Wikipedia articles and internet-era attention.
- CTL's corpus skews toward what CTL has researched so far; under-documented subjects score lower on evidence depth by construction.
- The Index reflects resonance in the record, not community sentiment on the ground.
- Monthly recomputation means ranks move; movement is signal, not verdict.

## 8. Branding

Every edition carries the CULTURETECHLENS wordmark, "Culture, Clearly Seen.,"
"Black Cultural Intelligence," and the black / deep red / gold identity.

---

## Change log

- 2026-09-28 — v1.0 methodology finalized. Pipeline scripted. Edition 001 topic pending founder decision.
- 2026-09-28 — v1.1: evidence-depth source clarified. Until research packages are ingested into CTL-KG-CORE-001, evidence depth is computed from the edition's named source research package (same formula family: claim grades + relationship counts + biography bonus). The source package is always named in the edition. No scores change hands — only the corpus address.
