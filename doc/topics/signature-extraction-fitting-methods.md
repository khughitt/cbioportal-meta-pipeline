---
id: "topic:signature-extraction-fitting-methods"
type: "topic"
title: "Mutational-signature extraction, fitting, and assignment methods"
status: "active"
created: "2026-05-31"
updated: "2026-05-31"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "method:h08-agnostic-association-model"
  - "question:q018-can-mutational-signature-decomposition-be-added-downstream-of-the-cross"
  - "question:q019-does-de-novo-extraction-on-the-aggregated-cohort-surface-factors-not-in"
  - "paper:Battuello2024"
  - "paper:Besselink2023"
  - "paper:Buscaroli2026"
  - "paper:DeVito2025"
  - "paper:DiazGay2023"
  - "paper:DiazGay2025"
  - "paper:Hubschmann2021"
  - "paper:Islam2022"
  - "paper:Jiang2025"
  - "paper:Jin2024"
  - "paper:Kesimoglu2026"
  - "paper:Landy2026"
  - "paper:Lee2022"
  - "paper:Lee2023a"
  - "paper:Manders2022"
  - "paper:Medo2024"
  - "paper:Miura2022"
  - "paper:Nguyen2020"
  - "paper:Pancotti2023"
  - "paper:Pandey2022"
  - "paper:Steele2022"
  - "paper:VazquezGarcia2022"
  - "paper:Wan2022"
  - "paper:Wong2022"
  - "paper:Wu2023"
  - "paper:Zhang2026"
  - "paper:Zou2018"
---

# Mutational-signature extraction, fitting, and assignment methods

## Summary

Mutational-signature analysis decomposes a tumour's somatic mutation catalogue into contributions
from distinct biological or technical mutagenic processes. Two complementary tasks exist: de novo
*extraction* (discovering signatures from data) and *fitting* / *assignment* (measuring per-sample
exposures to a known catalogue). For h08 — the agnostic within-tissue covariate ↔
signature-exposure association — the per-sample exposure matrix H is the outcome variable of
every association test. The quality, calibration, and biological specificity of H therefore
determine whether h08 can recover known aetiologies (UV/SBS7, smoking/SBS4, APOBEC/SBS2-13,
MMR/MSI) as positive controls and surface novel covariate links. This topic synthesises the
methodological state of the art, the settled questions, the active tensions, and the concrete
implications for the cbioportal cross-study pipeline.

---

## Key Concepts

**The NMF decomposition.** Both extraction and fitting express the mutation count matrix M
(samples × 96-channel SBS contexts) as M ≈ W H, where W (signatures × contexts) and H
(samples × exposures) are non-negative. For fitting, W is fixed at the COSMIC catalogue; for
de novo extraction, both W and H are learned. The resulting H column for each sample is the
per-sample exposure vector used as h08's outcome.

**The COSMIC catalogue.** COSMIC SBS v3.x (60 non-artefactual signatures in v3.3; 79 total)
is the dominant reference. Individual signatures range from spiky and distinctive (SBS7a/UV,
SBS4/smoking) to flat and near-uniform (SBS3/HRD, SBS5/clock, SBS40/ageing). paper:Pancotti2023
shows that 29 archetypes can reconstruct all 60 profiles, and that a "Light Grey" archetype
collapses the flat-signature cluster (SBS3, SBS5, SBS8, SBS40, SBS25, SBS93) — these are
mathematically near-indistinguishable and their individual exposures are inherently uncertain.

**Flat signatures as the critical challenge.** Across the whole literature, flat signature
assignments are the consistent pain point. paper:Jin2024 shows standard NMF systematically
distorts SBS3 (mvNMF corrects this). paper:Wu2023 shows cross-tool Kendall tau-b for SBS3 falls
as low as 0.15–0.34 (vs 0.90+ for SBS2/SBS13 and SBS1). paper:Medo2024 shows that fitting
error scales with Shannon equitability index. paper:Lee2023a and paper:Battuello2024 both find
flat signatures (SBS5/SBS40) cannot be reliably separated by targeted panels. paper:Pancotti2023
traces this to the COSMIC signature geometry: near-uniform profiles lie at the centre of the
simplex, making them co-linear with any mixture. The h08 association scan must treat associations
with SBS5/SBS3/SBS40 as requiring additional validation.

