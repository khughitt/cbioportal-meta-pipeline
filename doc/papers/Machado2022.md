---
id: "paper:Machado2022"
type: "paper"
title: "Diverse mutational landscapes in human lymphocytes"
status: "active"
ontology_terms: []
datasets: []
source_refs:
  - "cite:Machado2022"
related:
  - "paper:Machado2021"
created: "2026-05-31"
updated: "2026-05-31"
---

# Diverse mutational landscapes in human lymphocytes

- **Authors:** Heather E. Machado, Emily Mitchell, Nina F. Obro, Kirsten Kubler, Megan Davies, Daniel Leongamornlert, Alyssa Cull, Francesco Maura, Mathijs A. Sanders, Alex T. J. Cagan, Craig McDonald, Miriam Belmonte, Mairi S. Shepherd, Felipe A. Vieira Braga, Robert J. Osborne, Krishnaa Mahbubani, Inigo Martincorena, Elisa Laurenti, Anthony R. Green, Gad Getz, Paz Polak, Kourosh Saeb-Parsy, Daniel J. Hodson, David G. Kent, Peter J. Campbell
- **Year:** 2022
- **Journal:** Nature (Vol. 608, pp. 724–732)
- **DOI/URL:** https://doi.org/10.1038/s41586-022-05072-7
- **BibTeX key:** Machado2022
- **Source:** PDF

## Key Contribution

This paper provides the most comprehensive whole-genome characterisation to date of somatic mutation burden and mutational signatures in normal (non-malignant) human lymphocytes across five immune cell compartments (naive B, memory B, naive T, memory T, and HSPCs), sequencing 717 single-cell colony-expanded genomes from donors aged 0–81 years. It demonstrates that lymphocytes carry substantially more mutations than haematopoietic stem cells, that off-target effects of immunological diversification (SHM, RAG-mediated recombination) account for roughly half of the excess differentiation-associated mutations, and that the mutational signatures and burdens of normal memory B cells closely mirror those observed in many B-cell lymphomas — suggesting that malignant transformation of lymphocytes arises largely from the same mutational processes operating during normal ontogeny.

## Methods

**Cohort:** Four donors (bone marrow, spleen, peripheral blood; ages 27–81) plus cord blood and tonsil samples from additional donors; all haematopoietically normal and healthy. Five cell subsets sorted by flow cytometry: naive B (CD3-CD19+CD20+CD27-CD38-IgD+), memory B (CD3-CD19+CD20+CD27+CD38-IgD-), naive T (CD3+CD4/CD8+CCR7+CD45RA-), memory T (CD3+CD4/CD8+CCR7-CD45RA-), and HSPCs.

**Single-cell expansion:** Novel in-vitro protocols expanded single lymphocytes into colonies of 30–2,000 cells, then extracted DNA for sequencing. Culture efficiencies: ~2–5%.

**Sequencing:** Whole-genome sequencing (WGS) at ~20x mean depth on Illumina XTen platform; reads mapped to GRCh37d5 (BWA-MEM). Final dataset: 717 genomes (85 naive B, 74 memory B, 365 naive T, 100 memory T, plus overlapping HSPC genomes from a companion HSPC study).

**Variant calling:** SNVs via CaVEMan, indels via Pindel, structural variants (SVs) via BRASS, CNVs via ASCAT. Germline variants removed using beta-binomial and Shearwater filters. Somatic SVs and CNVs manually curated.

**Mutational signatures:** Per-colony signature decomposition using SigProfiler and hdp (de novo extraction). Seven signatures retained after cross-validation: SBSblood (novel blood-specific endogenous signature), SBS1, SBS7a (UV), SBS8, SBS9, SBS17b, SBS18. Signature timing inferred via regression of mutation distribution against 149 epigenomes representing 48 blood cell types/differentiation stages. Immunoglobulin receptor sequences analysed by IgCaller to quantify on-target SHM. RAG and CSR motif analysis performed at SV breakpoints using FIMO.

**Selection analysis:** dNdScv used genome-wide (excluding immunoglobulin loci) to estimate dN/dS ratio.

## Key Findings

### Mutation burden and rates

- SNV burden increases linearly with age across all cell types but at different rates: HSPCs ~16 SNVs/year; naive B ~15 SNVs/year; memory B ~17 SNVs/year; naive T ~22 SNVs/year; memory T ~25 SNVs/year. T cells accumulate mutations faster than B cells throughout life.
- Compared to HSPCs, naive B and T cells carry ~100 extra SNVs on average; memory B cells carry ~1,034 extra SNVs (95% CI: 604–1,465); memory T cells ~277 extra SNVs. The excess in memory cells reflects differentiation history, antigen exposure, and residency in diverse microenvironments.
- Indels also accumulate at ~0.7–1.1 per year, higher in lymphocytes than HSPCs (0.7 indels/year).
- Cell-to-cell variance is large: within-donor s.d. ~820 SNVs/cell for memory B and ~592 for memory T, far exceeding between-person variation (~60 SNVs/cell).

### Mutational signatures

Seven signatures identified and validated across lymphocyte subsets:

