---
type: paper
title: Diverse oncogenes use common mechanisms to drive growth of major forms of human
  cancer
status: active
created: '2026-06-07'
updated: '2026-06-07'
id: paper:Kauko2025
ontology_terms:
- oncogene convergence
- ribosome biogenesis
- translation
- MYC
- NOLC1
- phosphoproteomics
- pan-cancer
- growth signaling
- tissue specificity
- transcription factor
- cell proliferation
- cancer hallmarks
source_refs:
- cite:Kauko2025
related:
- topic:lineage-addiction-and-cell-of-origin-driver-specificity
- question:0042-driver-normal-expression-tissue-cell-type-specificity
- discussion:0008-tissue-cell-type-specificity-of-cancer-drivers
- paper:Haigis2019
- paper:Sack2018
---

# Diverse oncogenes use common mechanisms to drive growth of major forms of human cancer

- **Authors:** Otto Kauko, Mikko Turunen, Päivi Pihlajamaa, Antti Häkkinen, Rayner M.L. Queiroz, Mirva Pääkkönen, Sami Ventelä, Massimiliano Gaetani, Susanna L. Lundström, Antonio Murgia, Biswajyoti Sahu, Johannes Routila, Gong-Hong Wei, Heikki Irjala, Julian L. Griffin, Kathryn S. Lilley, Teemu Kivioja, Sampsa Hautaniemi, Jussi Taipale (corresponding)
- **Year:** 2025
- **Journal:** Science Advances
- **DOI:** 10.1126/sciadv.adt1798
- **BibTeX key:** Kauko2025
- **Source:** PDF

## Key Contribution

Diverse lineage-specific oncogenes — spanning oncogenic transcription factors (ER, AR, ERG, TCF4/β-catenin, GLI1, PAX3, FLI1) and kinase-activating mutations (BRAF, RAS, EGFR, ERBB2, PIK3CA, BCR-ABL) across breast, prostate, colorectal, lung, rhabdomyosarcoma, Ewing's sarcoma, and CML — converge on a small common set of downstream growth-regulatory mechanisms: primarily **translation and ribosome biogenesis**, orchestrated through the **MYC oncogene** as a central master regulator, and through direct posttranslational phosphorylation of ribosome biogenesis factors. The gene regulatory network shared by diverse cancers has an **hourglass topology**: many upstream tissue-specific drivers funnel through a narrow waist of shared master regulators (MYC, CDK4/6 axis) and then diverge again into a large effector gene set. Critically, **NOLC1** (nucleolar and coiled-body phosphoprotein 1) is identified as a key convergent node regulated both transcriptionally by MYC and posttranslationally by kinase signaling, with both modes independently required for tumor cell proliferation.

## Methods

**Experimental system.** All primary datasets were generated in-house using consistent methodology. The study combined:

