---
id: "paper:Shaffer2008"
type: "paper"
title: "IRF4 addiction in multiple myeloma"
status: "active"
ontology_terms:
  - multiple myeloma
  - IRF4
  - lineage addiction
  - nononcogene addiction
  - transcription factor dependency
  - plasma cell differentiation
  - MYC
  - RNA interference
  - loss-of-function screen
  - gene expression profiling
  - chromatin immunoprecipitation
datasets: []
source_refs:
  - "cite:Shaffer2008"
related:
  - "topic:lineage-addiction-and-cell-of-origin-driver-specificity"
  - "question:q042-driver-normal-expression-tissue-cell-type-specificity"
  - "discussion:2026-06-07-tissue-cell-type-specificity-of-cancer-drivers"
  - "paper:Garraway2006"
created: "2026-06-07"
updated: "2026-06-07"
---

# IRF4 addiction in multiple myeloma

<!--
- **Authors:** Arthur L. Shaffer, N. C. Tolga Emre, Laurence Lamy, Vu N. Ngo, George Wright, Wenming Xiao, John Powell, Sandeep Dave, Xin Yu, Hong Zhao, Yuxin Zeng, Bangzheng Chen, Joshua Epstein, Louis M. Staudt
- **Year:** 2008
- **Journal:** Nature 454(7201):226-231
- **DOI:** 10.1038/nature07064
- **PMID:** 18568025
- **PMCID:** PMC2542904
- **BibTeX key:** Shaffer2008
- **Source:** PMC full text (web fetch via pmc.ncbi.nlm.nih.gov)
-->

## Key Contribution

Using a doxycycline-inducible shRNA loss-of-function screen across multiple myeloma (MM) subtypes, Shaffer et al. show that myeloma cells are universally dependent on the transcription factor IRF4 for survival — despite IRF4 being unmutated and unamplified in ~90% of cases. The study frames this as "nononcogene addiction": MM cells co-opt a master plasma-cell-differentiation program that is an obligate part of normal B-cell biology, not a classically mutated driver. A key mechanistic discovery is an IRF4↔MYC autoregulatory positive-feedback circuit in which each factor directly binds and transactivates the other, creating a self-reinforcing transcriptional network that is aberrantly maintained in myeloma.

## Methods

**Loss-of-function RNAi screen.** Doxycycline-inducible retrovirally delivered shRNAs targeting IRF4 were introduced into three myeloma cell lines representing distinct oncogenic subtypes: KMS12 (CCND1 translocation), H929 (FGFR3/MMSET translocation), and SKMM1 (MAFB/IRF4 translocations). Competitive growth assays were used to measure depletion of shRNA-expressing cells relative to uninfected controls. Five lymphoma cell lines served as non-myeloma controls.

**Gene expression profiling.** Agilent microarrays and Lymphochip arrays were used to identify IRF4-dependent transcriptional programs following shRNA knockdown, and to compare IRF4 targets against a reference panel of primary myeloma samples (n=451) vs. normal B cell stages (activated B cells, plasma cells).

**Genome-wide ChIP-chip.** Chromatin immunoprecipitation followed by hybridization to Agilent Human Promoter Set microarrays (~17,574 genes) in KMS12 (myeloma) and OCI-Ly19 (lymphoma) cells mapped direct IRF4 binding across the genome. Quantitative PCR ChIP validated 22 selected loci.

**IRF4 mutation/amplification survey.** Resequencing of IRF4 coding exons and copy-number analysis was performed across 10 myeloma cell lines.

## Key Findings

**Universal myeloma dependency, subtype-independent.** IRF4 shRNA depleted myeloma cells 2- to 8-fold relative to uninfected competitors within days of induction, and was toxic across all three MM subtypes tested regardless of their distinct primary oncogenic lesion (translocation type, RAS mutation status, TP53/CDKN2C status). Five lymphoma lines were largely unaffected, except OCI-Ly3 (activated B cell-like diffuse large B-cell lymphoma), establishing selectivity for MM over most B-cell malignancies.

**IRF4 is not genetically altered in most myelomas.** Sequencing of 10 myeloma lines found wild-type IRF4 in 9/10; one line showed a heterozygous missense mutation of unknown significance. No IRF4 locus amplifications were detected beyond the known SKMM1 translocation. The dependency is therefore an expression/network phenomenon, not a classical mutational driver.