- **SBSblood**: Novel endogenous haematopoietic signature, dominant in HSPCs and naive cells; co-occurs with SBS1 in HSPCs (sigfit resolves them as distinct); correlates strongly with HSPC chromatin marks, consistent with pre-differentiation origin.
- **SBS1** (spontaneous deamination of methylated cytosines): ~14% of mutations in HSPCs, naive B, and naive T; clock-like.
- **SBS9**: Germinal-centre-associated signature; dominant excess signature in memory B cells (mean ~780 mutations/cell; up to ~3x baseline); strongly correlated with the on-target SHM rate (R²=0.57, P=4×10⁻⁹) and with telomere lengthening (R²=0.37, P=3×10⁻⁸); enriched in late-replicating, gene-poor repressed genomic regions. Authors propose SBS9 arises from error-prone translesion synthesis by polymerase eta at replication stress/oxidative lesions during germinal centre cycling rather than directly from AID deamination.
- **SBS7a** (UV damage): Substantial contribution in memory T cells (mean ~757 mutations/cell; range 205–2,783); 9 out of 100 memory T cells exceeded 10% SBS7a with CC>TT dinucleotide substitutions. High-SBS7a cells had significantly shorter telomeres, consistent with greater proliferative history and UV accumulation during skin residency.
- **SBS17b**: Present in >10% of mutations in ~4 out of 74 memory B and ~1 out of 100 memory T cells; spectrum resembles 5-fluorouracil chemotherapy but occurrence is independent of treatment — possibly reflects a specific microenvironmental mutagen in gastrointestinal mucosa.
- **SBS8** and **SBS18**: Sporadic exogenous processes accumulating hundreds to thousands of extra mutations in some memory cells.
- SBS7a and SBS17b do not correlate with age; SBSblood and SBS1 do, consistent with endogenous clock-like processes vs sporadic exogenous exposures.

### Epigenomic timing of mutational processes

- SBSblood mutations in naive B cells correlate better with HSC epigenomes than naive B epigenomes, implying most SBSblood mutations are acquired pre-differentiation.
- SBSblood in naive T cells correlates with CCR7+CD45RO-CD25-CD235- thymic-origin naive T epigenomes, consistent with a large long-lived naive T pool established in early life.
- Memory B cell SBS9 mutations correlate most closely with germinal centre B cell epigenomes, confirming germinal centre as the site of SBS9 acquisition.
- SBS7a in memory T cells correlates with more differentiated T cell epigenomes, supporting accumulation of UV damage during post-differentiation skin residency.

### Positive selection

- Exome-wide dN/dS ratio in lymphocytes: 1.12 (95% CI 1.06–1.19), implying ~11% (95% CI 6–15%) of non-synonymous mutations confer a selective advantage and drive clonal expansions.
- At single-gene resolution, only *ACTG1* was statistically significant after multiple testing correction (q=5×10⁻³); recurrently mutated in multiple myeloma.

### Structural variation

- Structural variation 16-fold higher in lymphocytes than stem cells; ~15% of deletions attributable to off-target RAG recombinase activity.
- 1,037 SVs found across 635 lymphocyte genomes; 85% in Ig-TCR regions.
- Non-Ig-TCR SVs: ~17% of lymphocytes carry at least one off-target SV (vs ~13% of HSPCs). Memory B and T cells have higher SV burdens than naive counterparts.
- 24% of non-Ig-TCR SVs are RAG-mediated (full RSS or heptamer within 50 bp of breakpoint); 84% of Ig-TCR SVs are RAG-mediated.
- On-target CSR enriched in memory B cells (76%) vs naive B cells (12%).
- Complex events (chromoplexy, templated insertions) observed occasionally.
- ~15% of non-Ig-TCR deletions affect genes recurrently mutated in lymphoid malignancies (e.g. CREBBP).

### Comparison with malignancy

- SNV and SV burdens of Burkitt lymphoma, mutated CLL, and unmutated CLL fall within the range of normal lymphocytes; follicular lymphoma, DLBCL, and multiple myeloma have higher SNV burdens but still broadly similar signature profiles.
- The vast majority of B-cell lymphoma mutations can be attributed to the same mutational processes active in normal memory B cells (SBSblood, SBS1, SBS8, SBS9), in broadly similar proportions.
- SBS9-enriched genes in normal memory B cells (top 1%) overlap substantially with SBS9-enriched genes in 5 post-germinal malignancies.
- ~10% of normal lymphocytes carry a non-Ig-TCR RAG-mediated SV; across lymphoid malignancies, the absolute numbers of RAG-mediated SVs (≥0.5 per lymphoma) are broadly comparable to those in normal lymphocytes except in ALL (much higher).

## Relevance

This paper establishes a quantitative baseline for somatic mutation burden and mutational-signature composition in non-malignant lymphocytes, providing critical reference data for interpreting signatures observed in lymphoid cancer cohorts (e.g., CLL, DLBCL, multiple myeloma studies in cBioPortal). Key connections to this project:

