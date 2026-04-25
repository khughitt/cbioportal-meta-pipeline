---
id: "paper:Smith2022"
type: "paper"
title: "Mitochondrial DNA mutations in ageing and cancer"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Smith2022"
related:
  - "topic:tumor-mutational-burden"
  - "topic:hypermutator-detection"
  - "topic:pan-cancer-mutation-landscape"
created: "2026-04-25"
updated: "2026-04-25"
---

# Mitochondrial DNA mutations in ageing and cancer

- **Authors:** Anna L. M. Smith, Julia C. Whitehall, Laura C. Greaves
- **Year:** 2022
- **Journal:** Molecular Oncology, vol. 16, pp. 3276-3294
- **DOI:** 10.1002/1878-0261.13291
- **PMCID:** PMC9490137
- **BibTeX key:** Smith2022
- **Source:** PDF (user-supplied); metadata confirmed via science-tool paper-fetch (Europe PMC, status: ok).

## Key Contribution

A comprehensive narrative review consolidating current knowledge on somatic mitochondrial DNA (mtDNA) mutations in two related contexts: normal ageing tissues and cancer. The authors synthesise evidence that mtDNA mutations accumulate clonally in post-mitotic and mitotic human tissues with age, that similar mutations are found in tumours, and that the functional consequences — predominantly via disruption of oxidative phosphorylation (OXPHOS) — are highly dependent on tissue type and on the specific gene and respiratory-chain complex affected. A key argument is that the same ageing-related somatic mtDNA clones that pre-exist in normal tissue may be enriched during oncogenic transformation, potentially modulating tumour metabolism, apoptotic threshold, and metastatic potential, without being the primary oncogenic driver in most settings.

## Methods

This is a **literature review** with no primary data. The authors draw on:
- PolγA^mut/mut mouse mutator models (proofreading-deficient mitochondrial polymerase gamma) as mechanistic systems.
- Transmitochondrial cybrid cell lines as tools to isolate mtDNA genotype effects from nuclear background.
- Large pan-cancer genomic analyses of patient tumour and matched normal tissues (key: the Pan-Cancer Analysis of Whole Genomes, PCAWG, consortium data for mtDNA).
- In vivo xenograft tumour models.
- Stable isotope tracing and metabolomics experiments in cell lines.
- The Wellcome Centre for Mitochondrial Research group's own in vivo intestinal tumour mouse work (Smith et al., Nat Cancer 2020, ref. 110 in paper).

No new bioinformatic pipeline or dataset is introduced.

## Key Findings

### The mtDNA genome and mutational biology
- Human mtDNA: 16,569 bp, circular, encodes 13 OXPHOS proteins (complexes I–V) + 22 tRNAs + 2 rRNAs. The remaining ~1,500 OXPHOS subunits are nuclear-encoded.
- mtDNA exists in thousands of copies per cell; heteroplasmy (mixed wild-type/mutant copies) is the norm for somatic mutations. Phenotypic threshold typically requires 60–90% mutant load before OXPHOS deficiency is manifest — important for interpreting low-VAF calls in tumour sequencing.
- Clonal expansion through mitotic segregation (random at each cell division) is the dominant mechanism by which low-level mtDNA variants rise to detectable or homoplasmic levels in proliferating cells.

### mtDNA mutations in ageing
- Clonally expanded mtDNA point mutations and large-scale deletions accumulate in post-mitotic tissues (brain, skeletal muscle, cardiomyocytes) and in stem-cell compartments of proliferating tissues (colon crypts, stomach, liver).
- In the colon, entirely COX-deficient crypts carry single clonally expanded mtDNA mutations — typically transitions involving G residues, consistent with replication error rather than oxidative damage.
- mtDNA deletions cause OXPHOS defects in substantia nigra neurons and are strongly associated with Parkinson's-related neurodegeneration.
- mtDNA mutations promote cellular senescence and ROS-mediated telomere shortening — hallmarks of ageing shared with cancer.