1. **ChIP-seq (transcription factor binding):** Six lineage-specific oncogenic TFs were profiled across cancer type–matched cell lines (estrogen receptor in breast cancer cells MCF-7; androgen receptor/ERG in prostate cancer VCaP; TCF4/β-catenin in colorectal cancer RKO/HCT116; GLI1/PAX3 in rhabdomyosarcoma SK-N-MC/CRL-2061; FLI1 in Ewing's sarcoma). ChIP-seq peaks were integrated with expression profiling (siRNA knockdown of each TF) and paralog-merged to identify convergent transcriptional targets.

2. **GWAS cross-validation:** Cancer-associated SNPs from the GWAS catalog (n = 7,796 SNPs across cancer traits) were ranked to independently corroborate ChIP-seq–derived convergent targets.

3. **Drug-resistant / drug-sensitive cell line pairs (kinase signaling arm):** Ten parental cancer cell lines were used (lung: NCI-H1975, A549; colorectal: RKO, HCT116, LoVo; breast: MCF-7, T47D, BT-474; CML: KBM-7/HAP1, K562), each driven by EGFR, BRAF/MAPK, PIK3CA/mTOR, ERBB2/CDK4/6, or BCR-ABL. CRISPR was used to engineer resistance mutations (PTEN KO, RB1 KO, NF1 KO, PIK3CA H1047R) creating drug-resistant derivatives for 10 parental–resistant pairs. Cells were treated with their cognate cytostatic kinase inhibitors (trametinib, osimertinib, lapatinib, palbociclib, temsirolimus, imatinib) at concentrations causing G1 arrest only in the parental line.

4. **Single-cell RNA-seq (scRNA-seq) time course:** Cells were pooled with unique TotalSeq-B barcodes per well, treated at varying drug concentrations and durations (0, 2, 6, 12, 24 hours), and profiled on a 10x Chromium platform. Gene expression was modeled as a function of drug concentration, time, cell cycle phase, and resistance genotype to decouple direct drug effects from cell cycle–secondary effects.

5. **Phosphoproteomics (MS3/SPS/TMT):** Early time points (30 min, 2 hours) before widespread transcriptional changes. >48,000 phosphopeptides identified across cell line pairs (median 19,771 per line) at <1% FDR. Pathway-level analysis using KEGG and CORUM complex databases.

6. **PISA assay (proteome integral solubility alteration):** Same three adherent cell line pairs (NCI-H1975, RKO, HCT116), five replicates each, 2- and 24-hour time points, identifying protein interaction/complex changes.

7. **Metabolomics (LC-MS):** Targeted polar metabolite profiling 24 hours post-treatment in eight cell line pairs.

8. **Human tumor proteomics:** Fresh-frozen biopsies of squamous cell carcinoma (SCC) of the tongue (HNSCC) cut into 500-µm serial slices parallel to the invasive front, analyzed by TMTPRO-labeled mass spectrometry to compare proliferative (invasive front) vs. less-proliferative (central tumor) compartments.

9. **CGE assay (competitive precision genome editing):** Used to functionally validate specific phosphorylation sites by introducing phosphoablating (alanine/phenylalanine) and phosphomimetic (aspartate/glutamate) mutations with silent "barcode" mutations for lineage tracing, measuring fitness effects over 8 days by read-count dropout.

## Key Findings

**1. Convergent transcriptional output — MYC is the central hub.**
Across six diverse lineage-specific oncogenic TFs, the most significant shared downstream targets are **MYC** (ranked #1–3 across analyses), **CDK4/6** (cell cycle entry), and **ROCK/LATS kinases**. This convergence was confirmed by two orthogonal approaches: ChIP-seq in cell lines and GWAS catalog SNPs from patients. Most shared transcriptional responses to kinase inhibitor treatment (identified by scRNA-seq) are MYC target genes. MYC downregulation precedes downregulation of its targets, confirming causal order.

**2. Translation and ribosome biogenesis are the primary convergent downstream programs.**
The most significantly enriched gene sets among convergent oncogenic transcriptional targets are:
- Ribosome biogenesis (p = 1×10⁻⁴⁸)
- Translation factors (p = 3×10⁻⁶)
- rRNA processing (p = 2.2×10⁻¹⁹)

These same processes are convergently regulated at the phosphoproteomic level within 2 hours of kinase inhibitor treatment, before cell cycle arrest or widespread transcriptional changes, establishing that posttranslational regulation precedes and reinforces transcriptional regulation.

**3. NOLC1 as the key integrative node.**
NOLC1 (and its paralog TCOF1) emerged as the most prominent common target regulated **both** transcriptionally by MYC and posttranslationally (phosphorylation of threonines 607/610 in NOLC1, S1410 in TCOF1) by oncogenic kinase signaling. CGE functional validation established that:
- Mutation of NOLC1 phosphorylation sites threonine 607/610 reduced cell proliferation (p = 0.0025)
- Mutation of the MYC binding E-box in the NOLC1 promoter reduced proliferation (p = 8.5×10⁻⁴)
- Both modes of regulation are independently required
- The phosphorylation site at threonine 607 is conserved from humans to Drosophila

**4. Feed-forward logic explains oncogene cooperation.**
The finding that both MYC (transcriptional) and RAS/MAPK (posttranslational) inputs are independently required for full NOLC1 activation provides a quantitative mechanistic explanation for classical MYC–RAS oncogene cooperation: neither alone can optimally activate the growth program; both are needed. This implies that in a given tissue, whichever is rate-limiting (MYC or kinase activity) will be the selective target for mutation.

**5. Hourglass network topology.**
The authors describe the architecture as hourglass-shaped: many diverse upstream oncogenic drivers → narrow waist of master regulators (MYC, CDK4/6) → large effector network (translation, ribosome biogenesis). The upstream diversity is tissue-specific (lineage-specific oncogenes); the waist and downstream effectors are shared across cancer types.

**6. Invasion/metastasis hallmarks are NOT convergent — they remain tissue-specific.**
Of the 10 Hanahan–Weinberg hallmarks, only the three proliferation-related ones (sustaining proliferative signaling, evading growth suppressors, enabling replicative immortality) showed convergent regulation. Invasion and metastasis showed no common transcriptional or phosphoproteomic signature, consistent with known organ-tropism patterns and tissue-specific invasion mechanisms.

**7. Human tumor validation.**
In human HNSCC biopsies, TCOF1 (and to a lesser extent NOLC1) expression co-localizes with the proliferative invasive front, not the central tumor or adjacent normal muscle, supporting clinical relevance. Ribosomal proteins, by contrast, are highest in adjacent normal muscle cells (high constitutive protein synthesis capacity), distinguishing the tumor-specific signature from general translational activity.

**8. Metabolic convergence.**
Concurrently with ribosome biogenesis changes, drug treatment reduced nucleotide monophosphates (UMP, AMP, GMP) and altered glycolytic flux in sensitive but not resistant lines, implicating oncogenic kinase signaling in metabolic reprogramming converging on anabolic support for ribosome production. HK2 phosphorylation at tyrosine 461 (not the previously described threonine 473) was functionally validated by CGE as required for proliferation.

**9. Scope covers ~46% of worldwide cancer mortality.**
The cancer types studied (breast, prostate, colorectal, lung, CML, rhabdomyosarcoma, Ewing's sarcoma, HNSCC) collectively account for roughly 46% of global cancer mortality, supporting generalizability.

## Relevance

This paper speaks directly to the central tension in the **question:0042 / tissue-specificity framing**: why do specific oncogenes associate so strongly with specific cancer types?

**Kauko et al. provide a convergence resolution to the tissue-specificity puzzle.** Their data shows that the downstream biology — the actual growth-driving mechanism — is largely shared: MYC upregulation → ribosome biogenesis/translation enhancement, flanked by kinase-mediated phosphorylation of the same targets. What is tissue-specific is *which upstream oncogene* is mutated, not *what it ultimately does to the cell*. This meshes with cell-of-origin models: a given tissue/lineage will have chromatin access (open enhancers) for its characteristic TFs (e.g., ER in breast, AR in prostate, TCF4/β-catenin in colon), making those oncogenic TFs "competent" to drive MYC upregulation in that cellular context. Another driver in the same tissue would need to be competent to bind those enhancers; a given oncogene may lack that competence in a different tissue because the relevant chromatin is closed.

**Relationship to paper:Haigis2019.** Haigis et al. (2019) stress that tissue-specificity of cancer drivers is the rule — KRAS mutations behave differently in lung vs. colon vs. pancreas, and the same mutant oncogene drives distinct cancers. Kauko et al. complement rather than contradict this view: the *upstream* biology is tissue-specific (which oncogene, and its immediate transcriptional wiring to tissue-specific enhancers), but the *downstream convergent growth program* is shared. Haigis et al.'s observation that tissue context shapes oncogene output maps onto the Kauko et al. hourglass: tissue-specificity lives in the wide upper funnel; the convergent biology lives in the narrow waist. Together these papers suggest a two-tier model: (tier 1) cell-of-origin/lineage context determines which driver can be activated and wired to enhance MYC; (tier 2) once wired, MYC and the ribosome biogenesis program are tissue-generic growth engines.

**Relationship to paper:Sack2018.** Sack et al. (2018) address why specific cancer types rely on specific metabolic programs. Kauko et al. show that metabolic reprogramming (glycolysis, nucleotide synthesis) converges downstream of diverse oncogenes via the same growth signaling axes, overlapping with the anabolic demands of elevated ribosome biogenesis. This consistency strengthens the Sack model while grounding it in a specific mechanistic chain (oncogenic kinase → phosphoproteome → ribosome/metabolic program).

**Implication for route-1/route-2 framing and question:0042:** If convergent downstream biology (MYC → ribosome biogenesis) is the common endpoint, then observing that a particular oncogene preferentially mutates in a particular cancer type may primarily reflect:
1. **Cell-of-origin chromatin accessibility**: which TF binding sites are open in the progenitor cell (the Kauko et al. ChIP-seq data shows that oncogenic TFs collaborate with tissue-specific co-factors at shared MYC enhancers).
2. **Quantitative rate-limiting constraints**: which leg of the MYC/kinase feed-forward loop is sub-saturating in a given cell type, making that node the selective bottleneck.

This **tempers** a strong "each tissue has its own distinct driver biology" reading. The paper suggests that tissue-specific driver selection reflects upstream accessibility and rate-limiting steps, not fundamentally divergent downstream mechanisms. The convergence finding does not eliminate tissue-specificity, but relocates it to the *cell-of-origin and chromatin* level rather than the effector level.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Lineage-specific oncogenic TFs | Driver gene tissue-specificity | The tissue-specific "upstream" leg of the hourglass |
| Hourglass network (many drivers → MYC waist → many effectors) | Route-1 / route-2 driver framing | Convergence at MYC is a single "waist" regardless of upstream route |
| MYC as master regulator / common node | Cancer driver; convergent effector | MYC is a frequent CNA driver in cBioPortal data; appears in Bailey2018 tier |
| NOLC1 phosphorylation node | Downstream effector target | Not a classical cancer driver gene; discovered through convergence analysis |
| Cell-of-origin chromatin accessibility | Lineage addiction / cell-of-origin specificity | Kauko et al. invoke tissue-specific co-factors at MYC enhancers |
| Invasion/metastasis — tissue-specific, no convergence | Tissue-specific cancer hallmarks | Consistent with organ-tropism literature |
| Cancer hyperbola (CNA vs. point mutations) | Mutation type patterns across cancer types | Feed-forward model explains why CNA (MYC) and point mutations (kinases) are complementary |

## Limitations

- **Cell-line–centric:** The drug-resistance model relies on introducing CRISPR-engineered resistance mutations, which creates artificial genetic backgrounds. Whether the resistance cells faithfully represent endogenous tumor heterogeneity is uncertain.
- **Limited cancer type coverage:** While 46% of mortality is represented, notably absent are pancreatic cancer (predominantly RAS-driven), ovarian cancer (frequent MYC amplification), hepatocellular carcinoma, melanoma, and bladder cancer. The authors acknowledge this and argue those cancers also converge on RAS/MYC axes, but this remains inferential.
- **ChIP-seq data reuse:** The TF ChIP-seq data for several cancer types (ER, AR, ERG, FLI1, GLI1/PAX3) were sourced from prior publications rather than newly generated. While internally consistent, batch effects across studies could inflate or deflate convergence estimates.
- **Convergence ≠ sufficiency:** Showing that MYC and ribosome biogenesis are common downstream outputs does not prove these are rate-limiting for tumorigenesis in all cases. Invasion, immune evasion, and other hallmarks are shown to be *not* convergent, which could mean that anti-proliferative therapies targeting the MYC/ribosome axis would face tissue-specific resistance mechanisms in those other dimensions.
- **Static vs. dynamic tumors:** All functional readouts are from cultured cells or a single HNSCC tumor model. Whether the convergence holds during tumor progression, metastasis, or therapy-adapted states was not examined.
- **Invasion/metastasis absence may be technical:** The authors acknowledge that the absence of common invasion/metastasis signals could reflect limitations of phosphoproteomic coverage (non-phosphorylation posttranslational regulation) rather than truly tissue-specific biology.
- **NOLC1 validation scope:** CGE functional validation was performed in HAP1 cells (near-haploid CML-derived); generalizability to epithelial cancer cell lines is shown indirectly by the proteomic/phosphoproteomic convergence data, but direct knockout validation in diverse cell lines was not shown.

## Model / Tool Availability

No standalone software tools or pre-trained models are released with the paper. CGE and ChIP-seq raw data are deposited in Gene Expression Omnibus (GEO) per standard Science Advances requirements. The CGE competitive fitness assay is described as a method published previously (Johnson et al.).

## Follow-up

**Papers to read next:**
- Bailey [@Bailey2018] — PanCanAtlas driver census; establishes the prior on tissue-specific driver frequencies; Kauko et al.'s convergence finding provides a downstream rationale for why those frequencies exist.
- Hanahan & Weinberg hallmarks papers (2000, 2011) — the Kauko framing explicitly maps to hallmarks.
- Paull et al. (master regulator computational approach) — Kauko et al. discuss and critique this work as identifying >400 master regulators, compared with their far fewer key nodes.

**Questions this raises for the project:**
- In our cBioPortal cross-study mutation frequency data, does MYC copy number gain co-occur with the same cancer types that have high frequencies of the lineage-specific oncogenic TFs (ER amplification in breast, AR amplification in prostate, etc.), consistent with the Kauko cooperative model?
- If kinase-pathway mutations and MYC amplifications are quantitatively cooperative (the "cancer hyperbola" argument), do our gene × cancer frequency matrices show a systematic anti-correlation or co-occurrence between RAS/MAPK pathway mutations and MYC copy number alterations within the same cancer type?
- For cancer types where we observe unusually high driver gene diversity (many different genes mutated at moderate frequency rather than one dominant driver), does the Kauko hourglass model predict that all those diverse genes still converge on MYC upregulation? This would predict they should all co-occur with MYC-target gene expression signatures.
