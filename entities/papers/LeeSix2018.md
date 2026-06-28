---
type: paper
title: Population dynamics of normal human blood inferred from somatic mutations
status: active
created: '2026-04-18'
updated: '2026-06-28'
id: paper:LeeSix2018
ontology_terms: []
source_refs:
- paper:LeeSix2018
related:
- topic:clonal-hematopoiesis-contamination
- paper:Poon2021
- paper:Yoshida2026
- question:0006-ch-priority-gene-completeness
---

# Population dynamics of normal human blood inferred from somatic mutations

- **Authors:** Henry Lee-Six, Nina Friesgaard Øbro, Mairi S. Shepherd, Sebastian Grossmann, Kevin Dawson, Miriam Belmonte, Robert J. Osborne, Brian J. P. Huntly, Inigo Martincorena, Elizabeth Anderson, Laura O'Neill, Michael R. Stratton, Elisa Laurenti, Anthony R. Green, David G. Kent, Peter J. Campbell
- **Year:** 2018
- **Journal:** Nature
- **Volume/Pages:** 561(7724): 473–478
- **DOI:** https://doi.org/10.1038/s41586-018-0497-0
- **PMID:** 30185910
- **PMCID:** PMC6163040
- **BibTeX key:** LeeSix2018
- **Source:** full-text XML (Europe PMC, PMC6163040); metadata confirmed via Crossref

## Key Contribution

This normal-blood clonal-dynamics note links topic:clonal-hematopoiesis-contamination, paper:Poon2021, and paper:Yoshida2026.

The first direct, genome-wide phylogenetic reconstruction of human haematopoietic stem cell (HSC) population dynamics in a single normal individual. By whole-genome sequencing 140 single-cell-derived HSC/progenitor colonies from a healthy 59-year-old man and performing deep "recapture" targeted sequencing of bulk blood lineages, the study establishes that: (1) blood production is supported by a large, continuously active pool of 50,000–200,000 HSCs; (2) HSC clonal dynamics in this subject are consistent with selectively neutral drift — no known driver mutations are present and dN/dS = 1.001; and (3) the phylogenetic tree traces back through early embryogenesis to a cell that predated gastrulation, demonstrating that the normal blood phylogeny spans the full human lifespan. This paper is the foundational measurement underpinning all modern quantitative models of CH clone dynamics and the "drift vs. selection" debate.

## Methods

**Experimental design ("capture–recapture").** Single HSCs and haematopoietic progenitor cells (HPCs) were FACS-sorted from a bone marrow aspirate and peripheral blood from a 59-year-old male with normal blood counts and no haematological history. Cells were expanded in single-cell liquid cultures or colony-forming cell (CFC) assays. 198 colonies were whole-genome sequenced (~15× per colony); 140 passed clonality QC (VAF distribution around 50%). The final set comprised 89 immunophenotypic HSCs, 38 megakaryocyte-erythrocyte progenitors (MEPs), 8 granulocyte-macrophage progenitors (GMPs), and 5 common myeloid progenitors (CMPs).

**Variant calling and phylogenetic tree.** 129,582 genome-wide somatic substitutions were identified. Substitutions shared between colonies identify lines-of-descent sharing a common ancestor. A maximum-parsimony / SCITE phylogeny was constructed from shared vs. private mutation patterns. Branch lengths are proportional to mutation counts (the molecular clock). Multiple tree-construction methods (substitutions, indels, tandem repeats; parsimony, neighbour joining) gave concordant results.

**Population size estimation.** "Recapture" targeted sequencing of peripheral blood granulocytes (three timepoints: 4, 9, 14 months after bone marrow aspirate; mean coverage 268–4,669×) and lymphocytes (B and T cells) detected the fraction of each colony's mutations present in bulk blood. An approximate Bayesian computation (ABC) framework with 200,000 simulations of neutral haematopoiesis estimated the number of active HSCs and their symmetric division rate by matching summary statistics from simulated experiments to observed data.

