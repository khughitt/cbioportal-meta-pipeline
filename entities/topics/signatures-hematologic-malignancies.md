---
type: topic
title: Mutational signatures in hematologic malignancies
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: topic:signatures-hematologic-malignancies
ontology_terms:
- mutational signatures
- hematological malignancies
- multiple myeloma
- acute myeloid leukemia
- chronic lymphocytic leukemia
- therapy-related myeloid neoplasm
- APOBEC
- clonal hematopoiesis
- signature fitting
- COSMIC SBS
source_refs:
- paper:Diamond2023
- paper:Goel2026
- paper:Lee2023
- paper:Maura2019
- paper:Maura2023
- paper:Rustad2021
- paper:Bolton2020
related:
- paper:Diamond2023
- paper:Goel2026
- paper:Lee2023
- paper:Maura2019
- paper:Maura2023
- paper:Rustad2021
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
- topic:signature-decomposition-unmatched-normal
- topic:clonal-hematopoiesis-contamination
- topic:tumor-mutational-burden
- question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross
- question:0019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in
---

# Mutational signatures in hematologic malignancies

## Summary

Hematologic malignancies occupy a distinct region of mutational-signature space: clock-like
processes (SBS1, SBS5, SBS40) and lineage-specific activities (APOBEC/SBS2-13 in myeloma, AID/SBS9
in CLL, oxidative SBS8 in myeloid tumors) dominate, while the environmental exposures that anchor
positive controls in solid tumors (UV/SBS7, tobacco/SBS4) are absent by expectation. Superimposed on
this biological background are iatrogenic signals — platinum (SBS31/SBS35) and melphalan (SBS-MM1) —
that act as precise temporal barcodes of prior cytotoxic therapy, with detectability modulated by
clonal escape routes that create systematic false-negative structure. Technically, this disease class
requires cosine-similarity-driven error suppression, matched-normal subtraction, and COSMIC v3+
reference catalogues; panel-sequenced studies cannot contribute per-sample signature exposures.

---

## Key Concepts

**Clock-like signatures (SBS1, SBS5, SBS40).** Ubiquitous age-related processes that form the
baseline in all hematologic malignancy types. SBS1 accumulates via spontaneous CpG deamination;
SBS5/SBS40 have no fully resolved mechanism but scale with time since cell division. In AML, SBS5
and SBS40 are the dominant signals (paper:Goel2026); in MM, SBS5 is used for molecular timing of
chromosomal gains (paper:Diamond2023). Because these signatures are flat across trinucleotide
contexts, they are the most vulnerable to inter-sample bleeding and cross-signature confusion in
naive fitting.

**APOBEC mutagenesis (SBS2/SBS13).** APOBEC3 cytidine deaminase activity produces CC>TT and
C>G transversions at TpC contexts, most prominently in MM (paper:Maura2023). High APOBEC exposure
independently predicts shorter progression-free survival in daratumumab-era NDMM, making it the
best-validated clinically actionable signature in heme malignancies. SBS2 and SBS13 were poorly
separated in COSMIC v2 but are cleanly resolved in v3.1 (paper:Rustad2021), making reference-version
choice non-trivial.

**AID/SBS9 (non-canonical activation-induced deaminase activity).** Germinal center mutagenesis
via polymerase eta acting on AID-deaminated templates produces SBS9 (G>T transversions at TpA). In
CLL, SBS9 is confined to IGHV-mutated cases (M-CLL) except where IGHV status is misclassified
(paper:Rustad2021). In MM, low SBS9 contribution predicts poor PFS (paper:Maura2023). SBS9 is
particularly vulnerable to assay type: non-coding AID targets make SBS9 largely invisible in WES
or panel data (paper:Rustad2021).

**Iatrogenic signatures (SBS31/SBS35, SBS-MM1, SBS-HSPC).** Platinum-based chemotherapy deposits
SBS31 and SBS35 (N2G adducts and interstrand crosslinks) with effectively 100% penetrance in
exposed patients who develop tMN (paper:Diamond2023). Melphalan alkylation deposits SBS-MM1 at
~41% penetrance due to leukapheresis escape: clones removed to apheresis before myeloablation
avoid exposure and, when reinfused, generate tMN lacking the signature (paper:Diamond2023,
paper:Lee2023). SBS-HSPC (hematopoietic stem/progenitor cell background) is a heme-specific
addition beyond the standard COSMIC catalogue that corrects for the stem-cell mutation clock
distinct from SBS1/SBS5.

