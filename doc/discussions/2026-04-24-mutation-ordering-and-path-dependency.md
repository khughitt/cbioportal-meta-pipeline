---
id: "discussion:2026-04-24-mutation-ordering-and-path-dependency"
type: "discussion"
title: "Mutation ordering and path dependency — can we detect A→B asymmetries in cBioPortal data?"
status: "active"
source_refs: []
related:
  - "task:t078"
  - "topic:co-occurrence-and-mutual-exclusivity"
  - "search:2026-04-13-cooccurrence-mutual-exclusivity-methods"
created: "2026-04-24"
updated: "2026-04-24"
focus_type: "approach"
focus_ref: "mutation ordering / path dependency in cross-study mutation data"
mode: "standard"
---

# Discussion: Mutation ordering and path dependency

## Focus

Can we detect asymmetric **ordering** signals between gene mutations — i.e. evidence that
`A → B` is more common than `B → A` across patients — from the aggregated cBioPortal /
GENIE data this project already assembles? The user's generating intuition is the
**mutator-phenotype** hypothesis: DNA-repair failures should be selected early because
they raise the per-generation supply of *all* subsequent driver variants, so repair-gene
mutations should appear upstream of immune-evasion, growth, and apoptosis-evasion
mutations. A broader framing is **canalization / path dependency**: the first few mutations
in a lineage constrain which later mutations are accessible or advantageous.

Four concrete sub-questions were asked:

1. **Detection** — can we *robustly* recover ordering from cross-sectional data?
2. **Specific pairs** — which gene pairs should show the strongest asymmetries?
3. **Biology** — do the resulting orderings make mechanistic sense?
4. **Longer chains** — is there evidence for `A → B → C` path-dependent biases beyond pairs?

## Current Position

The project has no ordering/temporal work in scope today. `specs/research-question.md`
frames the work around **static** gene × cancer frequency structure; the pipeline emits
per-study gene × cancer counts/ratios, gene × gene correlation matrices, and gene/cancer
clusters. Task `t078` plans cross-study **co-occurrence / mutual exclusivity** (DISCOVER /
WeSME / Stouffer), but that is a *symmetric* association test — it cannot distinguish
`A → B` from `B → A`.

Key state facts that constrain any ordering analysis:

- **Cross-sectional bulk MAFs only.** We have one biopsy per patient in nearly every
  study, not longitudinal biopsies and not multi-region. Order is therefore not
  directly *observed* — it has to be *inferred* from the joint distribution of binary
  mutation calls (and, if retained, VAFs) across many patients.
- **VAF is not carried through the pipeline.** `convert_to_feather.py` emits one row per
  gene × sample presence call; tumor/normal allele-count columns are dropped. Any
  clonal-ordering work would need a pipeline addition to retain `t_alt_count` /
  `t_ref_count` (or the precomputed `tumor_f` / VAF column) and, ideally, a CCF
  (cancer-cell-fraction) estimate that corrects for purity and local copy number.
- **Panel heterogeneity.** MSK-IMPACT and GENIE panels cover 341–505 genes; a gene
  absent from a panel is not the same as wild-type. Any ordering method on panel data
  has to condition on *callability* per sample (this is the same correction needed for
  co-occurrence — `t078`).
- **Known confounders already flagged in the project.** Clonal hematopoiesis
  contamination (`topic:clonal-hematopoiesis-contamination`, `t087`) inflates DNMT3A /
  TET2 / ASXL1 / PPM1D / TP53 as apparent "early" events because CH variants have
  high apparent tumor VAF; normal-tissue contamination in esophageal / breast (`q001`,
  `q002`) has the same effect. Any ordering inference that reads DNA-repair genes as
  early must be hardened against these.

## Critical Analysis

### What "ordering" means when you only have snapshots

The central identifiability issue: given a set of tumors with mutation sets
`S_i ⊆ {genes}`, there are several different signals one could call "order":

1. **Occurrence order within a tumor (clonal vs subclonal).** Requires VAF/CCF. Higher
   CCF → earlier, in a single tumor. This *is* directly temporal, and is the dominant
   signal used by PCAWG (Gerstung 2020, *Nature* 578:122) to reconstruct pan-cancer
   chronologies. But it depends on retaining allele counts and correcting for purity/CNA.
