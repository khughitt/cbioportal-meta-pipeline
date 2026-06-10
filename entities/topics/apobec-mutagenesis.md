---
type: topic
title: APOBEC mutagenesis and SBS2/SBS13
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: topic:apobec-mutagenesis
ontology_terms:
- APOBEC3A
- APOBEC3B
- SBS2
- SBS13
- mutational signatures
- cytosine deamination
- kataegis
- omikli
- mismatch repair
- ssDNA
- trinucleotide context
- YTCW
- RTCW
source_refs:
- paper:Carpenter2023
- paper:MasPonte2020
related:
- paper:Carpenter2023
- paper:MasPonte2020
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
---

# APOBEC mutagenesis and SBS2/SBS13

## Summary

APOBEC3A (A3A) and APOBEC3B (A3B) are cytidine deaminases that convert cytosine to uracil in
single-stranded DNA (ssDNA), producing the canonical SBS2 (C→T in TCW) and SBS13 (C→G in TCW)
COSMIC signatures. These two signatures together define the "APOBEC3 signature" and are among
the most prevalent endogenous mutational processes in human cancers, with high activity in
bladder, breast, cervical, lung, and head-and-neck squamous tumors. APOBEC mutagenesis serves
as a positive-control arm in
hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and: an agnostic
within-tissue covariate-to-signature-exposure association
must recover APOBEC3A/B mRNA expression as the top predictor of SBS2/SBS13 burden to be
considered validated.

---

## Key Concepts

**SBS2 and SBS13 as a composite.** The 96-trinucleotide COSMIC catalogue reports SBS2 (dominated
by C→T transitions at TCA and TCT contexts) and SBS13 (dominated by C→G transversions at the
same contexts) as separable components. Both arise from cytosine deamination by APOBEC3
enzymes acting on ssDNA; the C→T vs C→G ratio reflects downstream repair choice after uracil
insertion. Both signatures co-occur in APOBEC-active tumors.

**A3A vs A3B sub-signature resolution.** paper:Carpenter2023 demonstrates that A3A and A3B
generate SBS2/SBS13 with distinct tetranucleotide context biases: A3A strongly prefers YTCW
motifs (~72% of TC-context mutations), while A3B shows only weak YTCW preference (~47%) and
a corresponding enrichment for RTCW. Primary breast tumors cluster in an intermediate range
(50–70% YTCW), consistent with combinatorial contributions from both paralogs. This means the
composite COSMIC SBS2+SBS13 attribution is itself a mixture of at least two enzymatic sources.

**Omikli vs kataegis — two mechanistically distinct APOBEC cluster modes.** paper:MasPonte2020
formally distinguishes two types of APOBEC3 mutation clusters detectable in WGS data:

- *Omikli* (2–4 mutations per cluster, mean 2.2): diffuse, non-recurrent, genome-wide.
  Enriched in early-replicating, H3K36me3-marked (gene-rich) chromatin. Dependent on intact
  MMR activity; depleted 5.5-fold in MSI (MMR-deficient) tumors. IMD distribution matches
  ~800 nt ssDNA tracts — the length of MMR excision intermediates in vitro. Driven
  preferentially by A3A (YTCA-context enrichment).
- *Kataegis* (≥5 mutations per cluster, mean 7.1): focal, high-density showers. Associated
  with DSB repair (resection-generated ssDNA) rather than MMR. Relatively enriched for A3B-
  like RTCA context.

Omikli accounts for ~66% of all TCW>K mutations pan-cancer; kataegis accounts for effectively
zero of unclustered TCW>K mutations, and the ~32% remainder (A3-X) is attributed to BER-
processed lesions or replication-origin-proximal events.

**MMR promotes A3 omikli — a counterintuitive coupling.** The key insight from paper:MasPonte2020
is that functional MMR is required for omikli: repair of replication errors generates ssDNA
excision tracts that are then targeted by A3 enzymes before re-synthesis. MSI (MMR-deficient)
tumors paradoxically show *less* omikli despite their globally elevated mutation burden. The
implication for covariate analysis is that higher MMR gene expression (MSH2, MSH6, EXO1) should
associate *positively* with SBS2/13 burden within MMR-proficient tumor populations — opposite to
intuition.

