# MoL-Full source provenance and redistribution evidence

Snapshot date: 2026-07-28. Machine-readable fields and immutable evidence URLs
are in `mol_full_sources.yaml`; every release copies them, together with input
hashes, to `source_records.jsonl`.

| Source | Frozen upstream evidence | License evidence | Database redistribution decision |
|---|---|---|---|
| Spider | Spider 1.0 dev snapshot; official `taoyds/spider` repository | Apache-2.0 `LICENSE` at commit `b7b5b8c890cd30e35427348bb9eb8c6d1350ca7c` | **Yes, with attribution.** Preserve Spider attribution and any notices attached to contributed databases. |
| BIRD | Official Mini-Dev SQLite 500-example package, dated 2024-06-27; repository commit `b3d4bcbbae9a96934ad812551eb400c7a3b23c12` | Official README declares CC-BY-SA-4.0 | **Yes, with attribution and ShareAlike.** The adapted database release must retain the same terms. |
| BULL / FinSQL | FinSQL repository commit `5753259b62fd734e8a0dfd0ed990b7aae48d9540`; `BULL.zip` SHA-256 `103ef58e68bd22fc5c64b44c6f1594fc59a0d4ac809714bb42c5c92e9eacbcd1` | No license declaration was found in the official repository or download page | **No direct redistribution at present.** Keep `redistribution_policy: unresolved`; distribute only code, hashes, lineage, and reconstruction instructions until written permission or license evidence is obtained. |
| EHRSQL | EHRSQL v1.5.1, commit `01241a3c55bda895561c76923251ea2421d2e892` | CC-BY-4.0 `LICENSE` in the official repository | **Yes, with attribution.** Retain EHRSQL attribution, the de-identification/shuffling statement, intended-use notice, and cited MIMIC-III/eICU provenance. |
| KaggleDBQA | Official repository commit `ab6325c9b5749f2f3509a1f64299bfa30396e6b0` | CC-BY-SA-4.0 `LICENSE.md` | **Yes, with attribution and ShareAlike.** Preserve the Census Bureau non-endorsement notice. |

## Release consequence

The five-source aligned dataset can be built and audited internally, but a
single archive containing all five database families must not be publicly
redistributed while BULL remains unresolved. A public artifact may contain the
four cleared families and a BULL fetch/reconstruction manifest, or BULL may be
excluded from the redistributable package. This licensing decision is
independent of execution correctness.

This file records evidence, not legal advice. If an upstream source changes its
terms, freeze the cited snapshot and re-review before publishing a new release.