**Inter-sample bleeding.** When biologically distinct subgroups are pooled for de novo NMF
extraction, signatures active in one subgroup "bleed" into samples from the other. The canonical
example is the platinum signature appearing in primary AML when therapy-related AML cases are
included in the same NMF run (paper:Maura2019). The corollary for
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` is that
study composition (fraction of post-treatment patients) is a potential confounding covariate that
must be modeled.

**HRD/SBS3 false positive in MM.** SBS3 — traditionally a marker of BRCA1/2-mediated homologous
recombination deficiency — is extracted in naive MM decompositions but is a fitting artefact driven
by the flatness of SBS3 substituting for SBS5. MM lacks the structural hallmarks of BRCA-null
cancers (microhomology deletions, HRD-LOH, tandem duplications). HRDetect scores fall to near zero
when SBS8 replaces SBS3 in the fitting (paper:Maura2019). This is a cautionary example for any
cross-cancer agnostic pipeline: a biologically implausible assignment (HRD in plasma cells) can
pass naive statistical thresholds and must be guarded against via orthogonal validation.

---

## Current State of Knowledge

### Settled biology

The dominant mutagenic processes in each major hematologic lineage are now well characterized.
In MM (plasma cell tumors), the canonical active signatures are SBS1, SBS5, SBS2, SBS13, SBS8,
SBS9, and SBS18 (paper:Maura2023; paper:Maura2019). In CLL, SBS1, SBS5, and SBS9 predominate,
with nc-AID detectable in both M-CLL and U-CLL via localized IGH locus analysis (paper:Maura2019).
In AML, SBS5, SBS8, and SBS40 dominate endogenous mutagenesis (paper:Goel2026), while iatrogenic
signatures (SBS31/SBS35, SBS-MM1) appear in therapy-related cases (paper:Diamond2023). The absence
of UV (SBS7) and tobacco (SBS4) signatures in all hematologic subtypes is a consistent negative
reference — any cross-study pipeline recovering SBS4 or SBS7 in a heme cohort should flag this as
a likely artefact.

The clinical significance of APOBEC activity in MM is established across multiple independent
cohorts: high SBS2/SBS13 predicts inferior outcomes under conventional and daratumumab-era
immunotherapy alike (paper:Maura2023), making APOBEC the most actionable signature predictor
currently validated in myeloma.

The iatrogenic signatures (SBS31/SBS35, SBS-MM1) behave as temporal barcodes: chemotherapy-related
SBS are embedded within duplicated mutations inside chromosomal gains, allowing determination of
whether copy-number events preceded or followed drug exposure (paper:Diamond2023, paper:Lee2023).
This temporal logic has been validated in 8 tMN cases and cross-validated against SBS5 molecular
timing.

The three-step workflow — (1) de novo NMF extraction, (2) COSMIC catalogue assignment, (3)
fitting restricted to the identified shortlist — is now the consensus recommendation for heme
malignancy signature analysis (paper:Maura2019), implemented in the `mmsig` tool with cosine-
similarity-driven error suppression (paper:Rustad2021). Unconstrained fitting (e.g., running
deconstructSigs against all 30+ COSMIC signatures) produces systematic false positives.

### Panel-sequencing limitation

Panel-sequenced tumors yield too few mutations per sample for reliable per-sample signature fitting
in heme malignancies: MM WES panels produce ~245 mutations (vs. ~5,437 by WGS) and CLL WES panels
produce ~108 mutations (paper:Rustad2021). At <500 mutations, only signatures with highly distinctive
profiles (SBS2, SBS9) remain identifiable; flat clock-like signatures (SBS5) become unreliable. This
is a hard constraint for the cBioPortal cross-study pipeline: the majority of cBioPortal heme studies
are panel-sequenced and cannot contribute per-sample signature exposures to an agnostic association
scan.

---

## Controversies and Open Questions

### The leukapheresis escape paradox and SBS-MM1 penetrance

The 41% penetrance of SBS-MM1 in melphalan-exposed tMN is not a measurement failure — it reflects a
biological escape route (apheresis-collected CH clones avoid drug exposure) that is expected to be
study-design-dependent (paper:Diamond2023, paper:Lee2023). However, the exact fraction of ASCT
patients whose eventual tMN arises from a reinfused versus a surviving exposed clone is unknown
prospectively. [SPECULATION] The penetrance could be substantially higher in non-ASCT melphalan
contexts (e.g., oral melphalan in non-transplant-eligible patients) where the apheresis escape route
is unavailable, but this has not been systematically quantified. For any cross-study aggregation
using clinical covariates, "prior melphalan" will be a noisy predictor of SBS-MM1 with
effect-size attenuation proportional to the ASCT rate in the study.

### SBS9 and IGHV status as a positive-control axis in CLL

SBS9 is biologically constrained to GC-exposed cells and is an ideal
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` positive
control in CLL: IGHV-mutated status (a clinical covariate) upstream of SBS9. However,
paper:Rustad2021 reports at least one IGHV-unmutated patient with evidence of SBS9, suggesting
IGHV-mutated status is not a perfectly clean upstream predictor. Whether this reflects measurement
error in IGHV quantification or genuine GC-bypass is unresolved.