**Selection testing.** Positive or negative selection was assessed by (1) dN/dS ratio across all colonies using the Martincorena method [@Martincorena2017]; (2) inspection for known myeloid driver mutations in a targeted hotspot bait-set; (3) a buccal swab confirmed no germline confounds.

**Mutation rate in embryogenesis.** Early embryonic divisions were inferred from the first few mutations partitioning all 140 colonies; the rate of ~1.2 mutations/division was estimated from the number of cell doublings implied by polytomy resolution.

## Key Findings

### 1. Cohort and overall scale

A single healthy 59-year-old man. 140 single-cell-derived colonies successfully whole-genome sequenced. Total somatic mutations placed on the phylogenetic tree: **129,582 substitutions** (8,676 shared between ≥2 colonies). Mean mutation burden per colony: **1,023 substitutions** (range 815–1,210) and 20 indels (range 2–37). No somatic structural variants identified.

### 2. Mutation rate per cell per year (molecular clock)

The paper does not state a coding-specific per-year mutation rate directly. The per-colony mean burden of ~1,023 substitutions in a 59-year-old individual implies approximately **17 genome-wide point mutations per year** per HSC (1,023 / 59 ≈ 17.3 SBS/year), consistent with later estimates. The trinucleotide spectrum is dominated by C>T and T>C transitions, matching published patterns from myeloid cancers and age-related CH. [NOTE: The paper does not explicitly report "18 coding mutations per year"; the ~17–18 figure commonly cited for HSCs comes from the whole-genome rate integrated over the adult lifespan in this and companion studies.]

### 3. Neutral drift — no driver mutations

dN/dS across all colonies = **1.001** (95% CI: 0.889–1.127; dN/dS = 1.0 indicates neutrality). No known myeloid driver mutations were identified in any colony. Hotspot bait-set targeted sequencing of bulk blood confirmed no driver hotspots. This subject's haematopoietic compartment exhibits selectively neutral mutation accumulation — providing the key null-model baseline for interpreting CH selection signals in older/diseased individuals.

### 4. Effective HSC population size: 50,000–200,000

The ABC framework estimated the **90% credibility interval for active HSC number contributing to granulocytes: 44,000–215,000** (stated as "50,000–200,000" in the abstract). The time between successive symmetric self-renewal divisions was estimated at **2–20 months**. The 140 sequenced colonies represent approximately 1/1,000 of the active stem cell pool, explaining the preponderance of private mutations (no shared branches) in the phylogeny. This large population size is key: neutral drift in 50,000–200,000 HSCs is slow, so clones reaching 1% VAF require a meaningful selective fitness advantage.

### 5. Phylogenetic tree spans embryogenesis to adulthood

Two root-level mutations completely partitioned all 140 colonies (52 vs. 88 colonies; no colony carried both). These same mutations were detected in the buccal swab in the same ~1:2 ratio, establishing that the most recent common ancestor of blood and buccal epithelium predated gastrulation — consistent with the fertilised egg, with one mutation arising at the first cell division. Subsequent embryonic cleavages generated ~33 lines-of-descent by 10 mutations of molecular time, implying ≥5 cell doublings and a mutation rate of ~1.2/division in embryogenesis. This demonstrates that the normal blood phylogeny is an accurate recorder of human development from the very first cell division.

### 6. Population size trajectory: rapid early expansion, stable adult plateau

Phylodynamic coalescence analysis reveals rapid HSC pool expansion during early life (childhood/early adolescence), reaching a **stable plateau by late childhood/adolescence** — consistent with prior inferences from telomere-length and X-chromosome inactivation studies. The stable adult population implies symmetric self-renewal is balanced by stem cell death/senescence and symmetric commitment to progenitors.

### 7. Multilineage output from adult stem cells: granulocytes and B lymphocytes

In the recapture phase, early-phylogeny mutations (top of tree) were detectable in granulocytes, B lymphocytes, and T lymphocytes — confirming multilineage output from ancient shared progenitors. Beyond 100 mutations (~early adolescence equivalent), some adult clone branches contributed detectably to both granulocytes and B lymphocytes but not T lymphocytes. The authors interpret this as continued contribution of the same HSC lines to myeloid and B-lymphoid output throughout life, with granulocyte and B-cell production more closely coupled than T-cell production (perhaps due to the large long-lived T-cell pool diluting ongoing HSC contribution).