---

## Established Consensus

### Causal ground truth for the h08 positive controls

paper:Zou2018 provides isogenic CRISPR-Cas9 causal validation: MSH6 knockout reproduces COSMIC
Signature 20 (MMR-deficiency); EXO1 loss generates signatures resembling SBS3 (HR deficiency)
and Rearrangement Signature 1 (RS1); FANCC loss yields microhomology-mediated deletion indels
and RS3/RS5 (BRCA1-type HR rearrangements). paper:Lee2022 demonstrates that Lynch Syndrome
normal epithelium is not hypermutated — MMR-deficiency-associated SBSs (SBS20, SBS21, SBS26,
SBS44) and indels (ID1/ID2/ID7) appear only after second-hit LOH and clonal expansion, providing
ground truth for the MMR positive control. paper:Steele2022 (Alexandrov lab review) maps the
canonical aetiological links: UV → SBS7, smoking → SBS4, APOBEC3A/B → SBS2/SBS13, MMR-loss →
SBS6/15/26, POLE proofreading mutations → SBS10a/b. These ground truths are the targets h08
must recover before trusting novel associations.

Key caution from paper:Zou2018: POLE *loss* does not reproduce SBS10; the tumour signature
requires a dominant-negative proofreading missense. Consequently, POLE loss-of-function variants
in cBioPortal data are not a valid positive-control proxy for SBS10 — only POLE hotspot
mutations (as detected by `detect_polymerase_hotspots`) qualify.

### Variant calling is an upstream determinant of extracted signatures

paper:Jiang2025 demonstrates that consensus calling (≥2 callers) is essential for artifact-free
de novo SBS extraction. Single-caller outputs introduce reproducible artifactual signatures
(VarScan2 → SBS96C, MuSE → SBS96D in WES; MuTect → SBS96I/J, SAGE → SBS96H in WGS). These
artifacts overlap known COSMIC artifact signatures (SBS50, SBS51, SBS60-like) and localize to
repeat-masked, low-coverage, or low-VAF regions — the same sites enriched in unmatched-normal
germline leakage. The MC3 TCGA release (already in the pipeline) uses consensus 2+/3 calling and
passes this validity check. Single-caller cBioPortal studies are at risk of producing artifactual
de novo signatures that masquerade as biological discoveries.

A minimum mutation burden of ~383 SBSs is required for stable WES SBS-96 profiles (paper:Jiang2025),
consistent with the 64–323 mutation threshold from paper:Battuello2024. Both converge on the same
practical filter: low-burden samples should be excluded from signature decomposition before h08
covariate association.

### SigProfilerExtractor is the strongest de novo extraction tool

paper:Islam2022 benchmarks 14 tools across 34 scenarios (>80,000 synthetic cancer genomes) and
shows SigProfilerExtractor outperforms all others: 20–50% more true-positive signatures at 5%
noise in WGS settings, with >5-fold fewer false positives. It is the only tool achieving average
F1 > 0.60 in WES noise scenarios. The automatic rank selection via NMFk performs near-identically
to forced selection (rF1 ≈ 1.0 on medium and hard scenarios), reducing analyst-dependent
hyperparameter choices. Key discovery: SBS92 (bladder/tobacco), found only by de novo
extraction on WGS — invisible to WES because its profile concentrates in intergenic regions.

### Refitting tools: SigProfilerSingleSample excels at low burden; SigProfilerAssignment and MuSiCal at high burden

paper:Medo2024 benchmarks 12 fitting tools across mutation-burden regimes:
- ≤1,000 mutations: SigProfilerSingleSample is best.
- ≥2,000 mutations: SigProfilerAssignment and MuSiCal emerge as top performers.
- The reconstruction similarity score of SigProfilerSingleSample is a poor universal threshold;
  it reflects mutation count as much as fit quality.