**IRF4 controls 308 target genes that define the myeloma expression program.** Gene expression profiling after IRF4 knockdown identified 308 downregulated genes. These targets were significantly enriched for genes highly expressed in primary myeloma versus normal mature B cells (p=0.002). Notably, IRF4 targets fused two normally distinct regulatory programs: ~27% were upregulated in activated B cells (not plasma cells), and ~17% were characteristic of plasma cells (not activated B cells) — an aberrant hybrid state not present in any normal B-lineage stage.

**IRF4→MYC direct regulation.** Genome-wide ChIP-chip identified 558 direct IRF4-bound loci in myeloma cells but not lymphoma cells; 35 overlapped with downregulated genes after IRF4 knockdown (p=1.0×10⁻¹⁶). MYC was a direct target: IRF4 bound the MYC promoter ~1.6 kb upstream of the transcriptional start site, IRF4 knockdown reduced MYC mRNA >2-fold in myeloma lines, and ectopic IRF4 in lymphoma cells increased MYC mRNA. The same IRF4→MYC binding was observed in mitogen-activated primary B cells after 3-20 hours of stimulation.

**MYC→IRF4 reciprocal feedback (the autoregulatory circuit).** MYC knockdown decreased IRF4 expression in myeloma cells. ChIP demonstrated direct MYC binding within the IRF4 first intron in MYC-expressing myeloma lines (KMS12, H929) but not in the low-MYC line U266 (which instead expresses MYCL1). In primary myeloma samples, MYC and IRF4 mRNA showed significant positive correlation across 451 samples (r=0.24, p=2.5×10⁻⁷). This creates a self-sustaining positive feedback loop: any genetic event that elevates MYC (translocation, copy gain) will drive IRF4 expression, which in turn sustains MYC — locking cells into the hybrid activation/differentiation program.

**Cell death mechanism is multi-factorial.** IRF4 knockdown caused cell death (elevated sub-G1 fraction) within 3 days with no major cell-cycle arrest, and loss of many essential gene products simultaneously (CDK6, STAG2, metabolic enzymes LDHA/HK2/PDK1, mitochondrial components, telomere maintenance factors BMI1/TERT, differentiation regulator PRDM1/Blimp-1). The authors term this "death by a thousand cuts."

**Therapeutic window.** Mice lacking one IRF4 allele are phenotypically normal; ~50% knockdown was sufficient to kill myeloma cells in vitro, suggesting selective targeting may be achievable.

## Relevance

This paper is the canonical primary example for a key theme emerging in our project: **cancer-type-specific driver dependencies that arise from lineage identity rather than from somatic mutation of the dependency gene itself**.

**Direct parallel to hypothesis:h12 (expression-not-mutation).** Our cbioportal pipeline is mutation-centric — it queries somatic variant frequencies. IRF4 exemplifies a class of cancer vulnerabilities that are entirely invisible to mutation-frequency analysis: IRF4 is not recurrently mutated in MM (9/10 lines wild-type), yet it is the single most critical dependency across all MM subtypes. A pipeline that ranks genes by mutation recurrence would place IRF4 near background in myeloma data, missing what is arguably the disease's defining molecular vulnerability. This sharply illustrates the **ceiling of mutation-only analysis** for identifying actionable dependencies.

**Nononcogene addiction as a distinct driver class.** The paper explicitly coins the term "nononcogene addiction" to distinguish this from classical oncogene/TSG driver logic. In our project's driver-vs-biomarker framing: IRF4 is a dependency/biomarker, not a classically mutated driver. It would not be flagged by any recurrence-based statistical test (MutSigCV, dN/dS, etc.) applied to our aggregated cBioPortal data. This is a concrete instance where the "driver" designation requires functional screens, not just somatic mutation tallies.

**Lineage program as cancer vulnerability.** The mechanism — co-option of a normal lineage-specification transcription factor — is precisely the "cell-of-origin determines dependency" principle. Plasma cells require high IRF4 for their identity and function; MM cells inherit this requirement and cannot escape it. The parallel to MITF dependency in melanoma (Garraway 2006) is direct: both are cases where the cancer cell is "addicted" to the master transcription factor that specifies its normal cell-of-origin.

