---
type: synthesis
title: Project synthesis - cbioportal
status: active
created: '2026-06-02'
updated: '2026-06-02'
id: synthesis:0003-project-synthesis-cbioportal
report_kind: synthesis-rollup
generated_at: '2026-06-02T09:52:22Z'
source_commit: 037f0ab2d3c84ecc56bebd843e361c1a9dfbfa66
synthesized_from:
- hypothesis: hypothesis:0001-non-tumor-signal-contamination
  file: doc/reports/synthesis/h01-non-tumor-signal-contamination.md
  sha: 469e4ffe80898f947e27df685cf62b76f630fb64
- hypothesis: hypothesis:0002-cross-study-ranking-divergence-is-structured
  file: doc/reports/synthesis/h02-cross-study-ranking-divergence-is-structured.md
  sha: ae4d982f8891850c7b8a85d26e2dd578cf780d7a
- hypothesis: hypothesis:0003-gene-length-confounds-literature-attention
  file: doc/reports/synthesis/h03-gene-length-confounds-literature-attention.md
  sha: f41d7ba71a7e6325415f90d6bbdab66b20dfd17b
- hypothesis: hypothesis:0004-mhn-pathway-ordering
  file: doc/reports/synthesis/h04-mhn-pathway-ordering.md
  sha: b4eaa8e43b8aa7c1585e2e9cfbcc27f8e7ff9ef5
- hypothesis: hypothesis:0005-healthy-somatic-background-atlas
  file: doc/reports/synthesis/h05-healthy-somatic-background-atlas.md
  sha: 27ac266f10fe2f640d2bea058927126a4f638669
- hypothesis: hypothesis:0006-pre-malignant-n-minus-1-driver-carriage
  file: doc/reports/synthesis/h06-pre-malignant-n-minus-1-driver-carriage.md
  sha: 2b61650be04770ee0f9c2b9768d0a42f8199f60c
- hypothesis: hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
  file: doc/reports/synthesis/h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and.md
  sha: 1867db7fb064ed7036e12b186382d062a309f172
- hypothesis: hypothesis:0008-cross-study-signature-exposure-reproducibility
  file: doc/reports/synthesis/h09-cross-study-signature-exposure-reproducibility.md
  sha: 68cbb17a183481e363a89631881604ff718a10f1
- hypothesis: hypothesis:0009-treatment-induced-signature-frequency-contamination
  file: doc/reports/synthesis/h10-treatment-induced-signature-frequency-contamination.md
  sha: 134bc793e5797593b75f0837ba08bc62dadc3b41
- hypothesis: hypothesis:0010-joint-indel-sbs-improves-aetiology-discrimination
  file: doc/reports/synthesis/h11-joint-indel-sbs-improves-aetiology-discrimination.md
  sha: 4808224f7b283be3f6737a7fa11299dcea387f07
emergent_threads_sha: fa9a408ea27a3eca9b499c375626ae34b8dc3450
orphan_question_count: 1
---

# Project synthesis — cbioportal

## TL;DR

- **One proposition is decisively confirmed.** Cross-study gene rankings are structured, not
  random: dNdScv recovers 62/100 Bailey et al. [@Bailey2018] drivers (vs zero for raw and length-adjusted
  schemes) and reaches 88% CGC tier-1 recovery at K=100, while raw and length-adjusted lists are
  near-disjoint (Jaccard@100 = 0.015). This is the project's strongest result
  (synthesis:0006-cross-study-ranking-divergence-is-structured).
- **The signature program (`h08`–`h11`) is the live research frontier** and shares one hardened
  infrastructure stack (t178/t179 SBS-refit provenance + count floors). Its flagship gate, the `h08`
  positive-control scan, came back **inconclusive (1/3 arms)**: only APOBEC→SBS2/13 passed cleanly;
  UV and smoking failed on covariate-proxy quality, not method.
- **Two confounder channels were probed and partly ruled out.** Replication timing does *not*
  explain the residual TTN signal (RT coefficient ~0, CI spans zero); the simple SBS1/SBS5 ratio is
  *not* a usable contamination flag (direction reversed in the BRCA matched-vs-unmatched test).
- **A recurring structural ceiling is data access.** The SBS1 LRR contamination test, the
  healthy-tissue atlas, MHN ordering benchmarks, and external validation all stall on the same
  blocked WGS acquisitions (Hartwig, PCAWG/ICGC-25K, Genomics England, GTEx controlled-access).
- **`h10` (treatment-induced inflation) reached an infrastructure gate but no biological verdict:**
  the full-config impact run covers 383,477 samples, but only one patient cohort (GLASS) passes the
  discovery gate, so the `q027` exclusion arm is `underpowered_non_arbitrating`.
- **The orphan population is small and coherent:** one orphan question (`q009`, SBS1 LRR flag) plus
  six unaffiliated interpretations, dominated by the SBS1/LRR contamination-QC spine that a proposed
  candidate hypothesis **`h07`** would absorb.

## State

