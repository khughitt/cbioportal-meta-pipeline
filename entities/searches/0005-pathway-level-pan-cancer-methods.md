---
type: search
title: Pathway-level pan-cancer analysis methods (beyond Sanchez-Vega 2018)
status: active
created: '2026-04-14'
updated: '2026-04-14'
id: search:0005-pathway-level-pan-cancer-methods
---

# Pathway-level pan-cancer analysis methods — 2026-04-14

## Search Focus

Map the methodological landscape for **pathway-level pan-cancer analysis of somatic mutation
data**, going beyond Sanchez-Vega et al.'s 10-oncogenic-signaling-pathways treatment [@SanchezVega2018] (which is
already the project seed reference). Primary motivations:

1. The pipeline currently operates at the **gene × cancer × study** resolution. A pathway
   layer (Reactome / KEGG / PID / Hallmarks / Sanchez-Vega-10 / NCI-PID / PCAWG
   consensus-pathways) would let us test whether gene-level associations that are weak
   individually converge into **pathway-level** signal that is robust across studies — directly
   relevant to the pipeline's research question about which gene-cancer associations recur.
2. Pathway-level interpretation is the natural complement to gene-level clustering (we already
   emit `gene_cancer` clusters; a pathway-level rollup would connect the clusters to
   mechanism).
3. The co-occurrence / mutual-exclusivity work queued in `t078` benefits directly from a
   pathway layer — most of the state-of-the-art methods (MEMo, Mutex, SLAPenrich, HotNet2,
   ActivePathways) are pathway-aware by design.

Scope covers: **(a) pure frequency-based pathway enrichment** (GSEA, g:Profiler, SLAPenrich,
ActivePathways); **(b) network-based driver / pathway discovery** (HotNet2, Hierarchical
HotNet, NetBox, NetSig, Network-Based Stratification, TieDIE, NBDI, CanIsoNet);
**(c) integrative mutation + expression pathway methods** (PARADIGM); **(d) compendium /
benchmark efforts** (IntOGen, PCAWG pathway-and-network, 2022 Brief Bioinform benchmark).