**IRF4-MYC circuit as a model for mutation-amplified expression dependencies.** Even though IRF4 is not mutated, the MYC↔IRF4 feedback loop explains why MYC-activating events (translocations, copy gains — which ARE detectable in our pipeline) would amplify IRF4 activity without altering IRF4 sequence. This is a mechanistic example of how a mutational event in one gene (MYC) creates a dependency on a second gene (IRF4) that would only be apparent through expression or functional data.

**Relevance to cross-cancer generalization.** The finding that IRF4 dependency is MM-specific (lymphomas mostly spared) illustrates the cell-type restriction of lineage dependencies — exactly the tissue/cell-type specificity dimension we are exploring in our cross-cancer comparisons.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Nononcogene addiction | Lineage dependency (not mutation-driven) | Distinct from the somatic-mutation-based drivers our pipeline detects |
| IRF4 (unmutated dependency) | Expression biomarker / functional dependency | Invisible to cBioPortal mutation-frequency analysis |
| IRF4-MYC autoregulatory circuit | Mutation-amplified expression network | MYC mutations/translocations visible in our data; IRF4 upregulation is the downstream consequence |
| Subtype-independent toxicity despite molecular heterogeneity | Cross-study recurrence | Analogous to our interest in gene-cancer associations that recur across studies; here functional rather than mutational recurrence |
| Plasma-cell lineage program | Cell-of-origin identity | Shapes which dependencies are operative, independent of somatic mutation burden |
| "Death by a thousand cuts" | Multi-target simultaneous loss | Distinguishes master-regulator knockdown from single-gene knockouts |

## Limitations

**No primary patient tumor functional validation.** The loss-of-function screen was conducted in cell lines (3 MM lines, 5 lymphoma lines); the claim of universal dependency relies on this limited panel plus expression correlations in primary tumors (n=451 for the MYC-IRF4 correlation).

**Cell-line biology may not fully recapitulate tumor biology.** The myeloma microenvironment (bone marrow niche, cytokine signals) is absent; IRF4 dependency in vivo may be modulated by stromal factors.

**IRF4 target gene network of 308 genes is knockdown-defined, not necessarily direct.** Only 35 of these were confirmed as direct IRF4 binding targets by ChIP-chip; the majority may reflect indirect regulatory cascades that are downstream of primary IRF4 targets (e.g., via MYC).

**The "nononcogene addiction" framing is conceptual.** The paper does not rule out that rare IRF4 mutations or epigenetic alterations could cooperate; the resequencing of 10 lines is not a population-scale mutation survey.

**Therapeutic translation.** IRF4 is a transcription factor with no ligand-binding domain; direct pharmacological inhibition remains highly challenging. The ~50% knockdown therapeutic window estimated from IRF4-haploinsufficient mice is a rodent model extrapolation.

## Model / Tool Availability

This paper does not release a computational tool or model. Gene expression data from the primary myeloma cohort (n=451 samples) was presumably deposited in GEO (accession numbers referenced in the PMC article but not captured here). ChIP-chip data may also be available via GEO. No software artifact is described.

## Follow-up

**Papers to read next:**
- Garraway et al. 2006 (Nature) — MITF lineage survival oncogene in melanoma; the conceptual parallel to IRF4 in MM; referenced in `related`
- Bhatt et al. / later IRF4 inhibitor papers — subsequent pharmacological efforts to target the IRF4-MYC axis
- Hollenhorst et al. on ETS factors in prostate cancer — another lineage-TF addiction example
- Weinstein 2002 (Science) — original "oncogene addiction" framing that Shaffer2008 extends to nononcogene addiction

**Questions this raises for our project:**
- `question:q042-driver-normal-expression-tissue-cell-type-specificity` — What fraction of known cancer vulnerabilities are expression/lineage dependencies that are mutation-invisible? Can we estimate the "missed" dependency rate from our mutation-only data?
- How often does a recurrently mutated gene in our cBioPortal data (e.g., MYC amplification in MM) act primarily through upregulating an unmutated dependency (like IRF4) rather than through the mutated gene's own protein function?
- Are there other lineage-TF → MYC autoregulatory circuits in other cancer types detectable from co-expression in our cross-study data?
- Does the absence of recurrent IRF4 mutation in MM (vs. IRF4 translocation in DLBCL) represent a generalizable pattern: some cancer types acquire dependency through expression/network rewiring while related cancer types use mutational activation of the same gene?