paper:Battuello2024 reaches a compatible conclusion: among 5 commonly-used tools on CRC,
SigProfilerAssignment provides the highest biological stratification (ΔMMR, ΔPOLE) even though
mathematical cosine similarity is comparable across tools. MutationalPatterns is the best balanced
choice for coding-region data.

paper:Wu2023 independently confirms that the Refit strategy (active-set pre-selection followed
by re-fitting) beats both Regular (all signatures) and Remove (post-hoc zeroing) across all five
tools tested. Ensemble averaging of five tools (EnsembleFit) reduces RMSE by 15.9–24.7% over the
best single tool, with the largest benefit for flat signatures.

### Reference catalogue restriction: helpful only at low mutation counts

paper:Medo2024 shows that restricting the COSMIC reference to "likely active" signatures improves
performance at ~100 mutations/sample but is harmful at ≥2,000 mutations. The restricted
assignment strategy in `run_restricted_sigprofiler_assignment.py` is therefore appropriate for
panel-sequenced cBioPortal studies but should be replaced by full COSMICv3 refitting for WGS/WES
cohorts like MC3.

### Out-of-catalogue signatures are the biggest unsolved challenge for all refitting tools

paper:Medo2024: when 20% of true activity derives from signatures absent from the reference,
precision falls 20–40% across all 12 tools. Three tools (deconstructSigs, STL, sigfit) redistribute
less mass to wrong signatures but still fail on overall metrics. This is directly relevant to
the cross-study pipeline: cancer-type-specific or study-specific signatures not in COSMIC
(e.g., recently added SBS88, SBS92-SBS95, novel geographic signatures from paper:DiazGay2025)
will be mis-attributed to the nearest reference signature, inflating false-positive covariate
associations in h08b.

### Multi-study Bayesian frameworks match the pipeline's cross-study structure

paper:DeVito2025 reviews Grabski 2025 (Multi-Study NMF) and Hansen 2025 (BaP Multi-NMF), which
jointly model S study-specific count matrices with a shared signature matrix and study-specific
binary inclusion indicators. BaP Multi-NMF's probit model directly incorporates sample-level
covariates into the exposure estimation, making it the closest published analog to h08's
covariate-association design. The cbioportal pipeline's per-study MAF structure maps directly
onto these models' study-specific data structure.

---

## Active Tensions and Disagreements

### Tension 1: Extraction first, then refit — or jointly?

The dominant practice (paper:Islam2022; paper:DiazGay2023) is sequential: de novo extraction to
identify active signatures, then per-sample restricted refitting against those signatures.
paper:Kesimoglu2026 (ReDeNovo), paper:Buscaroli2026 (BASCULE), and paper:DeVito2025 (Grabski/Hansen)
all argue for simultaneous known + novel signature inference, avoiding the sequential composition of
errors. paper:Jin2024 (MuSiCal) uses mvNMF + in-silico validation, also jointly. ReDeNovo achieves
a de novo SDR of 1.000 vs 0.742 for CaMuS and 0.175 for MuSiCal in benchmark conditions. This
is an active methodological competition with no settled winner for the cross-study aggregation context.

### Tension 2: Flat signatures — assign separately or merge?

paper:Jin2024 argues SBS40 is systematically over-assigned by NNLS and restricts it to kidney/bladder.
paper:Pancotti2023 groups SBS3/SBS5/SBS8/SBS40/SBS25/SBS93 under a single archetype and suggests
these may be mathematical blends rather than distinct biological processes. paper:Wu2023 shows
SBS3 cross-tool Kendall tau-b as low as 0.15 — effectively noise. Yet paper:Lee2023a shows SATS
can detect SBS1 (also flat, clock-like) in targeted sequencing when context normalization is applied.
The resolution appears to be: flat signatures need either much larger cohort sizes (paper:Pancotti2023:
≥10,000 samples for reliable extraction of a 20-signature scenario), explicit panel-context
normalization (paper:Lee2023a), or Bayesian treatment with posterior uncertainty reported
(paper:Landy2026; paper:Buscaroli2026). No single tool has solved this across all deployment contexts.

