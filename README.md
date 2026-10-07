# CultureTechLens Index

**CULTURETECHLENS** · "Culture, Clearly Seen." · Black Cultural Intelligence

> 🌐 **Website:** [culturetechlens.com](https://culturetechlens.com) · 💛 **Donate:** [culturetechlens.com/donate](https://culturetechlens.com/donate/) · ✉️ **Contact:** [culturetechlens.com/contact](https://culturetechlens.com/contact/)

A monthly, data-driven ranking of cultural figures, moments, artifacts, and places — the **CTL 10** — published by CultureTechLens as a citable source for journalists, researchers, and the community.

Rankings describe the data. They do not crown winners.

## Current edition

**Edition 2026-10: Artifacts** — the ten everyday artifacts most resonant in the combined record of public attention and CTL's verified research. Read it: [`editions/2026-10/EDITION.md`](editions/2026-10/EDITION.md)

## How it works

Each edition scores 10 candidates on three signals — no hand-tuned scores:

| Signal | Weight | Source |
|---|---|---|
| Public attention | 40% | Trailing-30-day English Wikipedia pageviews, log-normalized |
| Evidence depth | 40% | CTL research-corpus claim grades, relationship counts, biography bonus |
| Momentum | 20% | Pageview trend vs. prior 30 days |

Full methodology: [`CTL-IDX-001-methodology.md`](CTL-IDX-001-methodology.md)

## Reproduce it

```bash
python3 ctl-index.py edition-2026-10-candidates.json \
  --edition 2026-10 \
  --out ./editions/2026-10/ \
  --evidence-json ./edition-2026-10-evidence.json
```

Every edition ships its candidates, evidence table, ranked table, and per-signal CSV.

## Cite it

CultureTechLens, "CultureTechLens Index, Edition 2026-10: Artifacts (CTL-IDX-003)," 2026-09-28.

## License

Content: CC BY 4.0 — see [LICENSE](LICENSE). Code: MIT — see [LICENSE-CODE](LICENSE-CODE).