### 8. Stem cells recirculate body-wide

Bone marrow-derived HSCs (from right iliac crest) were not more clustered on the phylogeny than peripheral blood-derived HSCs (p = 0.14), implying sufficient recirculation that the iliac crest aspirate is a representative sample of the whole-body HSC pool.

## Relevance

**1. Quantitative null model for CH drift vs. selection.**
The central finding — that 50,000–200,000 actively dividing HSCs underlie normal haematopoiesis, and that in this subject all clonal dynamics were consistent with neutral drift — provides the quantitative baseline for interpreting CH. With a pool this large, a clone reaching 1% VAF in bulk blood requires substantial fitness advantage (s >> 1/(2N_e) ≈ 1/100,000); neutral drift alone cannot explain most observed large CH clones. This directly sharpens the CH contamination concern for the cbioportal pipeline: clones that are detectable in standard sequencing panels (VAF >1–2%) are very likely to carry driver mutations, not just drift.

**2. Molecular clock (~17 SBS/year) anchors relative clone age estimates.**
The per-HSC mutation rate implied by the colony data (~17 SBS/year genome-wide) is widely used to date CH driver acquisition events. For example, DNMT3A mutations detected at 1% VAF in a 60-year-old were likely acquired ~20–40 years earlier and have been expanding under selection since. This timing context is important when interpreting whether DNMT3A-driven CH in a 65-year-old solid-tumor patient is likely to be a contaminating clone present in the blood draw or a genuinely tumor-intrinsic mutation.

**3. Neutral drift as a context for "unexplained selection" (Poon et al. sharpened).**
Poon et al. [@Poon2021] demonstrate that ~90% of positive selection in blood is unexplained by the 20 most common CH drivers and >85% unexplained even by the full 468-gene MSK-IMPACT panel. Lee-Six 2018 provides the population-genetic context: given N_eff ~ 100,000 HSCs, the expected neutral clone-size distribution makes it very unlikely for large clones to arise by chance. Therefore, the Poon et al. "unexplained selection" cannot be primarily cryptic neutral drift — it must reflect genuine positive selection from drivers currently outside known CH gene lists. This sharpens the `question:0006-ch-priority-gene-completeness` framing: the Bolton 7-gene list is not capturing most of the actual selective events. The selection is real; the genes driving it are unknown.

**4. Blood phylogeny predates cancer — single-individual depth.**
The demonstration that blood phylogeny traces to the fertilised egg, with embryonic clones still measurable 59 years later, confirms that CH mutations detected in cancer patients can in principle have originated in the embryo and be completely irrelevant to tumor biology. This is an extreme example of why matched-normal sequencing matters: the "normal" blood sample may itself carry embryo-age clones.

**5. No DNMT3A or other CH drivers in this subject — the driver-free baseline.**
This 59-year-old individual's HSCs showed no known myeloid drivers and dN/dS = 1. This is rare (most 59-year-olds have detectable CH clones). The paper explicitly notes this as fortuitous: it enables a clean null model. For DNMT3A: its absence here, combined with the large population size inferred, shows that the DNMT3A fitness advantage (~10–30%/year from other studies) would have allowed a DNMT3A clone arising at age 20 to reach >10% VAF by age 59 via selection. This quantitative framing is important for the `ch_priority_gene` logic: even at moderate selection coefficients, only a few decades are needed for DNMT3A clones to become detectable, so older study cohorts have higher expected CH contamination rates.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| HSC pool size 50k–200k | N_eff for drift calculations | Key for interpreting whether CH clones are drift or selection |
| ~17 SBS/year molecular clock | Mutation accumulation rate per HSC | Anchors clone-age estimation for CH driver timing |
| dN/dS = 1.001 (neutral) | Null model for CH gene detection | Confirms that large detectable clones require selection |
| Capture–recapture WGS design | Not yet in pipeline; conceptually relevant | Single-individual whole-genome phylogeny vs. bulk panel sequencing |
| Pre-gastrulation root | Embryo-age mutations in normal blood | Motivates matched-normal for very early CH mutations |
| Multilineage output | CH contamination cross-lineage risk | DNMT3A/TET2 clones pollute both myeloid and B-cell studies |
| Stable adult plateau | Age-stable pool; age-increasing clone size | CH accumulates with age; older cohorts have higher contamination |