### Tension 3: WES vs WGS — how much is lost?

paper:Islam2022 shows WES average F1 drops from 0.61 (WGS) to 0.46 (WES) for de novo extraction.
paper:Battuello2024 shows WES achieves higher ΔMMR than WGS for CRC cell lines — not despite
but *because* WGS includes intronic/extragenic regions that dilute true cancer signal with flat
clock-like signatures. paper:Islam2022's SBS92 is WGS-only (intergenic distribution). These
two findings point in opposite directions: for the canonical positive controls, WES may actually
give cleaner signal in coding-region studies; for discovery of novel processes, WGS is necessary.
The cbioportal pipeline operates on coding-region MAFs, which places it closer to the WES regime
and partially protects against the flat-signature dilution that affects WGS analyses
(paper:Battuello2024 finding).

### Tension 4: Panel data — usable or not?

paper:Lee2023a (SATS, 111,711 GENIE tumors) shows that targeted panels can reliably detect
canonical signatures (UV/SBS7, smoking/SBS4, APOBEC/SBS2-13, MMR/SBS6-44, POLE/SBS10) at
the cohort level with panel-context normalization, and that per-sample signature burdens can
be estimated for individual tumors from these results. paper:Medo2024 recommends
SigProfilerSingleSample at ≤100 mutations, which covers panel data. paper:Battuello2024 shows
TSO-500 (523-gene panel) can stratify CRC subtypes at least as well as WES.
By contrast, paper:Islam2022 and paper:Jiang2025 both document that de novo extraction and
profile stability fail for panels without large cohort sizes and context normalization.
The consensus: panel data is viable for refitting to COSMIC with panel-context correction
but not for de novo extraction. Per-sample refitting is feasible at ~100+ mutations with the
right tool.

### Tension 5: Cluster-then-associate vs. jointly model

paper:Buscaroli2026 (BASCULE) clusters patients jointly on SBS+DBS+ID exposure tensors (Dirichlet
Process) and shows DBS-resolved sub-clusters invisible to SBS alone. paper:VazquezGarcia2022
shows structural-variation mutational subtypes (HRD-Dup vs. FBI) predict TME immune programmes.
Both advocate a cluster-based integrative approach that differs from h08's regression-based
association design. The regression approach (h08; sigDriver from paper:Wong2022) is better suited
to continuous covariates and multiple testing correction across hundreds of covariates; the
clustering approach is better suited to discovery of subtype structure. These are complementary
rather than competing, but for h08 specifically the regression architecture is the correct choice.

---

## What Is Settled

1. Consensus variant calling (≥2 callers) is necessary upstream of signature analysis; single
   callers introduce reproducible artifactual signatures that no downstream tool can reliably
   remove (paper:Jiang2025).

2. The Refit strategy beats Regular and Remove across all fitting tools tested (paper:Wu2023;
   paper:Battuello2024; paper:Medo2024).

3. SigProfilerExtractor is the best-evidenced open-source de novo extraction tool for WGS data
   (paper:Islam2022).

4. SigProfilerAssignment is the best single tool for WGS/WES-scale refitting with high mutation
   burden (paper:Medo2024; paper:DiazGay2023).

5. SigProfilerSingleSample is the best tool for low-burden (panel, <500 mutations) refitting
   (paper:Medo2024).

6. Canonical positive-control signatures (SBS7/UV, SBS4/smoking, SBS2/13/APOBEC, SBS6/15/26/44
   /MMR) are high-concordance across tools (Kendall tau-b 0.90+) and are detectable even in
   cfDNA at 0.3× coverage (paper:Wan2022), WES (paper:Battuello2024), and targeted panels
   (paper:Lee2023a). These are reliable h08a positive controls.

7. Flat signatures (SBS3, SBS5, SBS8, SBS40) are unreliable from any single refitting tool at
   typical WES/panel sample sizes. Ensemble approaches (paper:Wu2023) or Bayesian posteriors
   (paper:Landy2026) are needed before treating associations with these signatures as trustworthy.