- **Hypothesis h08 (mutational-signature aetiology inference):** The paper definitively characterises which signatures are endogenous/clock-like (SBSblood, SBS1) vs lymphocyte-differentiation-associated (SBS9, SHM off-target) vs exogenous/environmental (SBS7a UV, SBS17b) in normal tissue. This provides a causal interpretive layer for signature decompositions in cross-study cBioPortal analyses: a signature like SBS9 elevated in a lymphoma study reflects the germinal-centre biology of the cell of origin, not a de novo cancer-specific process.
- **Normal-tissue baseline for cross-study comparisons:** Mutation rates per cell type (15–25 SNVs/year) quantify the expected background somatic load in lymphoid cells before malignant transformation. This is directly relevant when interpreting mutation-frequency tables in cBioPortal CLL/lymphoma studies.
- **Immune-cell confounding in pan-cancer analyses:** Tumour-infiltrating lymphocytes in non-lymphoid tumour biopsies could contribute SBSblood, SBS9, or SBS7a to bulk sequencing profiles. This paper documents the expected signature contribution from normal lymphocytes.
- **SBS17b (potential chemotherapy-associated signature):** The paper shows SBS17b can arise independently of treatment in normal memory cells, which is directly relevant when trying to attribute SBS17b in cBioPortal cohorts to prior 5-FU exposure vs inherent biology.
- **Group H_normgerm:** This is the canonical normal-germinal-centre / normal-lymphocyte reference paper for the project's mutational-signature interpretation framework.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBSblood (novel endogenous blood signature) | Background/clock-like endogenous signature in haematopoietic cells | Distinct from SBS5 but high cosine similarity (0.87); may co-occur with SBS1 in HSPC-derived normal cells |
| SBS9 (germinal centre signature) | Differentiation-associated lymphocyte signature | Key confounder for B-cell malignancy cross-study comparison; correlates with SHM rate |
| SBS7a (UV signature) | Exogenous environmental signature | Expected in memory T cells from skin-resident population; relevant to cutaneous T-cell lymphoma studies |
| SBS17b (5-FU-like signature) | Ambiguous exogenous/microenvironmental signature | Present in normal memory cells without chemotherapy exposure — cannot be used as unambiguous treatment marker |
| Off-target SHM / RAG SVs | Immunological off-target mutagenesis | Accounts for ~50% of excess differentiation-associated mutations; mechanistically distinct from replication errors |
| dN/dS > 1.0 in normal lymphocytes | Positive selection on somatic variants in non-malignant tissue | 11% non-synonymous mutations estimated to confer selective advantage; only ACTG1 significant at gene level |

## Limitations

- Single-cell colony expansion requires ~2–5% culture efficiency; cells that fail to expand are excluded, introducing potential selection bias. The authors show surface marker expression is similar between colony-forming and non-colony-forming cells, but functional differences cannot be fully excluded.
- Relatively small number of donors (4 main donors for all cell types, with supplementary donors for tonsil and cord blood) limits generalisation. Between-person variation is small relative to within-person variation, but rare population-level effects could be missed.
- WGS at ~20x depth gives sensitivity of ~80% at 10x; some low-VAF clonal expansions may be missed.
- SBS9 mechanistic interpretation (polymerase eta translesion synthesis during replicative stress) is a well-supported hypothesis but not directly proven — the paper cannot exclude AID contribution via an indirect mechanism.
- The study covers lymphocytes from peripheral blood, spleen, bone marrow, and tonsil but does not systematically sample lymph nodes, gut-associated lymphoid tissue, or other tissue-resident compartments where microenvironmental signatures (e.g., SBS17b in GI mucosa) may be enriched.
- Signature SBSblood is novel and defined in this dataset; its relationship to COSMIC SBS5 (cosine similarity 0.87) means it may be collapsed with SBS5 in studies using standard COSMIC decomposition, potentially obscuring blood-specific effects.

## Model / Tool Availability

- Code and statistical analyses: https://github.com/machadoheather/lymphocyte_somatic_mutation
- Raw sequencing data: European Genome-Phenome Archive, accession EGAD00001008107
- All somatic mutation calls and intermediate data: same GitHub repository

## Follow-up

- **Machado2021** (already summarised): companion paper on genome-wide mutational signatures in immunological diversification — overlapping cohort, complementary focus on the SHM/RAG off-target contribution in detail.
- Mitchell et al. 2022 (Nature, same volume): companion HSPC paper sharing 39 overlapping HSPC genomes from this cohort — provides the HSPC baseline used here.
- Osorio et al. 2018 (Cell Rep): earlier single-cell B-cell mutation characterisation (59 normal CD19+ B cells) — predecessor that motivated this larger study.
- Lee-Six et al. 2018 (Nature): normal blood somatic mutation accumulation in HSCs — methodological predecessor.
- **Key open question for this project:** Do the SBS9 and SBSblood proportions seen in cBioPortal lymphoma studies track with known cell-of-origin subtypes (GCB vs ABC DLBCL), and does the ratio of SBS9 to SBS1/SBSblood serve as a quantitative proxy for germinal-centre exposure?
- **Key open question:** Can the UV signature (SBS7a) burden in cBioPortal cutaneous T-cell lymphoma studies be used to rank patients by cumulative sun exposure, and does this correlate with clinical variables?