The project collectively believes — with its single strongest evidence base — that **cross-study
mutation-frequency rankings carry a reproducible, selection-driven signal that only a dN/dS-aware
method recovers**, and that naive frequency- or length-based ranking schemes are dominated by
structured confounders (protein length, panel ascertainment, fragile sites) rather than noise
(synthesis:0006-cross-study-ranking-divergence-is-structured,
synthesis:0007-gene-length-confounds-literature-attention). The dNdScv ranking is LOSO-stable
(Jaccard@100 = 0.85–0.92 on broad holdouts) and externally validated against CGC, with GENIE
identified as a *structured* rather than generic perturbation.

The strongest **methodological** assets sit in the signature program. The per-sample SBS-refit
layer is hardened (COSMIC version-pinned, caller-provenance flagged, count-floored) and has been
shown by `interpretation:0022-t197-mc3-7strata-sbs-refit` to deliver coherent exposures (SKCM
SBS7a+b ≈ 0.83; lung SBS4 ≈ 0.28–0.36). On that substrate, the one clean positive-control success is
APOBEC expression → SBS2/13 (BH-q ≈ 4e-12, permutation p = 0.001, robust to cis-mutation and
proliferation conditioning).

What is **contested or unresolved**: the `h08` positive-control gate is inconclusive, so discovery
work (H08b) is correctly locked; the residual large-protein (TTN) signal after trinucleotide
correction has no confirmed mechanism (RT ruled out, CFS untested); and the entire contamination
program (`h01`) remains untested at the proposition level — its one executed proxy (SBS1/SBS5)
returned negative. Several hypotheses (`h05`, `h06`, `h09`, `h11`) are infrastructure-ready but
analysis-empty, gated either on blocked external data or on a prerequisite census.

## Arc

**`h02` — cross-study ranking divergence (active).** This is the project's most advanced thread. From
the PoC observation that raw and length-adjusted top-100 lists are nearly disjoint, the work moved
through a full pan-cancer dNdScv run (fixing a tiebreaker artifact and pooled-mean inflation), to
external CGC validation defusing Bailey-circularity, to a LOSO arm that established dNdScv stability
and GENIE as a structured perturbation. P3 (canonical-driver replication) is confirmed; P4 (RT as
dominant residual confounder) is weakened by a null RT regression; the TTN residual is now chased
via fragile-site annotation and hypermutator stratification.

**`h03` — gene length confounds literature attention (active).** The structural prerequisite is
established (PubTator correlations track ranking scheme as predicted), but the decisive partial-slope
regression (`beta_length`) does not yet exist; it is blocked on a pooled-mean fix and assay-stratified
design, with panel-vs-WES ascertainment confirmed as a required covariate.

**`h08` — agnostic covariate→signature association (active).** The most engineering-intensive thread:
feasibility verdict → MC3 7-strata refit → NMF expression modules → within-tissue association core →
pre-registered positive-control gate. Verdict is inconclusive (APOBEC passes; UV/smoking fail on
proxy adequacy). A repaired binary-smoking rerun improved but still missed the top-3 gate. H08b is
held closed pending either a repaired pre-registration or narrowly scoped exploratory work.

**`h09` — cross-study signature reproducibility (active).** Infrastructure-ready (the t178/t179 stack
is exactly its batch-covariate substrate) but analysis-empty; t212 is the first `h09`-specific task and
has not run.

**`h10` — treatment-induced frequency contamination (active).** A concentrated 2026-06-01 burst built
an executable exposure-label substrate at full-config scale in
`interpretation:0030-t207-h10-treatment-impact-full-config` (383,477 samples), but the measured-
signature `q027` arm finds only one adequate patient cohort (36 SBS11-high GLASS samples), leaving
the cross-study biological claim non-arbitrating.

**`h11` — joint indel+SBS discrimination (active).** Earliest-stage active hypothesis; gated on an
indel-availability census (t188) that has not started.

**`h01` — non-tumor contamination (active).** Reference infrastructure (Li 2021 normal-tissue spectra)
exists, but the three-channel contamination partition is untested and the one proxy tried (SBS1/SBS5)
was ruled out.