### COSMIC reference version sensitivity

The choice of COSMIC v2 versus v3.1 materially alters estimated exposures for all signatures tested
(paper:Rustad2021; Wilcoxon p < 0.001 across all signatures). SBS2 and SBS13 are poorly separated in
v2 but resolved in v3.1; SBS1 estimates are inflated in v2. Cross-study pooling of signature
exposures computed under different COSMIC versions is therefore unreliable, and any cBioPortal
meta-analysis that aggregates published signature-exposure annotations from individual studies must
audit reference-version provenance before combining estimates.

### SBS8 interpretation in myeloid tumors

SBS8 appears as a secondary signature in AML (paper:Goel2026) and in MM (paper:Maura2023), where it
has been attributed to oxidative DNA damage. However, SBS8 has an overlapping flat profile with SBS5
and SBS9, making disambiguation challenging. [SPECULATION] The proportion of SBS8 in AML may partly
reflect oxidative stress from aberrant metabolic activity in myeloid blasts (consistent with the KEGG
central-carbon-metabolism enrichment in paper:Goel2026), but no mechanistic experiment confirms this
in heme malignancies.

### HRD absence in MM

The falseness of the SBS3/HRD signal in MM is well established methodologically (paper:Maura2019),
but whether a small MM subpopulation with genuine BRCA-mediated HRD exists is left open. Given the
small MM WGS cohort sizes to date (n=30-82), a rare HRD subgroup (<5%) would have limited power to
surface. This remains a small but genuine open question.

### South Asian and non-European population calibration

The Goel2026 cohort is Indian (South Asian), and COSMIC signature training data substantially
underrepresents this population. Minor signature assignments (SBS22, SBS24, SBS26 in paper:Goel2026)
at low levels in this cohort may be artefactual overfitting to ethnicity-specific germline
polymorphism patterns rather than real somatic processes (paper:Goel2026). Population-specific
reference catalogues for heme malignancies do not yet exist.

---

## Relevance to This Project

### Implications for the agnostic signature-aetiology aggregation

**Positive controls available in hematologic studies.** The heme malignancy literature
provides a rich but structurally different positive-control set from solid tumors:

| Expected association | Confidence | Caveat for cross-study recovery |
|---|---|---|
| Prior platinum exposure → SBS31/SBS35 | High (100% penetrance) | Requires clinical treatment metadata; WGS studies only |
| Prior melphalan + ASCT → SBS-MM1 | Medium (41% penetrance) | ASCT escape dilutes signal; noisy clinical predictor |
| IGHV-mutated CLL → SBS9 | High | WGS or deep WES required; not visible in standard cBioPortal panels |
| High APOBEC activity → adverse MM outcome | High (replicated) | Outcome covariate, not upstream aetiological variable |
| Absence of SBS4/SBS7 in all heme types | High (negative control) | Any recovery of these signals flags a batch or contamination artefact |