8. The minimum mutation count for stable per-sample SBS-96 profile is ~383 mutations for WES
   (paper:Jiang2025), 64–323 depending on matched-normal availability (paper:Battuello2024).
   Below this threshold, per-sample signature assignments are unreliable.

9. COSMIC v3 (rather than v2) reduces inter-tool disagreement and improves reconstruction
   fidelity (paper:Pandey2022; paper:Medo2024; paper:Battuello2024).

---

## Gaps

- No benchmarking study has directly evaluated de novo extraction or refitting on cBioPortal-
  style heterogeneous multi-study aggregates (mixed callers, mixed panels, mixed cancer types).

- Per-sample signature assignment from panel data has been studied mainly within single cohort
  designs (GENIE: paper:Lee2023a; TSO-500: paper:Battuello2024). Cross-study variation in
  panel design adds an untested confounder layer.

- The Bayesian multi-study frameworks (paper:DeVito2025; paper:Landy2026) are R-only, limiting
  direct integration into the Python/Snakemake pipeline. Python implementations exist (BASCULE
  via Pyro: paper:Buscaroli2026; bayesNMF via R: paper:Landy2026) but have not been head-to-head
  benchmarked against SigProfilerExtractor on real cross-study aggregated data.

- Extended signature channels (DBS, ID, CN, SV) beyond SBS-96 are supported by only a subset
  of tools (SigProfilerExtractor, SignatureAnalyzer, BASCULE). For the h08 pipeline, DBS and
  ID signatures are potentially informative (paper:Buscaroli2026 shows DBS resolves sub-clusters;
  paper:Jin2024 proposes 9 new ID signatures) but require per-sample indel counts that are
  variable across studies.

- The interaction between hypermutator exclusion and signature extraction is handled differently
  across tools (MMRD/POLE separate stratum: paper:Jin2024; NB mixture: paper:Landy2026; GMM
  per-cancer: existing pipeline). No systematic comparison of these strategies exists.

- Transformer-based approaches (paper:Zhang2026, SigFormer) have not been peer-reviewed and
  code was private at preprint posting. Deep-learning frameworks may offer advantages for the
  flat-signature problem but are not yet pipeline-ready.

---

## Implications for h08 and the Cross-Study Signature-Aetiology Aggregation

### Upstream prerequisites before running h08

**Variant-calling provenance audit.** Per paper:Jiang2025, per-study caller information should
be extracted and single-caller studies flagged as higher-risk for artifactual de novo signatures.
MC3 (consensus 2+/3) and matched-normal studies already in `matched_normal_studies` pass this
check. Single-caller cBioPortal studies may introduce SBS50/SBS51/SBS60-like artifacts that
generate spurious covariate hits.

**Minimum mutation count filter.** Per paper:Jiang2025 and paper:Battuello2024, exclude
per-sample profiles with <383 SBSs (WES) or implement the matched-normal-adjusted threshold
(64 mutations minimum when matched). This should be an explicit filter in the h08 signature
decomposition step, separate from the existing hypermutator annotation.

**Hypermutator exclusion.** The planned hypermutator annotation pipeline (t081/t092-t099)
produces `is_hypermutator` flags that map onto the preprocessing separation recommended by
paper:Jin2024 (MMRD/POLE analyzed separately), paper:Landy2026 (NB mixture exclusion), and
paper:Lee2023a (separate hypermutated subset in SATS). POLE samples require separate treatment:
paper:Zou2018 establishes that POLE loss ≠ SBS10; only POLE hotspot mutations drive the
ultra-hypermutator signature.

### Tool choice for the h08 fitting step (q018)

The literature supports a mutation-count-stratified approach:
- **Panel studies (<500 mutations/sample):** SigProfilerSingleSample with full COSMICv3;
  SATS with panel-context matrix L if running cohort-level extraction (paper:Lee2023a).