### mtDNA mutations in cancer — prevalence and spectrum
- mtDNA mutations are reported across all major cancer types. Early studies focused on D-loop deletions; more recent pan-cancer analyses use whole-mitochondrial genome sequencing.
- PCAWG pan-cancer analysis (Yuan et al. 2020, Nat Genet): comprehensive characterisation of mtDNA across thousands of tumours; MT-CO1 (complex IV) is the most frequently mutated mtDNA gene in breast, cervical, and bladder cancers.
- Gorelick et al. 2021 (Nat Metab): tissue lineage drives recurrence patterns — complex I mutations (MT-ND genes) positively selected in kidney, colon, thyroid; negatively selected in complex V (MT-ATP) genes across all types, implying total ATP synthase loss is intolerable.
- High levels of homoplasmy for mtDNA mutations are achievable via neutral drift alone (modelled in Coller et al., Nat Genet 2001) — not all homoplasmic tumour variants are positively selected.
- mtDNA copy number changes are tumour-type-specific: reduced in breast, kidney, hepatocellular, myeloproliferative; increased in lung, pancreatic, lymphocytic leukaemias.

### Functional consequences by respiratory complex

**Complex I (MT-ND1, -ND4, -ND5, -ND6):**
- Most frequently mutated (>50% of mtDNA encodes complex I subunits).
- Heteroplasmic MT-ND5 frameshift: increased ROS, apoptosis resistance, enhanced xenograft tumour growth.
- MT-ND6 nonsense/missense: activates Akt survival pathway via ROS, promotes EMT and lung adenocarcinoma migration/invasion.
- Homoplasmic m.3571insC (MT-ND1): disables complex I → NADH accumulation → α-KG/SA imbalance → HIF-1α stabilisation → glycolytic gene induction. Allotopic wild-type ND1 expression reverses the effect. This heteroplasmy-level-dependent phenotype (severe = tumour promoting; mild = null) is a central mechanistic theme of the review.
- Smith et al. 2020 (Nat Cancer, ref. 110): age-related complex I mtDNA mutations in APC-knockout intestinal tumour mice accelerate tumour growth via serine synthesis and one-carbon metabolism pathway upregulation.
- Renal oncocytoma: complex I loss of function is apparently oncogenic in this one tumour type — the only setting where mtDNA mutations can drive tumorigenesis without nuclear driver co-mutations.

**Complex III (MT-CYB):**
- MT-CYB mutations increase ROS → NF-κB-mediated tumour growth in bladder cancer.
- OXPHOS-deficient tumours may engage reductive carboxylation (reverse TCA) for biosynthetic precursors — stable isotope tracing in MT-CYB mutant osteosarcoma confirmed this.

**Complex IV (MT-CO1, -CO2, -CO3):**
- MT-CO1 most frequently mutated in pan-cancer data; 12% of prostate cancer samples in one cohort carry missense mutations.
- Increased ROS, nitric oxide in MT-CO1 mutant osteosarcoma cybrids.
- Inherited mitochondrial biogenesis variants influence ovarian cancer risk.

**Complex V (MT-ATP6, -ATP8):**
- Pathogenic m.8993T>G and m.9176T>C mutations in MT-ATP6: increased tumour cell proliferation in vitro and in xenografts; reduced apoptosis.
- Severely disruptive truncating complex V mutations are negatively selected across cancer types — total ATP loss is not compatible with cell survival.

**mtDNA copy number:**
- Kidney chromophobe and thyroid tumours with mtDNA null-allele fixations (homoplasmic truncating mutations) show much higher copy numbers — compensatory mitochondrial mass upregulation.

### Clinical phenotype and patient stratification
- Truncating mtDNA mutations affecting complex I in ~20% of stage 1–3 colorectal cancer cases are associated with significantly greater survival compared to wild-type or non-truncating variants (existing exome sequencing data, 344 patients).
- Weak association between mtDNA genotype and colorectal cancer consensus molecular subtype (CMS2).
- mtDNA genotyping as a cost-effective tool to distinguish synchronous versus metastatic endometrial and ovarian tumours — shared mtDNA genotype = metastatic origin; divergent genotypes = synchronous primaries. Validated in breast and borderline ovarian tumours.