**Functional impact of APOBEC3 mutagenesis.** A3 omikli is disproportionately enriched in
early-replicating, gene-dense chromatin due to its MMR dependency. This gives APOBEC3 mutations
the highest functional impact density (FID) of all major mutational processes: ~0.47 oncogenic
mutations per thousand (OMPK) vs 0.24 for tobacco (SBS4) and 0.19 for UV (SBS7). The mechanism
is not positive selection but spatial enrichment in coding sequence. Chromatin modifier and tumor
suppressor genes (KMT2A/C/D, SETD2, ARID2, PBRM1, NCOR1) are disproportionately affected.

---

## Current State of Knowledge

**What is settled:**

- A3A and A3B are the principal enzymatic sources of SBS2 and SBS13 in human cancer; A3H
  paralogs (haplotype I and II) do not generate detectable APOBEC3 signature mutations in
  controlled cell-line experiments (paper:Carpenter2023).
- Both paralogs produce genome-wide SBS2/13 mutations and kataegis in human cell lines, but
  A3A generates ~4-fold more events per unit time in the HAP1-TK-M9 system, partially because
  the experimental construct drives A3A ~5-fold above physiological breast tumor levels.
- Omikli is the dominant mode of APOBEC3 mutagenesis pan-cancer, accounting for ~66% of all
  TCW>K somatic mutations in TCGA WGS; kataegis is prevalent but contributes a small fraction
  of unclustered background (paper:MasPonte2020).
- MMR activity is mechanistically required for omikli: functional MMR generates ssDNA
  excision intermediates that provide APOBEC3 substrate; MSI tumors have ~5.5-fold lower
  omikli fractions despite elevated TMB (paper:MasPonte2020).
- A3A activity is associatively linked to omikli (YTCA context) and A3B to kataegis (RTCA
  context), corroborating the cell-line tetranucleotide findings (paper:Carpenter2023) with
  observational tumor data (paper:MasPonte2020).

**What is contested or uncertain:**

- **The relative in vivo contribution of A3A vs A3B.** Cell-line experiments (paper:Carpenter2023)
  establish that A3A at physiological levels is a weaker per-event contributor than the
  experimental ~5× overexpression suggests, and that A3B expression in cell lines better
  approximates tumor levels. Whether A3A or A3B dominates in any given cancer type is not
  directly resolved from WGS context analysis alone — the YTCW/RTCW distinction is associative.
- **The identity of A3-X (~32% of unclustered TCW>K mutations).** These events are not
  explained by omikli or kataegis mechanisms. Replication-origin-proximal events, BER
  intermediates, and lagging-strand synthesis errors are all candidate contributors, but have
  not been discriminated (paper:MasPonte2020).
- **Episodic vs continuous APOBEC3 activity.** Evidence from longitudinal tumor sequencing
  suggests APOBEC3 mutagenesis may be burst-like (episodic) rather than continuously active
  throughout tumor evolution [UNVERIFIED — not covered by the two papers in this topic; see
  Petljak et al. 2022]. If episodic, study-level mutation frequencies capture a snapshot that
  inflates cross-study variance independent of mean expression level.
- **Generalizability of the YTCW/RTCW sub-signature distinction beyond breast cancer.**
  paper:Carpenter2023 validates this fractionation in ICGC breast WGS; applicability to
  bladder, cervical, lung, and HNSC tumors is inferred but not directly established in that
  study.
- **A3H's contribution.** A3H remains incompletely ruled out as a minor contributor across all
  cancer types; the HAP1-TK-M9 system carries an unstable A3H haplotype that limits this test
  (paper:Carpenter2023).

---

## Controversies & Open Questions

1. **Single-predictor vs joint A3A/A3B association model.** If A3A and A3B generate the same
   composite SBS2/SBS13 signature, any single-gene mRNA expression test (A3A alone or A3B alone)
   may be underpowered, while a joint score or principal component of A3A+A3B expression should
   be a stronger predictor. The best predictor variable for an agnostic scan has not been
   established.

2. **How to decompose SBS2 vs SBS13 into A3A/A3B contributions in panel-sequencing data.** The
   YTCW/RTCW pentanucleotide fractionation that distinguishes A3A from A3B requires WGS-scale
   mutation counts per sample; panel-sequenced samples (the majority of cBioPortal studies) lack
   the resolution. This limits sub-signature attribution in the cross-study pipeline.