- **WES/WGS (500–5,000 mutations):** SigProfilerSingleSample or SigProfilerAssignment Refit.
- **MC3 WGS (>5,000 mutations):** SigProfilerAssignment Refit or MuSiCal (paper:Medo2024).
- **Ensemble as validation layer:** For the three mandatory positive controls (SBS7, SBS4,
  SBS2/13), running EnsembleFit (paper:Wu2023) alongside the primary tool provides a
  robustness check at low additional cost. This is particularly important for SBS3 (HRD),
  where SigProfilerAssignment has the lowest qualitative PPV (paper:Wu2023).

### Positive-control recovery expectations (h08a)

The following signatures are reliably recoverable across all deployment contexts tested in this
literature and should serve as unconditional pass/fail positive controls for h08a:

| Signature | Aetiology | Evidence |
|---|---|---|
| SBS7a/SBS7b | UV radiation (melanoma) | paper:DiazGay2023, paper:Miura2022, paper:Zhang2026 |
| SBS4 (+SBS92 for WGS) | Tobacco smoking (lung/bladder) | paper:Islam2022, paper:Miura2022, paper:Lee2023a |
| SBS2 + SBS13 | APOBEC3A/B (breast, bladder) | paper:Manders2022, paper:Miura2022, paper:Wan2022 |
| SBS6/SBS15/SBS20/SBS21/SBS26/SBS44 | MMR deficiency / MSI-H | paper:Zou2018, paper:Lee2022, paper:Wan2022, paper:Lee2023a |

Concordance thresholds: expect Kendall tau-b ≥ 0.90 between tools for SBS2/13 and SBS1; expect
≥ 0.70 for SBS4 and SBS7. Values below these signal either calibration failure or tool-specific
artefact.

SBS3 (HRD/BRCA-deficiency) is **not** a reliable unconditional positive control because of
systematic over-assignment and low cross-tool concordance (paper:Wu2023; paper:Jin2024). If HRD
is a target, require Ensemble-Unanimous calling or use CHORD's raw-context classifier
(paper:Nguyen2020) instead of NNLS-fitted SBS3.

### De novo extraction (q019): feasibility conditions

De novo extraction on the aggregated cross-study cohort is feasible only under these conditions
(paper:Islam2022; paper:Pancotti2023):
- Minimum ~3,000–5,000 samples per cancer type for scenarios with >10 co-occurring signatures
  (Pancotti2023 Scenario 3 requires 10,000 samples for 80% success).
- Consensus variant calling across contributing studies; single-caller contamination will inject
  artifactual de novo signatures (paper:Jiang2025).
- Within-tissue (per-cancer-type) extraction, not pan-cancer pooling, to avoid tissue collinearity
  confounding h08's within-tissue conditioning requirement.

Simultaneous catalogue-aware + de novo methods (ReDeNovo: paper:Kesimoglu2026; BASCULE:
paper:Buscaroli2026) offer an advantage: they prevent de novo signatures from being spurious
linear combinations of catalogue entries, which is the dominant false-positive mode when running
SigProfilerExtractor without restrictions.

### Novel discovery considerations (h08b)

paper:DiazGay2025 provides a direct model for h08b: covariate-based discovery of signatures
from geographic variation identified SBS89/DBS8/ID_J in Argentina and SBS94/SBS_F/DBS6 in
Colombia — both sets have no known aetiology and emerged via agnostic enrichment regression
adjusted for confounders. The cbioportal pipeline's cross-study aggregation is structurally
analogous, with study provenance substituting for geography.

paper:Wong2022 (sigDriver) demonstrates that kernel regression of per-sample signature exposures
against a structured predictor (genomic hotspot presence) surfaces both positive and negative
associations (PIK3CA E542K/E545K positively APOBEC-associated; PIK3CA H1047R negatively
SBS39-associated). The regression architecture is a direct template for h08's covariate
association layer.

