---
type: topic
title: Mutational signatures (COSMIC SBS/DBS/ID)
status: active
created: '2026-04-13'
updated: '2026-04-13'
id: topic:mutational-signatures
ontology_terms: []
source_refs: []
related:
- paper:Alexandrov2020
- paper:Tate2019
- paper:PCAWG2020
- paper:Zehir2017
---

# Mutational signatures (COSMIC SBS/DBS/ID)

## Summary

Decomposition of tumor mutation spectra into reproducible signatures (COSMIC v3: 67 SBS, 11
DBS, 17 ID) that reflect underlying mutational processes (aging, smoking, UV, APOBEC, MMR/HRD
deficiency, chemotherapy). Out-of-scope for the current pipeline but a natural future axis
beyond gene-level frequencies. **Critical caveat**: full SigProfiler decomposition needs WES/WGS
power; panel data needs SigMA or coarse "dominant signature" tags only.

## Key Concepts

- **96 trinucleotide-context SBS framework** (Alexandrov et al.
  [@Alexandrov2013Nature; @Alexandrov2020]). Tumor mutations classified by base-substitution +
  5'/3' flanking context; NMF factorizes the sample × context matrix into signature × per-sample
  exposures.
- **DBS and ID extensions** (new in v3): doublet-base substitutions and small indel patterns,
  capturing mechanisms invisible to SBS-only (e.g., NHEJ-mediated microhomology deletions, ID6).
- **Validated etiologies**: SBS1 (5mC-deamination/aging), SBS4 (smoking), SBS7a-d (UV),
  SBS2/SBS13 (APOBEC), SBS6/15/20/26 (MMR deficiency), SBS3 (HRD), SBS10a/b (POLE), several
  chemotherapy signatures (platinum, temozolomide, 5-FU). Roughly half of v3 SBS signatures
  remain idiopathic.
- **Per-cancer signature exposures** are tabulated in Alexandrov et al. [@Alexandrov2020] —
  UV-dominant in melanoma, smoking-dominant in lung adenocarcinoma, APOBEC across
  bladder/cervical/breast.

## Current State of Knowledge

- **SigProfiler (Python, official)** is canonical for *de novo* signature extraction. Heavyweight,
  WGS-friendly.
- **SigProfilerAssignment / deconstructSigs / sigfit / MutationalPatterns** for *refit* against
  the v3 reference catalog. Lighter-weight, WES-friendly.
- **SigMA** (Gulhan et al. 2019) is purpose-built for low-mutation-count panel data.
- Zehir et al. [@Zehir2017]: panel-derived signature attribution worked at MSK-IMPACT scale for
  high-prevalence signatures (UV, smoking, MMR, POLE, temozolomide) by restricting to the
  highest-TMB tail.
  Caveat-laden.

## Controversies & Open Questions

- **Method discordance.** SigProfiler vs SignatureAnalyzer disagree on hypermutator decomposition
  (13 vs 25 SBS signatures); illustrates residual subjectivity in NMF rank selection.
- **Panel feasibility.** Panel data typically yields tens of mutations per sample vs the
  thousands needed for stable trinucleotide spectra. Realistic scope: a handful of dominant
  signatures (UV, smoking, MMR/MSI, APOBEC, HRD) with explicit confidence flags.
- **Artifact contamination.** Sequencing/calling differences themselves generate spurious
  signatures; curation against artifacts is manual and version-dependent.

## Relevance to This Project

Out-of-scope for current pipeline. If/when added, the realistic scope is:
1. **For WES studies in our cohort (TCGA portion via MC3)**: per-sample exposures via
   SigProfilerAssignment or MutationalPatterns; per-cancer-type dominant-signature tags.
2. **For panel studies (MSK-IMPACT, GENIE)**: per-cancer "dominant signature class" via SigMA
   for high-prevalence signatures only (APOBEC / MMR / UV / smoking flags). Skip per-sample
   attribution.
3. Add a `dominant_signature` cancer-type-level annotation to our metadata; explicit
   panel-vs-WES flag; never report panel-derived signature percentages without that flag.

See `task:t024` (retired) and `task:t021` (this topic). The follow-up search `task:t024` was retired
in favor of directly reading Alexandrov et al. [@Alexandrov2020] and Tate et al. [@Tate2019] (done).

## Key References

- Alexandrov et al. [@Alexandrov2020] (COSMIC v3 catalog)
- Tate et al. [@Tate2019] (COSMIC v86 — note: signatures in v86 are pre-v3)
- PCAWG Consortium [@PCAWG2020] (WGS pan-cancer signature landscape)
- Zehir et al. [@Zehir2017] (panel-data attribution feasibility example)