### Three mechanistic models for mtDNA mutations in cancer (Fig. 3)
1. mtDNA mutations as direct oncogenic drivers (renal oncocytoma, complex I loss).
2. Age-acquired mtDNA mutations that pre-exist transformation and modulate tumour phenotype after nuclear oncogene activation — can be pro-tumourigenic (metabolic rewiring, ROS survival signalling, EMT) or neutral.
3. mtDNA mutations that arise during rapid tumour cell division by neutral drift or are negatively selected if too deleterious (complex V loss).

### Emerging therapeutics
- OXPHOS-dependent cancer stem cells resist standard therapies; mitochondrial complex I inhibitors (IACS-010759) show efficacy in AML and T-ALL pre-clinical models.
- Small-molecule inhibitors of mitochondrial transcription (IMTs targeting POLRMT) suppress OXPHOS-dependent cancer cell lines.
- mtDNA genome editing tools: mitochondrially targeted zinc finger nucleases (mtZFNs), DddA-derived cytosine base editors (mitoDdCBEs), TALE-linked adenine deaminases (TALEDs) — enable site-specific mutagenesis without CRISPR, opening new research tools.

## Relevance

**Direct relevance to the cbioportal hypermutator pipeline (topic:tumor-mutational-burden):**

The cbioportal pipeline detects hypermutators using nuclear-genome TMB (mutations per Mb of callable nuclear genome). MtDNA mutations are a separate phenomenon and are not part of standard cBioPortal mutation calls — virtually all cBioPortal studies call somatic variants on the nuclear genome only. The chrM chromosome is routinely excluded from somatic variant calling pipelines because: (1) the mitochondrial genome is haploid-equivalent at the population level but polyploid within cells, making variant calling ill-defined under diploid assumptions; (2) matched-normal subtraction is unreliable for mtDNA due to heteroplasmy and differing mtDNA copy number between tumour and normal; (3) the high copy number causes extreme depth that confounds standard callers. This means:

- The existing `compute_per_sample_tmb.py` denominator (callable Mb of nuclear genome) is correct and unaffected by mtDNA biology.
- mtDNA mutations are absent from the mutation tables the pipeline processes, so they do not inflate or deflate nuclear TMB estimates.
- The POLE/POLD1 hotspot detection in `detect_polymerase_hotspots.py` targets the nuclear-encoded polymerases responsible for nuclear DNA replication fidelity. Mitochondrial genome fidelity is controlled by the mitochondrially targeted PolγA (POLG gene, nuclear-encoded) — distinct from POLE/POLD1 and not currently modelled in the pipeline. This is appropriate given that mtDNA mutations are not in the input data.

**Indirect relevance — interpreting cancer-type mutation frequencies:**

Tissues with high mtDNA mutation burden (kidney, colon, thyroid per PCAWG data) may have confounded tumour-versus-normal comparisons in unmatched cBioPortal studies if any mtDNA variants were inadvertently included. However, standard bioinformatic practice excludes chrM, making this a low-risk concern.

The metabolic rewiring described here (Warburg shift, reductive carboxylation, serine-one-carbon upregulation) is driven by OXPHOS dysfunction, which could in principle affect which nuclear genes are under selection pressure in different cancer types. This provides biological context for interpreting cross-study variation in metabolic gene mutation frequencies (IDH1/2, FH, SDH genes) in the pipeline's output tables.