## Limitations

- **Single individual.** The entire population-size estimate and drift-vs-selection inference rests on one 59-year-old man with the unusual property of having no detectable CH drivers. Generalizability to the general aging population (where most individuals have at least one detectable CH clone by age 60) requires companion studies.
- **No driver mutations observed.** The dN/dS = 1 finding is informative for the null model but means the paper cannot directly characterize DNMT3A or TET2 fitness dynamics. Those require studies deliberately sampling CH-positive individuals.
- **~140 colonies = ~1/1,000 of the HSC pool.** The authors note that increasing the sampled fraction would reduce uncertainty on the population-size estimate. The current estimate's 90% CI spans 4.5-fold (44k–215k).
- **Single tissue (blood).** Applicable only to haematopoiesis; cannot be generalized to solid tissues without analogous studies.
- **2–20 month symmetric division rate.** The generation time uncertainty spans 10-fold, making absolute clone-age calculations imprecise. Combined with population size uncertainty, absolute fitness coefficient estimates from other studies carry large error bars.
- **No assessment of DNMT3A or other epigenetic regulator mutations.** The study explicitly sought and did not find myeloid drivers. It cannot speak to what fraction of healthy 59-year-old HSC pools carry DNMT3A clones below detection (VAF < 1/2000 in granulocytes).

## Model / Tool Availability

No standalone software package described. The ABC framework code was developed by the Campbell lab (Wellcome Sanger) and is described in the Technical Supplement. The SCITE phylogenetic tool (Jahn et al., referenced in the methods) is separately available. The underlying phylodynamic coalescence inference uses the BEAST/phylodynamics framework (Lan et al. 2015, Bioinformatics). Data: bulk targeted sequencing summary data referenced; primary colony WGS data available under controlled access via EGA (accession not stated in the full text — contact corresponding authors).

## Follow-up

- **Watson et al. 2020 (Nature)** — direct extension from the same Campbell lab using >400 individuals to characterize DNMT3A fitness dynamics and clone age, using the Lee-Six 2018 methodology. Essential companion for CH driver quantification.
- **Fabre et al. 2022 (Nature)** — phylogenetic reconstruction in multiple individuals with CH drivers, extending Lee-Six 2018 to driver-positive contexts; quantifies selection coefficients for DNMT3A, TET2, ASXL1.
- **Poon et al. [@Poon2021]** — this paper's neutral-population estimate is the population-genetic substrate for Poon's argument that the "unexplained" selection in blood is genuinely selective (not drift), because N_eff ~ 100,000 makes drift-driven large clones extremely unlikely.
- **Question for this project:** Given the Lee-Six population size estimate (N_eff ~ 100,000), what is the minimum per-year fitness advantage (s) needed for a clone to reach 5% VAF by age 60 starting from a single mutation at age 30? The rough answer is s ~0.1–0.3/year, consistent with estimates for DNMT3A (~10–20%/year) but much larger than typical neutral drift expectation. This grounds the Bolton 7-gene list concern (`question:0006-ch-priority-gene-completeness`): the genes driving the unexplained 90% of selection in Poon et al. must each have s > ~0.05/year to be detectable; the question is whether there are many low-s genes or a few unidentified high-s genes.
- **Approach implication:** For the cbioportal pipeline, the Lee-Six 2018 HSC pool size places a quantitative lower bound on required fitness advantage for any blood-study CH clone to be at detectable VAF. Studies with median patient age >55 should be treated with the highest caution for CH contamination; even without known driver mutations, neutral drift in this large pool cannot explain observable clonal expansions.