Out-of-catalogue signal is the biggest driver of false positive h08b discoveries: if an active
process is absent from COSMICv3, all fitting tools redistribute its mutations to the nearest
catalogue entry, creating spurious covariate associations with that entry (paper:Medo2024). The
explicit unattributed residual channel in paper:Zhang2026 (SigFormer) is a design feature that
reduces this risk, as is the simultaneous de novo discovery in paper:Kesimoglu2026 and
paper:Buscaroli2026. For the h08b prong, any novel association should be validated by checking
whether the attributed signature's profile shifts in the direction of the putative aetiology
(paper:Miura2022's iS score provides a per-sample exclusion test applicable here).

### Confounders to exclude before trusting covariate associations

- **Flat-signature catch-all inflation (SBS5, SBS40):** associations with these signatures may
  reflect unmodelled signal absorbed from any source, not a true causal covariate link. Require
  ensemble agreement and effect size ≥ 2× any single-tool noise estimate (paper:Wu2023;
  paper:Zhang2026).

- **Artefact signatures (SBS27/43/45–60 COSMIC artefact set):** should be excluded from the
  COSMIC reference before h08 fitting (paper:Wan2022; paper:Jiang2025).

- **Treatment-induced signatures (SBS11/temozolomide, SBS31+35/platinum, SBS87/thiopurine,
  SBS32/azathioprine):** paper:Lee2022 shows SBS35 appears in all intestinal crypts of a FOLFOX-
  treated patient; paper:Lee2023a detects SBS32 and SBS87 across GENIE cohorts. These signatures
  carry strong clinical history confounders and should be declared *a priori* as covariates to
  condition on (not discover), lest treatment history masquerade as a biology-signature link.

- **Hypomethylation is not a SBS process:** paper:Besselink2023 demonstrates that global DNA
  hypomethylation at cancer-equivalent levels does not increase SBS burden or enrich any COSMIC
  signature, including MMR-related ones. Any covariate association with a DNMT-expression module
  in h08 would not reflect a direct mutagenic effect of methylation loss; causal reinterpretation
  would be required. The primary consequence of hypomethylation is chromosomal instability —
  relevant to the pipeline's CIN annotation but not to SBS exposures.

### Cross-modality extensions

paper:VazquezGarcia2022 shows that structural-variation mutational subtypes (HRD-Dup, FBI)
predict distinct TME immune programmes (JAK-STAT vs TGFβ) — connecting mutational processes
to expression modules via a pathway orthogonal to SBS signatures. paper:Buscaroli2026 shows
joint SBS+DBS clustering resolves sub-types invisible to SBS alone. These results motivate
extending the h08 exposure matrix H to include DBS, ID, and structural rearrangement signatures
as additional outcome variables if the per-study mutation calls support them. The DBS channel is
most informative for studies with WGS; ID signatures require reliable indel calling.

---

## Tool Landscape Summary

| Task | Recommended Tool | Notes |
|---|---|---|
| De novo extraction (WGS, large cohort) | SigProfilerExtractor | Best benchmarked; automatic rank selection |
| De novo + known simultaneous | ReDeNovo or BASCULE | Better de novo SDR; preprints |
| Single-sample refitting, panel (<500 muts) | SigProfilerSingleSample | Best at low burden |
| Single-sample refitting, WES/WGS | SigProfilerAssignment (Refit) | Best at high burden; pipeline default |
| Ensemble validation | EnsembleFit | 15–25% RMSE reduction; web portal |
| SBS3/HRD specifically | EnsembleFit Unanimous or MuSiCal | Low single-tool PPV for SBS3 |
| Panel-context normalization | SATS | Handles mixed-panel cohorts |
| Bayesian posterior uncertainty | bayesNMF or BASCULE | R/Python; not yet in pipeline |
| Multi-study joint extraction | Grabski/Hansen models | R; cross-study sharing structure |
| Raw-context HRD detection | CHORD | No signature fitting needed |
| Signature–covariate association | sigDriver / direct regression | Template for h08 association layer |
| Phylogeny-aware per-branch refitting | PhyloSignare | NSCLC-validated; not applicable without clone trees |

All tools operate on per-sample or per-cohort SBS-96 matrices. The pipeline must generate
these matrices from the per-study MAF outputs before invoking any signature tool.