3. **MMR↔APOBEC coupling in cross-study analysis.** MSI status is available as a clinical
   variable for many cBioPortal samples. Whether an agnostic association scan picks up MMR gene
   expression as a positive (counter-intuitive) covariate for SBS2/13 in MSS-restricted subsets —
   as predicted by paper:MasPonte2020 — is an open empirical question with interpretive value.

4. **Coding-region inflation of A3 signal in WES/panel data.** Because omikli is enriched in
   early-replicating, gene-dense chromatin (paper:MasPonte2020), WES and panel data systematically
   oversample the A3 omikli mutation pool relative to WGS, inflating apparent per-sample A3
   mutation burden in the cBioPortal pipeline. The magnitude of this inflation across cancer types
   has not been directly quantified for panel-based cohorts [SPECULATION — extrapolated from WGS
   FID enrichment data].

---

## Implications for h08 and the cross-study signature-aetiology aggregation

**Positive control expectation.** An agnostic within-tissue mRNA covariate scan for SBS2/SBS13
exposure must recover APOBEC3A and/or APOBEC3B mRNA as the top-ranked covariates within
APOBEC-active cancer types (bladder, breast, cervical, lung, HNSC). Failure to do so would
falsify H08a for the APOBEC arm, indicating either: (a) the covariate feature space lacks A3A/B
expression, (b) within-study expression variance is insufficient, or (c) sample-count-limited
signature decomposition introduces too much noise. Both papers (paper:MasPonte2020 reporting
Spearman rho ~0.31–0.45 for A3A/B expression vs omikli burden, and paper:Carpenter2023
providing mechanistic causal warrant) justify expecting this as a recoverable signal given
adequate sample size.

**Joint A3A+A3B expression score.** Because A3A and A3B both contribute to SBS2/SBS13 with
different context biases and possibly different mechanistic weights per cancer type
(paper:Carpenter2023), H08's association model should test A3A and A3B jointly — either as a
combined expression score or as parallel predictors — rather than relying on either paralog
alone. A3A-alone tests may be underpowered in cancers where A3B dominates, and vice versa.

**Counterintuitive MMR covariate.** The h08 agnostic scan should be prepared to encounter MMR
pathway genes (MSH2, MSH6, EXO1) positively associated with SBS2/13 burden in MSS-restricted
analyses (paper:MasPonte2020). This is a genuine mechanistic signal — not a confound — that
would appear counterintuitive without the omikli framework. It should be flagged as an
interpretable finding rather than filtered as paradoxical.

**WES/panel inflation and cross-study bias.** The pipeline aggregates mutation counts from
studies sequenced with diverse panels and WES assays. Since omikli targets gene-dense, early-
replicating regions (paper:MasPonte2020), WES/panel data over-represent A3-context mutations
relative to WGS. Cancer types with high A3 activity (bladder, breast, HNSC) will therefore show
inflated A3 mutation frequency in WES/panel-dominated cBioPortal studies relative to WGS
studies. Cross-study meta-analysis of APOBEC signal should stratify or control for assay type
(WGS vs WES vs panel) to avoid systematic upward bias in coding-region-centric cohorts.

**Sub-signature attribution limitation.** The YTCW/RTCW pentanucleotide distinction between A3A
and A3B (paper:Carpenter2023) requires WGS-scale mutation counts and cannot be reliably computed
from the typical per-sample mutation counts in cBioPortal panel-sequencing data. The h08
pipeline cannot routinely attribute SBS2/13 to A3A vs A3B at the sample level in most studies;
this fractionation is a potential improvement only for WGS-scale studies (e.g., MC3 TCGA).

**Driver gene context.** Chromatin modifier genes (KMT2A/C/D, SETD2, ARID2, PBRM1) that appear
in the pipeline's cross-study mutation frequency tables at elevated rates in APOBEC-active cancers
partly reflect the omikli mechanism (spatial enrichment in gene-rich domains) rather than purely
positive selection (paper:MasPonte2020). Mutation frequency rankings for these genes in high-APOBEC
cancer types should be annotated with this mechanistic caveat.

---

## Key References

- paper:Carpenter2023 — Direct cell-line comparison of A3A vs A3B mutagenic outputs; establishes
  YTCW/RTCW as a sub-signature discriminant and confirms both as causal SBS2/SBS13 sources.
- paper:MasPonte2020 — Identifies omikli as the dominant APOBEC3 cluster mode; demonstrates
  MMR-dependency and preferential omikli enrichment in gene-dense chromatin; mechanistically
  links A3A to omikli and A3B to kataegis.
