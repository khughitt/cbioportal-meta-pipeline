---
type: discussion
title: "Is there a preferred ordering among the hallmarks of cancer \u2014 and can\
  \ the hallmarks themselves be inferred from data rather than human labels?"
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: discussion:0007-hallmark-ordering-and-data-driven-modules
source_refs:
- paper:Gourmet2024
- paper:RaphaelVandin2015
- paper:Iorio2018SLAPenrich
- paper:Deshpande2026
- paper:Wang2025a
related:
- hypothesis:0004-mhn-pathway-ordering
- question:0012-mutation-ordering-cross-sectional-inference
- discussion:0002-mutation-ordering-and-path-dependency
- discussion:0006-age-of-onset-and-multistage-mutation-requirement
- theme:0003-temporal-structure-of-carcinogenesis-order-count-and-timing-of-the
- topic:co-occurrence-and-mutual-exclusivity
- task:t078
focus_type: approach
focus_ref: ordering of cancer hallmarks; data-driven (label-free) inference of hallmark-like
  mutation modules
mode: standard
---

# Discussion: Hallmark ordering and data-driven modules

## Focus

Two linked questions, raised as a coarser-grain extension of the gene/pathway ordering
work (`question:0012`, `hypothesis:0004`):

1. **Is there a preferred ordering among the *hallmarks* of cancer?** I.e. do the gene/
   pathway sets associated with each hallmark tend to be acquired in a characteristic
   sequence (some hallmarks "enabling" and therefore early), both pan-cancer and
   conditioned on cancer type — and are there clusters of cancer types with more coherent
   orderings?
2. **Can the hallmark→mutation mapping be done from first principles / from data**, rather
   than relying on human- or AI-assigned hallmark labels — and, more ambitiously, can we
   *infer* hallmark-like gene/pathway modules as latent structure and ask whether they
   recapitulate the canonical hallmarks or carve the space differently?

The user's generating intuition: mutations that raise the mutation supply (genome
instability) should be selected early; immune evasion may be late. Major caveat the user
flagged: the "hallmarks" are a human-imposed discrete simplification of a continuous,
heterogeneous disease space — convenient, but we should not over-constrain ourselves to
the particular magic set the field currently favors.

## Current Position

**This is not green field — the specific experiment was run recently** (`paper:Gourmet2024`,
"The temporal evolution of cancer hallmarks", bioRxiv 2024.01.21.576566 / Research Square
rs-5499335). It ordered the hallmarks across **>10,000 untreated primary tumors + >8,000
healthy tissues** (9,484 TCGA / 7,584 GTEx) and reported a **common evolutionary trajectory
in 27/32 cancer types: genome instability first → … → immune evasion last** (angiogenesis /
growth / immortality / metabolism early; cell-death-evasion / proliferation / metastasis
late), with widespread positive selection in tumors and negative selection in normals.
Melanomas (uveal + skin) were the exception — strong environmental mutagenesis disrupts the
common path. Clustering patient trajectories gave **two prognostic clusters (early vs late
genomic instability)**. Critically, their **order proxy was allele frequency (clonality) +
selective advantage (dN/dS-style)**, not patient age, and their hallmark→gene mapping used
**curated hallmark gene-set labels**.

**A caveat from `paper:Gourmet2024` that directly concerns this project:** their headline
ordering uses raw variant allele frequency; a **CCF-based sensitivity analysis moves genome
instability to a *mid-order* position**. That is exactly the VAF→CCF (purity/copy-number)
correction the project already flagged as load-bearing for any clonality ordering
(`question:0012`, `t133` VAF audit, `t055` deferred CNA) — so even this prior art's
genome-instability-first headline is sensitive to the correction we would have to make
ourselves. It strengthens, not weakens, the case that the *order axis* must be CCF-corrected
clonality / MHN rather than raw VAF or age.

This result is, at the hallmark grain, the same claim `hypothesis:0004` makes at the
Sanchez-Vega pathway grain: **intrinsic genome-instability / mutator events precede
lineage drivers, which precede checkpoint / late events.** Genome-instability-first is
also consistent with its 2011-update status as an *enabling characteristic* rather than a
core hallmark. → The temporal-evolution paper is therefore best treated as an **external
calibration target / prior art** for h04, not a separate workstream.

For the **label-free module question**, the relevant methods literature already exists:

- **`paper:RaphaelVandin2015`** ("Simultaneous Inference of Cancer Pathways and Tumor
  Progression from Cross-Sectional Mutation Data", J Comput Biol; RECOMB 2014) — jointly
  infers mutually-exclusive gene *modules* **and** their progression order from snapshot
  mutation data via ILP. This is almost exactly the proposed pipeline (discover modules
  label-free, then order them) in one method.
- **`paper:Iorio2018SLAPenrich`** — pathway-level somatic-mutation enrichment mapped onto
  canonical hallmarks across cancer types; the curated pathway→hallmark bridge if/when we
  want to *interpret* data-driven modules against the human labels.
- **`paper:Deshpande2026`** ("Cancer Attractor States … Embryonic Origin and Cancer
  Hallmarks") — **unsupervised** clustering (Jaccard t-SNE + K-means) over **MSK-MET**
  (n≈25,775, the MSK-IMPACT metastatic panel cohort — directly comparable to this project's
  panel data) finds stable pan-cancer attractor states; integrates embryological origin (EO)
  with hallmark-related mutations (HRM). Caveat: *semi*-label-free — hallmark labels still
  enter via the HRM feature construction; and it models **states, not ordering**. The EO
  (cell-of-origin) axis aligns with the project's mandatory per-histology framing.
- **`paper:Wang2025a`** ("Data-driven … hallmark networks", npj Syst Biol Appl 2025) — a
  coarse-grained hallmark-GRN + stochastic-differential-equation dynamical model where
  network topology reconfigures *before* hallmark-level shifts. **Adjacent modality**
  (expression/GRN dynamics, not somatic-mutation ordering): useful for the "hallmarks as
  coarse-grained modules / critical transitions" framing, not directly transferable to our
  mutation data.

## Critical Analysis

### Average patient age is the wrong primary order proxy

The user's step-2 proposal — "for each cancer type, compute average age associated with
each mutation as a proxy for order" — is **weak and heavily confounded** as a measure of
*within-lineage* acquisition order, and should not be the primary axis:

- **Age-dependent passenger accumulation.** Older patients carry more mutations regardless
  of order (clock-like SBS1/SBS5). "Found in older patients" ≠ "acquired late in the
  tumor's lineage." This biases the proxy toward calling *everything* in older-skewed
  histologies "late".
- **Cancer-type age structure (Simpson's paradox).** Mutations common in young-onset
  cancers (e.g. some sarcomas, testicular, certain leukemias) inherit a low mean carrier
  age that reflects *which disease* they mark, not *when* in that disease they arise. This
  is the same pooling hazard that forces per-histology analysis everywhere else here.
- **Germline / hereditary early-onset** (Lynch, Li-Fraumeni, etc.) pulls specific genes'
  carrier-age down for reasons orthogonal to somatic order.
- **Detection / screening / stage-at-sequencing** modulate age at biopsy independently of
  biology — the same diagnostic-cohort collider that `paper:Schill2024` models for
  ordering.

What average age *does* give is a legitimate **population-epidemiological association**
(which alterations track younger onset) — interesting, but a **different question** from
acquisition order. **Recommendation:** keep clonality (VAF/CCF, gated on the `t133` VAF
audit) and MHN as the order axes; demote age to an **orthogonal covariate / falsification
check** ("does the clonality/MHN ordering also show the expected age gradient?"), never the
primary ordering signal.

### Label-free hallmark modules via mutual exclusivity + MHN

The principled route to "hallmarks from data" exploits a known regularity: **within a
pathway/hallmark, driver mutations tend to be mutually exclusive** (one hit suffices to
perturb the module), while **across modules they co-occur**. So:

1. **Association substrate — not yet modules.** `t078` (DISCOVER / SELECT / WeSME) supplies
   *pairwise / set-level* co-occurrence and mutual-exclusivity **tests** — a signed
   association structure, not a global partition. **Module inference is a distinct, added
   step**: assemble those pairwise signals into a partition via an explicit module-discovery
   method — `paper:RaphaelVandin2015`'s PLPM/ILP joint module+progression model, WeSME-style
   mutually-exclusive module assembly, or clustering over the signed association graph. Only
   the *output* of that step is the set of data-driven "hallmark-like" modules. Keep the two
   layers separate: association substrate (`t078`) ≠ module inference (added).
2. **Order the modules** with the same per-histology MHN fit as `h04` (observation-event
   MHN, `paper:Vocht2026` / `paper:Schill2024`).
3. **Annotate post hoc** — enrich each data-driven module against curated hallmark / CHG /
   `paper:Iorio2018SLAPenrich` pathway sets — to ask the user's real question: **do the
   inferred modules recapitulate the canonical hallmarks, or carve the space differently?**
   This is the direct, data-first answer to the "don't over-constrain on the magic discrete
   set" caveat: the human labels become a *validation overlay*, not an input.

### Same confounders as h04/q012, only more severe

Hallmark/module ordering is a higher-moment statistic than frequency, so **every confounder
already catalogued for `q012` / `h04` applies, harder**: cross-sectional
under-identification (`P(A)>P(B)∧P(A,B)` is consistent with both order *and* pure fitness
asymmetry); diagnostic-cohort collider bias (`paper:Schill2024`); clonal-hematopoiesis and
normal-tissue contamination inflating apparent-early events (`topic:clonal-hematopoiesis-
contamination`, `t087`); panel callability (`t078`); mandatory hypermutator / signature
stratification (`t081` / `t111`); and strict per-histology fitting to avoid Simpson's
paradox. Aggregating to module/hallmark grain *helps* power and stability (absorbs panel
heterogeneity) but does not remove these.

## Relationship to existing entities

- **Coarser-grain sibling of `h04`.** Recommend implementing hallmark ordering as (a) an
  aggregation/relabeling layer over h04's per-histology pathway-MHN using a hallmark
  grouping, reported **alongside** (b) a data-driven module grouping that *tests whether the
  hallmark partition is even the right one*. Not a parallel pipeline.
- **`q012`** is the inference-feasibility question; this discussion is the
  hallmark-grain + label-free-module framing of the same machinery.
- **`t078` / `t137`**, once production-wired — `t137` ("t078 SELECT pipeline integration
  wiring") still needs the production prerequisites (`gene_sample_long.feather`,
  `samples_annotated.feather`, schema fixes) — supply the *corrected co-occurrence /
  mutual-exclusivity substrate* and the callability null shared with the MHN fit. That is the
  substrate *from which* modules could be inferred (via the separate module-discovery step
  above), **not** the modules themselves.
- The temporal-evolution paper's genome-instability-first / immune-evasion-last result is a
  **free external calibration check** for any ordering we recover.

## Evidence Needed

- Corrected co-occurrence and mutual-exclusivity outputs are needed before inferring label-free modules; the pairwise association layer is not itself a module partition.
- Per-histology MHN or equivalent ordering fits need CCF/VAF sensitivity checks, hypermutator stratification, and callability correction before any hallmark-order claim is interpreted.
- External calibration should compare inferred module orderings against published hallmark-order results without treating those papers as ground truth.

## Prioritized Follow-Ups

| Priority | Action | Why | Dependencies |
|---|---|---|---|
| ✅ done 2026-06-07 | Summarized all five into `doc/papers/`: `paper:Gourmet2024`, `paper:RaphaelVandin2015`, `paper:Iorio2018SLAPenrich`, `paper:Deshpande2026`, `paper:Wang2025a`. | Establishes prior art + calibration target; some are method blueprints. | — |
| P3 | Add a candidate hypothesis (sibling to h04) framed as a **test, not a foregone result**: *do* data-driven mutual-exclusivity modules ordered by per-histology MHN reproduce a genome-instability-early → immune-evasion-late sequence, and *to what degree* do the inferred modules align with vs. diverge from the canonical hallmark partition? Explicit falsifiers: (i) TP53 / checkpoint dominance places genome-instability **late**, not early; (ii) the ordering is **not robust to CCF correction** (the `paper:Gourmet2024` VAF→CCF discordance reproduced in our data); (iii) modules do not stably map to hallmarks (low partition agreement). | Canonicalizes the *open* question; Gourmet2024 is the calibration prior, not the assumed answer. | this discussion; h04 scoping |
| P3 | When h04's pathway-MHN runs, add a hallmark-grouping aggregation view + a `RaphaelVandin2015`-style data-driven module view as a second grouping; compare orderings. | Delivers the hallmark answer as a thin layer over existing machinery. | h04 (blocked on t078, t133) |
| P4 | Use average age only as an orthogonal covariate / falsification overlay on the recovered ordering (age gradient consistency), never as the primary order proxy. | Captures the epidemiological signal without the confounds of age-as-order. | ordering output |

## Synthesis

`paper:Gourmet2024` **reports a VAF-based preferred ordering** of hallmarks (genome
instability first, immune evasion last, in 27/32 cancer types), which echoes at hallmark
grain what `h04` predicts at pathway grain — **but that headline is sensitivity-dependent**:
their own CCF-based analysis moves genome instability to mid-order. So the defensible claim
is "a preferred ordering is *reported under VAF, pending CCF correction*," not the
unqualified "there is a preferred ordering." The novel, defensible contribution
for this project is **not** re-deriving that ordering with a weak age proxy, but (i)
calibrating h04 against it, and (ii) **inferring hallmark-like modules label-free**
(mutual exclusivity + MHN, à la `paper:RaphaelVandin2015`) and asking whether the data's
own partition matches the human hallmark set — directly honoring the "don't over-constrain
on the magic discrete set" caveat. Fold into the h04/q012 orbit; do not start a parallel
ordering workstream; reuse every confounder correction already scoped for q012.