2. **Population-level progression order.** If a lineage must acquire A *before* B to
   reach a fit cancerous state, then tumors with only A should be more frequent than
   tumors with only B. This is the assumption behind **Conjunctive Bayesian Networks**
   (Beerenwinkel 2007), **oncogenetic trees** (Desper 1999), **CAPRI / TRONCO**
   (Caravagna 2016 *PLoS Comput Biol*), and **Mutual Hazard Networks** (MHN — Schill
   2020 *Bioinformatics*). These methods infer directed edges from *only* binary
   presence/absence data across a cohort.
3. **Ordering along subclonal trees.** Requires multi-region or single-cell data.
   Not available in cBioPortal.
4. **Temporal in real time.** Requires longitudinal sampling or age-stratified cohorts.
   Not available outside a few series (e.g. pre/post treatment in MSK).

Only (1) and (2) are plausibly addressable with cBioPortal + minor pipeline work. Both
are indirect and vulnerable to the confounders below.

### Why `A→B >> B→A` asymmetry is not self-evidently causal order

Even if we see the asymmetric frequency inequality `P(A alone) > P(B alone) ∧
P(A,B) ≈ P(A,B)` (the CBN "A precedes B" signature), several non-temporal explanations
produce the same pattern:

- **Selection asymmetry with no temporal constraint.** A-only clones are simply more
  fit than B-only clones (either survive longer to be biopsied, or expand to
  clinically detectable size faster). This gives the same inequality without B needing
  to come after A. CBN-family methods cannot distinguish this from true ordering
  without additional assumptions (commonly: no reversal, constant hazards).
- **Differential detection.** A is covered by more panels / better assays than B, so
  A-only samples are over-ascertained. Panel-heterogeneity correction is essential.
- **Cancer-type mixing.** If A is common in one histology and B in another, pooling
  across the combined cohort creates apparent A→B asymmetry that is actually
  between-histology composition. This is the Simpson's-paradox failure mode for
  pan-cancer ordering — it is why PCAWG chronologies are reported *per histology*.
- **Mutational-signature coupling.** MMR-deficient tumors acquire indels/SNVs at a
  very different rate than MMR-proficient ones. If A is an MMR gene, a cohort of
  A-mutated tumors will have many more "downstream" mutations than an MMR-proficient
  cohort *regardless of causal order* — simply because the clock ran faster. The
  hypermutator annotation (`t081`) and signature exposures (`t111`) already quantify
  this; ordering analyses must stratify on them.
- **Clonal hematopoiesis and normal-tissue contamination.** CH variants have
  near-100% VAF in blood-contaminated unmatched-normal tumors, so they will always
  look "earliest" if VAF-based clonality ordering is used naively. `t087` (graded
  `ch_contamination_prob`) and the CH-priority-gene flag partially fix the mean-ratio
  tables but do not protect a VAF-based clonality estimator.
- **Apparent clonality inflated by CNA.** A heterozygous mutation in a region with
  LOH reads as ~100% VAF — it looks clonal even if it arose late, in one subclone,
  with the other allele lost afterwards. Correcting this requires CNA data, which the
  pipeline explicitly excludes (`out_of_scope`, and `t055` is deferred).

### The mutator-phenotype prediction specifically

The user's specific hypothesis — repair gene mutations precede non-repair driver
mutations — has mixed empirical support in the existing literature and is not a free
win even if an ordering method works:

- **Supporting.** Lynch-syndrome-like MMR deficiency in CRC is overwhelmingly an early
  event. MMR-deficient / POLE tumors carry >10× the TMB of proficient counterparts,
  consistent with repair-first. `t081` will flag these as hypermutators.