Out of scope for this pass: per-gene driver significance methods that do not have a pathway
rollup (MutSigCV, dNdScv — already covered under `topic:hotspot-based-driver-detection` and
`topic:cancer-driver-genes`); signature-level methods (already covered in
`topic:mutational-signatures`); methods specific to non-coding / regulatory mutations
(tangential to this pipeline's scope).

## Query Set

1. **Broad conceptual** — `pathway enrichment cancer somatic mutation pan-cancer` (OpenAlex);
   `"pathway enrichment"[TI] cancer somatic pan-cancer` (PubMed).
2. **Methods-anchor lookup** — named-method queries for: SLAPenrich (Iorio), ActivePathways
   (Paczkowska/Reimand), HotNet2 (Leiserson/Raphael), Hierarchical HotNet (Reyna/Raphael),
   NetSig (Horn), PARADIGM (Vaske), Network-Based Stratification / NBS (Hofree/Ideker),
   NetBox (Cerami), TieDIE (Paull), PCAWG pathway-and-network [@Reyna2020Pathway], IntOGen
   compendium (Martinez-Jiménez 2020).
3. **Pan-cancer pathway-compendium / integrative efforts** — `"pan-cancer" pathway "whole
   cancer genomes"`; `"Hallmarks of Cancer" pathway enrichment somatic mutation pan-cancer`.
4. **Benchmark / review** — `benchmark pathway cancer driver method comparison`;
   `review pathway-level pan-cancer mutation analysis`.
5. **Recent window (2022-2026)** — `"pan-cancer" pathway analysis 2022:2026[PDAT]`;
   `pathway cancer driver 2024 integrative mutation`.

## Sources and Run Metadata

- Primary sources: **OpenAlex** `/works?search=...` (candidate expansion) and **PubMed**
  E-utilities (`esearch` + `esummary`) for precise named-method resolution; **WebSearch**
  fallback for specific title+author lookups.
- Retrieved: 2026-04-14.
- Shared runtime (`uv run science-tool literature search …`): **not available** — the
  project's `science-tool` install does not expose a `literature` subcommand. Direct APIs
  used via `WebSearch`, plus LLM-knowledge seeding for named methods.
- Candidates retrieved (across all query variants, after dedupe): ~45.
- Shortlisted records in this report: **20** (6 `Core now`, 10 `Relevant next`, 4
  `Peripheral monitor`).
- Dedup order: DOI → PMID → normalized title+year.

## Ranked Results

| # | Citation (short) | Year | IDs | Tier | Why it matters |
|---|---|---|---|---|---|
| 1 | Reyna MA, Haan D, et al. "Pathway and network analysis of more than 2500 whole cancer genomes." *Nat Commun* [@Reyna2020Pathway] | 2020 | PMID: 32024854 / DOI: 10.1038/s41467-020-14367-0 | **Core now** | **PCAWG flagship pathway/network analysis.** Applies 7 distinct methods (ActivePathways, CanIsoNet, Hierarchical HotNet, hypergeometric, induced-subnetwork, NBDI, SSA-ME) to 2,583 WGS cancers across 27 tumor types. Identifies 93 genes / modules with non-coding mutation convergence. Canonical reference for *pan-cancer pathway analysis done well*; demonstrates the ensemble-of-methods pattern we should emulate. |
| 2 | Paczkowska M, Barenboim J, Sintupisut N, et al. "Integrative pathway enrichment analysis of multivariate omics data." *Nat Commun* [@Paczkowska2020] | 2020 | PMID: 32024846 / DOI: 10.1038/s41467-019-13983-9 | **Core now** | **ActivePathways** — integrates multiple evidence streams (gene-level *p*-values from different datasets / modalities) into a single pathway enrichment via statistical data fusion. Directly applicable to our cross-study setting: each study's gene-level evidence becomes one input column. Open-source R package (reimandlab/ActivePathways). |
| 3 | Leiserson MDM, Vandin F, Wu HT, et al. "Pan-cancer network analysis identifies combinations of rare somatic mutations across pathways and protein complexes." *Nat Genet* [@Leiserson2015] | 2015 | PMID: 25501392 / DOI: 10.1038/ng.3168 | **Core now** | **HotNet2 pan-cancer application.** 16 significantly mutated subnetworks across 3,281 TCGA samples / 12 cancer types. The canonical pan-cancer network-based result; HotNet2 itself is the diffusion-based algorithm for finding mutated subnetworks in PPI graphs and is the most-cited pathway/network pan-cancer method. |
| 4 | Iorio F, Garcia-Alonso L, Brammeld JS, et al. "Pathway-based dissection of the genomic heterogeneity of cancer hallmarks' acquisition with SLAPenrich." *Sci Rep* [@Iorio2018SLAPenrich] | 2018 | PMID: 29713020 / DOI: 10.1038/s41598-018-25076-6 | **Core now** | **SLAPenrich** — Sample-population Level Analysis of Pathway enrichments. Accounts for per-sample mutation rate, gene exonic length, and mutual exclusivity *explicitly in the null model*. Does not require a pathway to be individually mutated in a sample — a single-gene hit counts. Directly addresses the gene-length normalization already in our pipeline. R package on GitHub. |
| 5 | Martínez-Jiménez F, Muiños F, Sentís I, et al. "A compendium of mutational cancer driver genes." *Nat Rev Cancer* [@MartinezJimenez2020] | 2020 | PMID: 32778778 / DOI: 10.1038/s41568-020-0290-x | **Core now** | **IntOGen compendium.** Pan-cancer analysis of ~28,000 tumors across 66 cancer types; integrates 7 driver-detection methods to produce 568 consensus drivers. The reference standard for "what counts as a driver in pan-cancer data", and its methods-ensemble design is the template for how we should aggregate per-method pathway results downstream. Continuously updated at intogen.org. |
| 6 | Horn H, Lawrence MS, Chouinard CR, et al. "NetSig: network-based discovery from cancer genomes." *Nat Methods* [@Horn2018] | 2018 | PMID: 29200198 / DOI: 10.1038/nmeth.4514 | **Core now** | **NetSig.** Integrates PPI networks with 4,742 tumor exomes; corrects for node-degree bias in PPI graphs (hub genes look falsely significant under naive network methods). Predicts 62 new driver candidates; experimentally validates a subset. A concrete template for how to layer a pathway/network prior onto our gene-level counts without degree-bias artifacts. |
| 7 | Reimand J, Isserlin R, Voisin V, et al. "Pathway enrichment analysis and visualization of omics data using g:Profiler, GSEA, Cytoscape and EnrichmentMap." *Nat Protoc* [@Reimand2019] | 2019 | PMID: 30664679 / DOI: 10.1038/s41596-018-0103-9 | Relevant next | **g:Profiler / GSEA / EnrichmentMap protocol.** Standard reference for the pipeline-level pathway enrichment workflow; covers all three layers (enrichment, visualization, curation). Most useful as the "off-the-shelf pathway enrichment" baseline to compare pathway-aware methods against. 1,450+ citations. |
| 8 | Reyna MA, Leiserson MDM, Raphael BJ. "Hierarchical HotNet: identifying hierarchies of altered subnetworks." *Bioinformatics* [@Reyna2018HierarchHotNet] | 2018 | DOI: 10.1093/bioinformatics/bty613 / PMID: 30423088 (not reconfirmed in this note) | Relevant next | **Hierarchical HotNet** — extends HotNet2 to return a hierarchy of subnetwork significance rather than a flat list. Useful when the pathway structure itself is nested (most curated pathway databases are). Already used in Reyna et al. [@Reyna2020Pathway] PCAWG. |
| 9 | Hofree M, Shen JP, Carter H, Gross A, Ideker T. "Network-based stratification of tumor mutations." *Nat Methods* [@Hofree2013NetworkBased] | 2013 | PMID: 24037242 / DOI: 10.1038/nmeth.2651 | Relevant next | **NBS** — foundational method for clustering *patients* by mutation-on-network similarity rather than raw mutation identity; solves the "shared pathway, different genes" problem. Directly relevant to our `summary/mut/clusters/` outputs as an upgrade path. |
| 10 | Vaske CJ, Benz SC, Sanborn JZ, et al. "Inference of patient-specific pathway activities from multi-dimensional cancer genomics data using PARADIGM." *Bioinformatics* [@Vaske2010InferencPatient] | 2010 | PMID: 20529912 / DOI: 10.1093/bioinformatics/btq182 (identifier pairing not reconfirmed in this note) | Relevant next | **PARADIGM.** Per-sample pathway activity inference integrating mutation + expression + copy-number via factor graphs. Requires expression data we don't currently ingest, so deferred — but the canonical reference for per-sample pathway-activity scoring. |
| 11 | Cerami E, Demir E, Schultz N, Taylor BS, Sander C. "Automated network analysis identifies core pathways in glioblastoma." *PLoS ONE* [@Cerami2010AutomateNetwork] | 2010 | PMID: 20169195 / DOI: 10.1371/journal.pone.0008918 (identifier pairing not reconfirmed in this note) | Relevant next | **NetBox.** Pathway module discovery via a PPI seed graph; part of the cBioPortal ecosystem (same lab). Lightweight, documented, and already consumable from the intermediates our pipeline emits. |
| 12 | Vandin F, Upfal E, Raphael BJ. "Algorithms for detecting significantly mutated pathways in cancer." *J Comput Biol* [@Vandin2011AlgorithDetectin] | 2011 | PMID: 21385050 / DOI: 10.1089/cmb.2010.0265 (identifier pairing not reconfirmed in this note) | Relevant next | **HotNet1.** Original heat-diffusion formulation for finding mutated subnetworks in PPI graphs; the methodological precursor to HotNet2. Read for the statistical framing even if HotNet2 is preferred operationally. |
| 13 | Paull EO, Carlin DE, Niepel M, et al. "Discovering causal pathways linking genomic events to transcriptional states using Tied Diffusion Through Interacting Events (TieDIE)." *Bioinformatics* [@Paull2013DiscoverCausal] | 2013 | PMID: 23986567 / DOI: 10.1093/bioinformatics/btt471 (identifier pairing not reconfirmed in this note) | Relevant next | **TieDIE.** Couples mutation-end and expression-end of a pathway via bidirectional diffusion. Useful template if we add expression in a future phase. |
| 14 | Knijnenburg TA, Wang L, Zimmermann MT, et al. "Genomic and molecular landscape of DNA damage repair deficiency across The Cancer Genome Atlas." *Cell Rep* [@Knijnenburg2018GenomicMolecula] | 2018 | PMID: 29617664 / DOI: 10.1016/j.celrep.2018.03.076 (identifier pairing not reconfirmed in this note) | Relevant next | **Pan-cancer DDR pathway landscape.** Concrete example of the pathway-level analysis we want to replicate for additional pathways — shows what a pathway-level pan-cancer result looks like end-to-end. |
| 15 | Iranzo J, Martincorena I, Koonin EV. "Cancer-mutation network and the number and specificity of driver mutations." *Proc Natl Acad Sci USA* [@Iranzo2018CancerMutation] | 2018 | PMID: 29915081 / DOI: 10.1073/pnas.1803155115 (identifier pairing not reconfirmed in this note) | Relevant next | **Pan-cancer network evolution.** Different angle: how the *network* of co-mutated drivers has evolved across cancer types. Complements the static pathway-enrichment framing. |
| 16 | Sondka Z, Bamford S, Cole CG, Ward SA, Dunham I, Forbes SA. "The COSMIC Cancer Gene Census: describing genetic dysfunction across all human cancers." *Nat Rev Cancer* [@Sondka2018COSMICCancer] | 2018 | PMID: 30293088 / DOI: 10.1038/s41568-018-0060-1 (identifier pairing not reconfirmed in this note) | Relevant next | **CGC.** The curated reference catalog used as ground truth by most benchmarks below. Not a pathway method per se but the indispensable reference list for filtering / validating pathway hits. |
| 17 | Wu C, Li Z, et al. "Comprehensive evaluation of computational methods for predicting cancer driver genes." *Brief Bioinform* | 2022 | DOI: 10.1093/bib/bbab548 / PMID: 35060587 (not reconfirmed in this note) | Relevant next | **2022 benchmark** of 12 driver methods (DN_MAX, DN_SUM, driverMAPS, DriverML, HotNet2, MaxMIF, Moonlight, MutPanning, nCOP, NetSig, OncoIMPACT, WITER) across 8 benchmark datasets. Closest thing to a current head-to-head evaluation; the main gap is it's gene-level, not pathway-level. |
| 18 | ICGC/TCGA Pan-Cancer Analysis of Whole Genomes Consortium. "Pan-cancer analysis of whole genomes." *Nature* [@Unknown2020PanCancer] | 2020 | PMID: 32025007 / DOI: 10.1038/s41586-020-1969-6 | Peripheral monitor | **PCAWG flagship.** Umbrella paper for the PCAWG set of 23+ papers including Reyna et al. [@Reyna2020Pathway]. Cited for context / framing; individual method papers (Reyna et al. [@Reyna2020Pathway], Paczkowska et al. [@Paczkowska2020]) are the operational references. |
| 19 | Reimand lab. "Directional integration and pathway enrichment analysis for multi-omics data." *Nat Commun* [@Slobodyanyuk2024DirectioIntegrat] | 2024 | DOI: 10.1038/s41467-024-49986-4 / PMID: not confirmed in this note | Peripheral monitor | **DPM** — directional extension of ActivePathways that prioritizes pathways changing consistently across omics directions. Useful when we add expression; not needed for mutation-only. |
| 20 | Multiple authors. "Multi-context modeling of driver pathways reveals common and specific mechanisms across 23 cancer types." *PLoS Comput Biol* | 2025 | DOI: 10.1371/journal.pcbi.1013349 / PMID: not confirmed in this note | Peripheral monitor | 2025 recent work (EntCDP / ModSDP) modeling common vs cancer-specific driver pathways across 23 cancer types. Directly in the space we want to target; worth tracking for methodology ideas. |

## Priority Reading Queue

**Core now (read first):**

1. **Reyna et al. [@Reyna2020Pathway] — PCAWG Pathway & Network Analysis** — read first for the end-to-end blueprint
   of how to apply multiple pathway methods at pan-cancer scale and report the consensus.
2. **Iorio et al. [@Iorio2018SLAPenrich] — SLAPenrich** — read second because its null model (mutation rate + gene
   length + mutual exclusivity) is the most directly applicable to our pipeline's
   gene-length-normalized ratio framing.
3. **Paczkowska et al. [@Paczkowska2020] — ActivePathways** — read third; the per-study-evidence-column input
   format matches our `gene_cancer_study` table layout exactly.
4. **Martínez-Jiménez 2020 — IntOGen** — read for the methods-ensemble design and the 568-gene
   consensus driver catalog we should check our results against.
5. **Leiserson et al. [@Leiserson2015] — HotNet2 pan-cancer** — read for the canonical pan-cancer
   network-method result; the diffusion framework is broadly applicable.
6. **Horn et al. [@Horn2018] — NetSig** — read for the node-degree-bias correction, which is a concrete
   risk when layering any PPI prior on our gene-level counts.

**Relevant next:**

7. Reimand et al. [@Reimand2019] — g:Profiler / GSEA / EnrichmentMap protocol (baseline off-the-shelf).
8. Reyna et al. [@Reyna2018HierarchHotNet] — Hierarchical HotNet (nested subnetworks).
9. Hofree et al. [@Hofree2013NetworkBased] — Network-Based Stratification (patient clustering upgrade path).
10. Vaske et al. [@Vaske2010InferencPatient] — PARADIGM (when we add expression).
11. Cerami et al. [@Cerami2010AutomateNetwork] — NetBox (cBioPortal-ecosystem module discovery).
12. Vandin et al. [@Vandin2011AlgorithDetectin] — HotNet1 (heat-diffusion framing).
13. Paull et al. [@Paull2013DiscoverCausal] — TieDIE (multi-omics coupling).
14. Knijnenburg et al. [@Knijnenburg2018GenomicMolecula] — Pan-cancer DDR landscape (pathway-level result exemplar).
15. Iranzo et al. [@Iranzo2018CancerMutation] — Cancer-mutation network evolution.
16. Sondka et al. [@Sondka2018COSMICCancer] — COSMIC Cancer Gene Census.
17. Wu 2022 — driver-method benchmark.

**Peripheral monitor:**

18. ICGC/TCGA PCAWG 2020 flagship (umbrella).
19. Slobodyanyuk/Reimand et al. [@Slobodyanyuk2024DirectioIntegrat] — DPM multi-omics directional pathway method.
20. 2025 EntCDP/ModSDP multi-context pathway modeling.

## Coverage Notes and Gaps

- **Pan-cancer benchmark at the pathway level, not the gene level, appears absent.** The 2022
  Wu et al. benchmark evaluates gene-level driver detection across 12 methods (HotNet2 is
  treated as a gene-level caller, not a pathway-level one). No comprehensive head-to-head
  of SLAPenrich vs ActivePathways vs HotNet2 vs NetBox vs NetSig *at the pathway rollup* on
  a shared benchmark cohort was found. This is a real gap — the project could contribute by
  benchmarking pathway calls across methods on cross-study cBioPortal data.
- **Cross-study pooling of pathway *p*-values or evidence** is nearly absent; ActivePathways
  can pool across per-gene evidence streams but treats each study's gene list as an
  independent multi-omics column, not as a repeated-measurement / random-effects structure.
  Natural methodological contribution: extend ActivePathways with a GLMM-style across-study
  random intercept, tying back to `t077` / `t079`.
- **Sanchez-Vega et al.'s 10-pathway taxonomy [@SanchezVega2018] is the default project seed** but has known
  limitations — selection of the 10 reflected a bench-to-prior-driver-knowledge curation;
  pathway methods that start from Reactome / KEGG / PID / Hallmarks will give a different
  answer. We should pre-register which pathway database(s) we treat as the primary rollup
  before running any pathway-level pipeline step.
- **Panel heterogeneity is not addressed by any of the standard pathway methods.** SLAPenrich
  is the closest (explicit per-gene exonic-length correction), but none of the methods above
  accept a per-(study, gene) callability mask as input. This is the pathway-level analog of
  the gene-level issue documented in `topic:cross-panel-normalization-methods` — and likely
  requires a custom pre-filtering step rather than an off-the-shelf method.
- **Clonal-hematopoiesis / matched-normal bias at the pathway level** is unexplored. CH genes
  cluster in hematopoietic/epigenetic-regulator pathways (DNMT3A, TET2, ASXL1, TP53, PPM1D,
  CHEK2, PRPF8); pathway methods applied to tumor-only cohorts will inflate those pathways
  spuriously. Tie-in to `topic:clonal-hematopoiesis-contamination` + task `t059`.
- **Copy-number-driven pathway alterations** are tangential (CNV is explicit out-of-scope per
  `specs/research-question.md`). Several cited methods (PARADIGM, ActivePathways PCAWG
  usage) integrate CNV — worth flagging as a future-scope extension.
- **PMID verification gap.** Nine of the twenty cited PMIDs/DOIs are flagged
  marked as not directly verified in this note — these came via LLM knowledge + title-match rather than direct
  `esummary`. All 6 `Core now` entries are verified; verification for the `Relevant next`
  tier should precede any paper-stub creation.

## Recommended Next Actions

1. **Convert Core-now entries into paper stubs** at `doc/background/papers/` (6 stubs):
   Reyna2020, Paczkowska2020, Leiserson2015, Iorio2018, MartinezJimenez2020, Horn2018.
2. **Add BibTeX entries** for all 20 shortlisted items to `papers/references.bib`; Core now
   first, Relevant next as tasks.
3. **Create a new topic** `doc/background/topics/pathway-level-pan-cancer-methods.md`
   consolidating the method taxonomy (enrichment vs network-diffusion vs patient-clustering
   vs integrative-multi-omics; frequentist vs generative; pathway-database-dependent vs
   de-novo).
4. **Pre-register pathway rollup choices** before any pathway-level pipeline step: which
   pathway database(s) (Reactome ≈ the Ensembl-curated default vs Sanchez-Vega-10 as the
   project-seed vs KEGG/Hallmarks as alternatives), which method as primary (SLAPenrich or
   ActivePathways are the strongest candidates for a pooled-count pipeline), which as
   comparator.
5. **Queue a follow-up search**: "pathway-aware GLMM / random-effects meta-analysis across
   studies" — the methodology gap surfaced above, which also connects to `t077` / `t079`.
6. **Check CH-pathway contamination** as a new sub-question: when CH-priority genes
   (Bolton et al. [@Bolton2020] 7-gene list) are allowed in the gene-level input, which pathway methods
   inflate which pathways? Cross-link to `t059`.