The cBioPortal cross-study pipeline is predominantly panel-sequenced. The
`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`
positive-control test for heme malignancies is therefore primarily a study-level rather than
sample-level exercise:
platinum/melphalan signatures will be detectable only in WGS-based heme studies (e.g., CoMMpass,
Beat AML, TCGA LAML from the MC3 unified MAF), not in targeted-panel cBioPortal submissions.

**Inter-sample bleeding as a nuisance covariate.** The platinum/melphalan bleeding artefact
(paper:Maura2019) motivates adding study composition — specifically, the fraction of post-treatment
or therapy-related cases per study — as an explicit nuisance covariate in the agnostic association
scan. If a cBioPortal AML study is enriched for tMN patients without that annotation, naive
signature decomposition will produce inflated SBS31/SBS35 estimates in de novo AML samples via
bleeding.

**Toolchain and reference-version alignment.** The mmsig + COSMIC v3.1 combination is the current
community standard for heme signature fitting (paper:Rustad2021; paper:Maura2023). If the pipeline
moves toward per-sample signature exposures
(`question:0018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross`), it should
use COSMIC v3.1+ and a restricted reference panel appropriate to each cancer type — not a pan-cancer
unconstrained fit. Any pooling of externally computed signature exposures from cBioPortal study
metadata must audit which COSMIC version was used before aggregation.

**Clock-like signatures as discovery targets.** SBS5 and SBS40 dominate AML (paper:Goel2026) and
contribute substantially to MM and CLL. These are the primary targets for the agnostic association
prediction that novel upstream covariates can explain clock-like signature exposure. Novel covariates
could include: age at diagnosis, clonal hematopoiesis clone size, time from CH detection to AML
transformation, or exposure-related variables not yet annotated in clinical tables.

**TP53 and CH contamination interaction.** In therapy-related tMN, TP53-mutant CH clones survive
myeloablation and give rise to high-TMB, chromothriptic AML (paper:Diamond2023). TP53 is one of
the seven Bolton et al. [@Bolton2020] CH-priority genes already flagged by the pipeline's
`annotate_ch.py` step.
The tMN biology reinforces that TP53 in blood-derived samples may represent pre-leukemic CH — a
source of signal that the `ch_priority_gene` flag is designed to surface but that the pipeline
currently does not link back to the iatrogenic signature context.

**WES without matched normals (Goel2026 case).** The absence of matched germline controls in
paper:Goel2026, combined with population-specific germline polymorphisms (TET1 A256V), illustrates
the risk of false-positive somatic calls that inflate mutation burden and distort signature
attribution in unmatched-normal studies — the exact confound tracked under
`topic:signature-decomposition-unmatched-normal`. The pipeline's `matched_normal_studies` config
list is the primary mitigation.

---

## Key References

- paper:Maura2019 — foundational methods paper establishing the three-step de novo + COSMIC +
  restricted-fit workflow and exposing inter-sample bleeding in MM, CLL, AML.
- paper:Rustad2021 — introduces the `mmsig` R package with cosine-similarity error suppression;
  establishes COSMIC v3.1 superiority and quantifies WES/panel limitations for per-sample fitting.
- paper:Diamond2023 — WGS of 39 tMN cases; establishes platinum/melphalan signatures as temporal
  barcodes and characterizes two clonal evolutionary routes to tMN.
- paper:Lee2023 — editorial synthesis of Diamond2023; clarifies the two evolutionary modes and
  their implications for cross-study signature confounding.
- paper:Maura2023 — integrates WGS + scRNA in NDMM; validates APOBEC (SBS2/SBS13) as pan-
  treatment adverse predictor and introduces SBS9 as an independent prognostic marker.
- paper:Goel2026 — small Indian AML WES cohort; confirms SBS5/SBS8/SBS40 dominance in AML,
  illustrates germline-contamination risk in unmatched cohorts, provides a non-European reference
  point for signature calibration.