- **Contradicting for TP53 specifically.** TP53, the poster-child repair/checkpoint
  gene, is often a **late** clonal-expansion event in many solid tumors (breast,
  CLL, MDS, pancreatic progression from IPMN). PCAWG (Gerstung 2020) puts TP53
  among the *late* pan-cancer events on average, with APC, KRAS, and several
  chromatin remodelers ranked earlier. So "repair gene → immune-evasion gene"
  collapses if "repair" includes TP53: TP53 is not usually mechanistically acting
  as a mismatch repair accelerator; it is acting as a checkpoint whose loss
  *permits* expansion of clones that already accumulated mutations elsewhere.
  This is exactly the distinction between **intrinsic mutator** (MMR, POLE) and
  **extrinsic permissiveness** (TP53, cell-cycle checkpoints).
- **Implication.** The ordering question needs to be asked at the **pathway** level,
  not the "DNA repair" bag-of-genes level. Split the repair label into
  (mismatch repair / HR / NER / BER / polymerase proofreading / checkpoint /
  damage sensing). Expect MMR / POLE / POLD1 to precede most things in their
  cancer types; expect TP53 to follow APC in CRC, follow HER2 amp in breast, etc.
  This is also what Sanchez-Vega 2018 pathway framing (already in the project —
  `process_sanchez_vega_pathways.py`) supports.

### Path dependency / canalization

The framing as canalization is interesting but operationally reduces to **conditional
prevalence**: `P(B | A, cancer type, signature context) vs P(B | ¬A, ...)`. Once the
conditioning is right, path dependency is indistinguishable from "strong context-specific
positive selection" on the static data — i.e. it is exactly the signal that co-occurrence
methods (DISCOVER / SELECT / WeSME in `t078`) already try to detect, plus a *direction*.
The direction is the new thing. MHN is the method that adds direction on top of what
DISCOVER does: it is essentially "DISCOVER with an explicit CTMC generative model."

Strong recommendation: if we pursue this, frame it as **MHN-on-top-of-DISCOVER** so the
two workstreams share the sample-specific-background-rate null and the panel callability
correction. Do not invent a bespoke ordering statistic.

## Evidence Needed

To answer each sub-question:

- **Detection robustness.** Need: (i) per-sample VAF or CCF columns retained from MAFs;
  (ii) per-sample callable-gene mask (from `build_panel_callable_sizes`, extended to
  per-gene); (iii) simulation study — generate synthetic tumors from a known MHN /
  CBN, subsample to the same panel + cohort-size distribution as the real data, and
  check whether we recover the known edges. Without this, any asymmetry we find is
  un-calibrated.
- **Specific pairs.** Need PCAWG and REVOLVER chronology tables as ground truth to
  compare against. If we recover their known per-histology pairs (APC→KRAS→TP53 in
  CRC; TP53→PIK3CA in breast; STK11→KEAP1 in LUAD; BRAF→TERT in thyroid), the method
  is working. If not, it is not.
- **Biology.** Pathway-level aggregation via `process_sanchez_vega_pathways.py`
  (already in project) — ordering at the RTK/RAS, Wnt, p53, cell-cycle, TGFβ, Notch,
  Myc, Hippo, NRF2, PI3K, genome-integrity pathway level is likelier to be
  biologically interpretable and statistically powered than gene-pair ordering at
  scale.
- **Longer chains.** CBN / MHN fit arbitrary-length DAGs natively but power drops
  steeply beyond triples for realistic cohort sizes (~10³–10⁴ samples per histology).
  Expect to be able to talk about triples, not quintuples.

## Prioritized Follow-Ups