**Coverage flag — chrM in cBioPortal studies:**
Most cBioPortal studies do NOT call mtDNA variants. If the pipeline's `build_panel_callable_sizes` rule ingests BED files from targeted panels (e.g., GENIE), those BED files generally do not include chrM intervals, so the callable-Mb denominator for TMB is already implicitly nuclear-only. This is correct behaviour. If a future cBioPortal study were to include mtDNA calls, the study's per-sample mutation count could be artificially inflated by thousands of homoplasmic or near-homoplasmic mtDNA variants — such a study should be flagged and excluded from the TMB normalisation, or mtDNA variants filtered before input.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| mtDNA somatic mutation burden | Not in pipeline scope | chrM excluded from standard cBioPortal calls; pipeline is nuclear-genome-only |
| OXPHOS complex I–V gene mutations | Nuclear TMB; driver gene lists | MT-ND*, MT-CO*, MT-CYB, MT-ATP* are mtDNA-encoded; separate from nuclear POLE/POLD1 |
| Heteroplasmy threshold (60–90% for phenotype) | VAF filtering thresholds | Distinct from somatic nuclear VAF; context only |
| Clonal expansion of mtDNA mutations | Clonal hematopoiesis contamination (SNV level) | Mechanistically analogous but distinct genome; CH annotation focuses on nuclear variants |
| PolγA (POLG) replication fidelity | POLE/POLD1 hotspot detection | POLG drives mtDNA replication errors; POLE/POLD1 drive nuclear hypermutation — different genes, different genomes |
| Pan-cancer PCAWG mtDNA analysis | Cross-study gene×cancer frequency table | PCAWG mtDNA results are not in cBioPortal mutation tables; complementary external data |
| Cancer type–specific mtDNA selection | Cancer-type stratification in pipeline | Tissue specificity of complex I selection supports per-cancer-type rather than pan-cancer modelling |
| TMB (nuclear, per Mb) vs. mtDNA mutation load | `compute_per_sample_tmb.py` | Pipeline TMB denominator is nuclear callable Mb — correct and unaffected by mtDNA |
| mtDNA genotyping for tumour clonality | Not modelled | Potential future use: distinguishing synchronous vs. metastatic study samples |

## Limitations

- Literature review only — no new quantitative synthesis or meta-analysis; effect-size estimates are drawn from individual studies with variable designs and sample sizes.
- Pan-cancer mtDNA data rely on PCAWG and a handful of large studies; cBioPortal-derived cohorts are not directly assessed.
- The functional studies are predominantly in cybrid cell lines or mouse models; clinical translation of mechanistic claims (e.g., complex I mutation → EMT) remains incomplete.
- The three mechanistic models (Fig. 3) are schematic and not formally tested across cancer types; the boundary between "driver" and "modulator" is qualitative.
- The review was written in 2022; subsequent pan-cancer mtDNA analyses (e.g., from expanded PCAWG releases) may have updated specific prevalence estimates.
- Therapeutic claims (IACS-010759 in AML/T-ALL; IMTs) are based on pre-clinical and early-stage data; clinical utility is not yet established.

## Model / Tool Availability

No computational model or tool is released with this review. Tools mentioned:
- mtZFNs (mitochondrially targeted zinc finger nucleases) — not publicly available as off-the-shelf reagents.
- mitoDdCBEs and TALEDs — described in companion primary papers (Mok et al. 2020, Richter et al. 2020); reagents available per those papers' terms.
- PCAWG mtDNA dataset — available via ICGC/TCGA data portals (controlled access).

## Follow-up

- Confirm that `build_panel_callable_sizes` never ingests chrM intervals from any BED file in the GENIE dataset — a one-line grep of the BED files would close this.
- If any future cBioPortal study is encountered that appears to call mtDNA variants (very unusual), add a pre-processing filter step to strip chrM rows from mutation input before per-sample TMB computation.
- The renal oncocytoma finding (complex I mtDNA loss as oncogenic driver without nuclear co-mutations) is the one cancer type where mtDNA-driven hypermutation could in principle produce anomalous nuclear TMB estimates — but only if mtDNA calls were accidentally included. Not an active risk given current cBioPortal data conventions.
- Representative primary references flagged in this review relevant to hypermutator / TMB context:
  - Gorelick et al. 2021, Nat Metab 3(4):558–70 — tissue lineage drives recurrent mtDNA selection in tumours (positive selection in complex I for kidney/colon/thyroid; negative selection for complex V across all types).
  - Yuan et al. 2020, Nat Genet 52(3):342–52 — PCAWG comprehensive mtDNA characterisation across human cancers.
  - Smith et al. 2020, Nat Cancer 1(10):976–89 — age-related complex I mtDNA mutations accelerate intestinal tumourigenesis (authors' own in vivo work).
