---
type: question
title: Does the GLI1 exon 12 normal-tissue recurrent hotspot inflate GLI1 mutation
  frequencies in our cBioPortal cancer outputs?
status: active
created: '2026-04-18'
updated: '2026-06-28'
id: question:0005-gli1-normal-tissue-hotspot-inflation
ontology_terms: []
datasets: []
source_refs:
- paper:Xu2025
related:
- topic:pan-cancer-mutation-landscape
- topic:mutation-rate-normalization
- paper:Xu2025
- paper:Yoshida2026
---

# Does the GLI1 exon 12 normal-tissue recurrent hotspot inflate GLI1 mutation frequencies in our cBioPortal cancer outputs?

## Summary

Xu et al. 2025 identified a statistically significant recurrent somatic mutation cluster in GLI1 exon 12 across 4 unrelated individuals, spanning sun-exposed skin, non-sun-exposed skin, prostate, and testis — all phenotypically normal. GLI1 is a Hedgehog pathway effector and established oncogene in basal cell carcinoma, medulloblastoma, and pancreatic cancer. If GLI1 exon 12 carries a systematic normal-tissue mutation hotspot that survives into bulk tumor sequencing, it could inflate GLI1 mutation rates in our cross-study frequency tables beyond what is attributable to tumor driver selection.

## Why It Matters

- If GLI1 exon 12 mutations are elevated in our pipeline's cancer gene frequency tables partly due to normal-tissue background signal, GLI1's apparent recurrence across cancer types would be artifactual.
- The hotspot spans multiple tissues (skin, prostate, testis) — meaning it could bleed into melanoma, prostate cancer, and testicular cancer cohorts simultaneously, creating a spurious cross-cancer signal.
- This is distinct from the NOTCH1 esophageal case (`question:0001-normal-epithelial-clone-contamination-in-esophageal-studies`) because GLI1 is a recognized oncogene whose normal-tissue hotspot has not been widely reported; it could be systematically overlooked in driver-gene annotation.

## Current Evidence

- Xu et al. 2025: 4 missense mutations at GLI1 exon 12 in 4 unrelated donors from sun-exposed skin, non-sun-exposed skin, prostate, and testis (statistically significant cluster, p < 10^-8 per their caller).
- GLI1 is in the cancer driver gene compendium from [@Bailey2018] and COSMIC Cancer Gene Census.
- No cBioPortal-level analysis of GLI1 exon 12 mutation hotspot vs. background rate has been done in this pipeline.

## Thoughts

- A first check: compare GLI1 mutation rates across cBioPortal cancer types and identify whether the exon 12 region is overrepresented relative to other GLI1 exons.
- If the hotspot is in exon 12, the protein-level location and predicted functional consequence should be examined — are these likely activating or loss-of-function variants? (If they are synonymous or functionally neutral hotspots in normal tissue, they are less likely to confound driver inference.)
- The Xu et al. study detected these in normal tissue at low VAF (median 2.3%) — they would be captured in cancer studies at higher VAF if clonally expanded in the tumor; they would be below detection if they are low-VAF background contamination in bulk tumor samples.

## Connections to Project

- Related hypotheses: none yet filed.
- Required data or analyses: GLI1 exon 12 mutation counts in current pipeline outputs; comparison to GLI1 overall counts; protein domain annotation of exon 12 missense mutations.
- Priority level: low-medium — GLI1 is not a top-ranked gene in our current outputs, but the principle of recurrent normal-tissue hotspots as background noise is broadly applicable.

## Related

- Topic notes: `topic:pan-cancer-mutation-landscape`, `topic:mutation-rate-normalization`
- Article notes: `paper:Xu2025`, `paper:Yoshida2026`, `paper:Bailey2018`
- Methods/Datasets: cBioPortal mutation data for skin, prostate, testicular cancer cohorts; COSMIC Cancer Gene Census GLI1 entry
