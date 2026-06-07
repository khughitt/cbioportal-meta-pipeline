---
id: "question:q037-canonical-neural-gene-dnds-selection"
type: "question"
title: "Do canonical cancer-neuroscience effector genes (NLGN3, ADRB2, NTRK1/2, CHRM3, GRIN2A/B, NGF, BDNF) show positive selection (dN/dS) in any cancer type — the only defensible mutational evidence for active neural hijacking (H1)?"
status: "active"
ontology_terms:
  - dN/dS
  - positive selection
  - cancer neuroscience
  - driver genes
datasets: []
source_refs:
  - "paper:Mancusi2023"
  - "paper:Hanahan2023"
  - "paper:Huang2025"
related:
  - "hypothesis:h12-neural-gene-enrichment-length-histology-artifact"
  - "question:q036-oncofetal-fetal-vs-adult-neural-expression"
  - "topic:cancer-neuroscience-neural-regulation"
created: "2026-06-06"
updated: "2026-06-06"
---

# Do canonical cancer-neuroscience effectors show positive selection (dN/dS) in any cancer type?

## Summary

If neural biology drives cancer through *mutation* (H1-as-selection), the signal should appear
not in long passenger-prone candidate genes but in the field's mechanistic effectors. This
asks whether the canonical set — NLGN3, ADAM10, ADRB1/2/3, CHRM1/3, NTRK1/2/3, GRIN2A/2B,
GRIA, GAD1, NGF, BDNF, NF1 — shows dN/dS>1 / driver-level recurrence in any cancer type,
which would be the only defensible mutational evidence for active neural hijacking.

## Why It Matters

- Flips the analysis from "are long neural-labeled genes enriched" (likely artifact) to "are
  the *mechanistically implicated* genes under selection" (the real H1 test).
- NF1 is an established tumor suppressor (positive control that the dN/dS path works); NTRK1/2/3
  fusions are known oncogenic events.
- A negative result cleanly closes mutational-H1; a localized positive result is a real lead.

## Current Evidence

- The batch establishes these effectors functionally but provides *no* somatic-mutation
  frequency data (`paper:Mancusi2023`, `paper:Hanahan2023`, `paper:Huang2025`).
- Most effectors are receptors/ligands acting via expression, not recurrent point-mutation
  targets — prior expectation is mostly negative except NF1 (loss) and NTRK (fusion).

## Thoughts

- Best current interpretation: expect NF1 (loss) to score; most receptors/ligands not under
  point-mutation selection; therefore mutational-H1 is weak and cancer-type-local at best.
- Major uncertainty: fusions/CNAs (NTRK, etc.) are outside the current SNV/indel pipeline scope.

## Connections to Project

- Related hypotheses: h12 (P5)
- Required data or analyses: run the canonical-effector set through the project's dndscv path
  per cancer type; report q-values; flag NF1 as positive control; note fusion/CNA events as
  out-of-scope but record for follow-up.
- Priority level: P3

## Related

- Topic notes: topic:cancer-neuroscience-neural-regulation
- Article notes: paper:Mancusi2023, paper:Hanahan2023, paper:Huang2025
- Methods/Datasets: run_dndscv.R path; per-cancer-type MAF