**How the active hypotheses relate.** Two backbones organize the active set. The **ranking/confounder
backbone** (`h02` ← `h03`, with `h01`'s CFS channel feeding `q014`) asks what survives cross-study aggregation
and why long-tail genes diverge. The **signature backbone** (`h08` ← `h09`, `h10`, `h11`, all on the shared
SBS-refit stack) asks whether per-sample exposures are causally interpretable (`h08`), reproducible
(`h09`), confounded by treatment (`h10`), and sharpenable with indels (`h11`). `h01` straddles both — its
contamination concern motivates the signature QC work and supplies a confounder class to the ranking
work.

## Research fronts

Ranked across active hypotheses by uncertainty density, recent activity, and explicit task priority:

1. **Repair-or-retire the `h08` positive-control gate** *(from `h08`)* — the single highest-leverage
   decision: a repaired pre-registration fixing the UV proxy and lung burden-dominance, versus
   accepting `[?]` and limiting to scoped exploratory work (task:t205 framed both paths). Gates all
   downstream discovery.
2. **External validation of the dNdScv ranking** *(from `h02`)* — task:t171 (IntOGen 2024 + DepMap),
   the highest-priority remaining check, blocked on data acquisition.
3. **The decisive `h03` length-attention regression** *(from `h03`)* — task:t129 / task:t170; the
   headline `beta_length` is the hypothesis's whole point and still unmeasured.
4. **First `h09` cross-study reproducibility pass** *(from `h09`)* — task:t212, the only task scoped
   directly to `h09`; turns ready infrastructure into a result.
5. **TTN residual mechanism** *(from `h02`)* — task:t153 (CFS overlap) + task:t147 (hypermutator-
   stratified dNdScv) after the RT null.
6. **`h10` next step** *(from `h10`)* — either a GLASS-specific clinical-timing audit or external
   treatment-rich WES/WGS acquisition to obtain a second `q027` patient substrate.
7. **`h01` contamination first quantitative pass** *(from `h01`)* — task:t127 (blocked), the per-gene
   rate comparison before/after spectra subtraction.
8. **`h11` indel-availability census** *(from `h11`)* — task:t188, prerequisite gate, not started.

**Knowledge Gaps (rollup).** A demanding-vs-covered scan over project topics surfaced one gap:

| Topic | Coverage | Demand | Gap | Hypotheses |
|---|---|---|---|---|
| topic:clinical-translational-signatures | 0 | 2 | 2 | `h08`, `h10` |

`topic:clinical-translational-signatures` is referenced by question:0024-treatment-exposed-cohort-chemotherapy-signature and question:0027-does-excluding-treatment-signature-high-samples (both in
the treatment-signature arm) but has no project literature coverage — the clearest near-term
background-research target.

## Candidate frames

**`h04` — MHN pathway ordering (candidate).** Proposes that cross-sectional cBioPortal/GENIE data
contain enough joint-distribution signal for Mutual Hazard Networks (the Schill 2024 observation-
event formulation, implemented by Vocht 2026) to recover a directed intrinsic-mutator → lineage-
driver → checkpoint-loss progression at the Sanchez-Vega pathway level. No project-internal result
yet bears on its three propositions. Promotion is gated on a VAF availability audit (task:t133), a
primary-method check that the observation-event correction survives panel-specific missingness, and
a simulation-calibration pass recovering ≥70% of injected pathway edges (task:t152). The framing
discussion already flags that the naive mutator-phenotype prediction is partly wrong unless
MMR/POLE/POLD1 are separated from the late, expansion-permitting TP53 event.

**`h05` — healthy somatic-background atlas (candidate).** Generalizes `h01`'s within-sample contamination
frame to a cross-tissue null: that healthy somatic mutation rates vary >2 orders of magnitude and
that substituting a meta-analyzed normal null shifts cBioPortal driver frequencies in calibrated,
tissue-specific ways. The Li 2021 body-map (liver highest, pancreas lowest) is the closest anchor for
the >2-OoM claim but rests on five donors and needs clone-size corrections. Data harmonization across
heterogeneous normal-tissue cohorts is the principal obstacle; promotion is gated on a feasibility
audit (task:t150), ≥6 tissues at age-stratified scale, and a pre-registered single-tissue pilot
(task:t114 + task:t151). External-data tasks are blocked, including GTEx controlled-access (task:t169,
blocked on institutional affiliation).

**`h06` — pre-malignant n-1 driver carriage (candidate).** The empirical sibling of `h04`: rather than
inferring ordering probabilistically, it uses directly observed pre-malignant-vs-invasive cohorts to
test whether pre-malignant lesions already carry ≥80% of same-lineage invasive drivers, with a small
checkpoint-enriched late-stage residual. Supporting literature (Martincorena et al. [@Martincorena2018], Lee-Six et al. [@LeeSix2018]) is
consistent but unanalyzed against cBioPortal data. The hypothesis is fully blocked behind a pre-
malignant cohort audit (task:t156); if fewer than three cancer types reach n≥30 pre-malignant samples,
P1 is likely untestable within current scope, and the pipeline's SNV/indel-only design makes
CNA-driven pre-malignant events (e.g., IgH rearrangements, Barrett's chromosomal instability)
invisible.

## Emergent threads

Beyond the per-hypothesis arcs, seven resolver questions bridge two or more hypotheses — the
load-bearing connective tissue between the ranking backbone (`q011`, `q014`) and the signature backbone
(`q020`, `q021`, `q024`) — and a small, coherent orphan population sits off the spine. The standout is a
**contamination-QC spine** (orphan question `q009` plus four SBS1/LRR diagnostic interpretations) that a
proposed candidate hypothesis **`h07`** would absorb once WGS inputs are ingested; the test is currently
structurally unpowered on panel data per `synthesis:0004-emergent-threads-cbioportal` (MSK-IMPACT
covers only ~20.7 kb of late-replicating territory, 23:1 CE:CL). See
`doc/reports/synthesis/_emergent-threads.md` for the full bridge map and orphan inventory (**orphan
question count: 1**; orphan interpretations: 6).