| Priority | Action | Why now | Dependencies |
|---|---|---|---|
| P2 | New literature search: **temporal / ordering methods for bulk cross-sectional cancer data** — MHN (Schill 2020), CBN (Beerenwinkel 2007), CAPRI/TRONCO (Caravagna 2016), REVOLVER (Caravagna 2018), HINTRA, PMCE, SCITE-as-context, PCAWG chronology (Gerstung 2020 *Nature* 578:122). Deliverable: `doc/searches/YYYY-MM-DD-mutation-ordering-methods.md` with method × assumption table and recommendation. | Decides whether this is a method-selection exercise or a novel-methods exercise. Likely the former (MHN is a strong fit). | none |
| P2 | New question file: `q012-mutation-ordering-cross-sectional-inference.md` — restate the four sub-questions as a project question with required evidence and stop-rule (per template). | Canonicalises the discussion into a tracked question so it can be prioritised against the other open questions. | none |
| P2 | Feasibility spike: audit what fraction of the current studies retain VAF (`tumor_f` / `t_alt_count`+`t_ref_count`) in their MAFs *before* `convert_to_feather.py` drops them. One-afternoon task: read each MAF header, tally. Output: `doc/audits/YYYY-MM-DD-vaf-availability-audit.md`. | Hard gate on the whole workstream. If <50% of studies carry VAF, clonal-ordering is off the table and we are restricted to CBN/MHN-style population-level inference. | none |
| P3 | Pipeline addition: extend `convert_to_feather.py` to retain `t_alt_count`, `t_ref_count`, and precomputed `tumor_f`/VAF per variant in a new `studies/{id}/mut/variants.feather` (or columns on the existing variant-level feather). Required for any clonality-based ordering work and cheap to add. | Unblocks both this line of work and any future CCF / signature-per-sample / driver-evolution analyses. | VAF-availability audit above |
| P3 | If `t078` is implemented first, follow with an MHN fit per histology using exactly the same sample-specific-background-rate null that DISCOVER uses. Compare recovered edges to Gerstung 2020 pan-cancer chronology Table 1 as a calibration test. | Shares infrastructure with `t078`; the only new code is the CTMC fit. Produces *directed* companion to co-occurrence results. | `t078` (co-occurrence pipeline), VAF retention optional |
| P3 | Pathway-level ordering as the **primary** reporting granularity (Sanchez-Vega 10-pathway groups), with per-gene ordering as a secondary drill-down. Explicit stratification by hypermutator / signature class from `t081` / `t111`. | Answers the user's biology question in a form that is interpretable and powered. Mitigates the "TP53 is not really a repair gene" failure mode. | pathway annotations (already in project), `t081`, `t111` |
| P4 | Defer longer-than-triple chains until calibration on pairs + triples is done. | Power drops steeply; no point chasing long chains before pair-level is validated. | pair / triple results |

## Synthesis

The question is scientifically real and has a dedicated methods literature that already
addresses it — **Mutual Hazard Networks (Schill 2020)** is essentially the method
designed for what the user wants to do, using exactly the data we have (cross-sectional
binary mutation calls). This is a method-selection exercise, not a novel-methods
exercise.

However, three things are true simultaneously:

1. Ordering asymmetry on cross-sectional data is **under-identified** — the inequality
   `P(A) > P(B) ∧ P(A,B)` is consistent with both "A is temporally upstream of B" *and*
   "A-only clones are simply fitter than B-only clones." CBN/MHN resolve this only
   under strong assumptions (no reversal, constant hazards) that are arguably violated
   in cancer.
2. The project's existing known confounders — **CH contamination, normal-tissue
   contamination, panel heterogeneity, signature / hypermutator stratification, cancer-
   type mixing** — all bias ordering estimators in the same direction they bias
   frequency estimators, but more severely, because ordering is a higher-moment
   statistic. Any ordering analysis has to reuse and extend the corrections `t067`,
   `t081`, `t087`, `t111` already build.
3. The specific biological intuition — "repair genes first, immune evasion last" — is
   partially correct (MMR / POLE) and partially wrong (TP53 is often late). The
   correct framing is **intrinsic mutators (MMR, POLE, POLD1) precede everything;
   checkpoint and expansion-permitting genes (TP53, RB1) follow lineage-specifying
   drivers.** That distinction requires pathway-level aggregation, not bag-of-repair-
   genes aggregation.

**Recommendation.** Do not commit project effort to this before `t078` is done. When
it is, add an MHN fit on the same samples × same genes × same callability mask as
`t078`, stratified per histology and per hypermutator class, reported primarily at
Sanchez-Vega pathway level with gene-level as a drill-down. Calibrate against PCAWG
(Gerstung 2020) chronology before reporting anything novel. Start by filing `q012` and
running the VAF-availability audit so we know which regime (clonality-aware vs
population-only) is even available to us.
