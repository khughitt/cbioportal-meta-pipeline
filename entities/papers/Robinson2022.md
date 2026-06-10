---
type: paper
title: Inherited MUTYH mutations cause elevated somatic mutation rates and distinctive
  mutational signatures in normal human cells
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Robinson2022
ontology_terms:
- mutational signatures
- MUTYH-associated polyposis
- base excision repair
- somatic mutation
- normal tissue
- reactive oxygen species
- SBS18
- SBS36
datasets: []
source_refs:
- cite:Robinson2022
related:
- paper:LeeSix2018
- paper:Martincorena2018
---

# Inherited MUTYH mutations cause elevated somatic mutation rates and distinctive mutational signatures in normal human cells

- **Authors:** Philip S. Robinson, Laura E. Thomas, Federico Abascal, Hyunchul Jung, Luke M. R. Harvey, Hannah D. West, Sigurgeir Olafsson, Bernard C. H. Lee, Tim H. H. Coorens, Henry Lee-Six, Laura Butlin, Nicola Lander, Rebekah Truscott, Mathijs A. Sanders, Stefanie V. Lensing, Simon J. A. Buczacki, Rogier ten Hoopen, Nicholas Coleman, Roxanne Brunton-Sim, Simon Rushbrook, Kourosh Saeb-Parsy, Fiona Lalloo, Peter J. Campbell, Iñigo Martincorena, Julian R. Sampson, Michael R. Stratton
- **Year:** 2022
- **Journal:** Nature Communications
- **DOI/URL:** https://doi.org/10.1038/s41467-022-31341-0
- **BibTeX key:** Robinson2022
- **Source:** PDF

## Key Contribution

Whole-genome sequencing of individual normal intestinal crypts from 10 individuals with biallelic germline *MUTYH* mutations (MUTYH-Associated Polyposis; MAP) shows that inherited BER deficiency elevates the somatic base-substitution rate 2–4-fold (median; one outlier 31-fold) above wild-type, and does so through a characteristic combination of COSMIC signatures SBS18 (ROS damage) and SBS36 (defective MUTYH function), both dominated by C>A transversions. The elevated rate in histologically normal cells directly explains the increased colorectal cancer predisposition in MAP, and demonstrates that cells tolerate substantially elevated somatic mutation burdens without premature ageing.

## Methods

- **Cohort:** 10 individuals aged 16–79 with biallelic *MUTYH* germline mutations (five missense homozygotes MUTYH^Y179C+/+^, one MUTYH^G286E+/+^, three compound heterozygotes MUTYH^Y179C+/−G396D+/−^, two homozygous truncating MUTYH^Y104*+/+^); all had ≥10–100 colonic adenomas.
- **Tissue sampling:** 144 individual normal intestinal crypts (LI n=107, SI n=37) from MAP individuals by laser-capture microdissection; 13 adenoma glands from 5 individuals; peripheral blood and tissue lymphocytes from a subset.
- **Sequencing:** Bespoke low-input DNA library preparation from microdissected material; paired-end Illumina WGS at mean 28-fold coverage; duplex NanoSeq for blood/lymphocyte bulk samples.
- **Mutation calling:** CaVEMan (SBS) and Pindel (ID); germline filtering using an unmatched normal synthetic BAM; sensitivity corrected by simulation.
- **Signature extraction:** Hierarchical Dirichlet Process (HDP) de novo extraction (9 components N0–N8); decomposed into COSMIC references; validated with SigProfiler (NMF). Three novel components N1–N3 extracted; N1 and N3 mapped to SBS18/SBS36; N2 (abundant only in outlier PD44890) mapped to SBSOGG1 (OGG1-deletion signature).
- **Phylogenetic analysis:** MPBoot trees per individual; mutations mapped to branches; signature contributions per branch estimated using sigfit.
- **Control cohort:** Reprocessed wild-type normal crypts (n=445) from Lee-Six et al. 2018 using identical pipeline for direct comparison.
- **Cancer driver mutations:** dNdScv and MutationMapper hotspot/truncating analysis on crypt and adenoma samples.

## Key Findings

1. **Elevated SBS mutation rate in MAP normal crypts:** Median SBS burden 2294–33,350 per crypt (92–1446 SBS/year), compared to ~46 SBS/year in wild-type. Linear mixed-effects model: 2–4-fold increase for most MAP genotypes (95% CI 69–1520 SBS/yr); one outlier individual (PD44890, MUTYH^Y179C+/−G396D+/−^ + biallelic *OGG1* germline variants) exhibited 31-fold elevation (~25 SBS/yr vs 19 SBS/yr modelled for wild-type normalised by sensitivity; equivalently a "mutational age" of ~500 years).
2. **Mutational signatures SBS18 and SBS36 drive excess burden:** Four reference signatures identified in all MAP samples: SBS1, SBS5, SBS18, SBS36. The excess mutations are almost entirely attributable to SBS18 (ROS/8-oxoguanine damage) and SBS36 (defective MUTYH activity), both characterised by C>A mutations. SBS18 predominated in MUTYH^Y179C+/−G396D+/−^ individuals (n=85 crypts); SBS36 was proportionally higher in truncating MUTYH^Y104*+/+^ and MUTYH^G286E+/+^ genotypes.
3. **Novel signature N2 (= SBSOGG1):** Present almost exclusively in the outlier individual PD44890, who carried biallelic *OGG1* germline missense variants; characterised by C>A at GCA and CCA trinucleotides. Consistent with experimental OGG1 deletion signature, this signature reflects non-excised 8-oxoguanine accumulation when both OGG1 and MUTYH are defective.
4. **Adenoma mutation burdens ~2-fold above matched normal crypts:** The mutation rate is further increased during neoplastic transformation, with SBS18 and SBS36 remaining dominant, consistent with elevated BER-deficiency-driven mutational activity continuing during early carcinogenesis.
5. **Candidate cancer driver mutations enriched in MAP normal crypts:** Putative driver mutations in 15% of crypts (22/144), vs 6% in wild-type controls; 16/22 were nonsense mutations; the elevated truncation rate reflects the higher SBS burden and the proclivity of defective MUTYH to generate protein-truncating mutations at specific trinucleotides.
6. **Elevated mutation rates in non-intestinal cell types:** Peripheral blood granulocytes showed elevated SBS18+SBS36 rates (25 SBS/yr vs 19 SBS/yr in wild-type; P=10^−7^); tissue lymphocytes showed more modest elevation (53 vs 40 SBS/yr; P=0.01). SBS mutation rate of MAP-associated processes is ~13-fold (CI 10–17) higher in intestinal epithelium than in blood, consistent with tissue-specific ROS exposure.
7. **No evidence of premature ageing:** Despite ubiquitously elevated mutation rates — including a "mutational age" equivalent of ~500 years in the most extreme individual — no individual exhibited overt functional decline or phenotypic features of premature ageing, confirming that somatic mutation accumulation alone is not sufficient to drive global organismal ageing.
8. **Colibactin signature (SBS88) in a subset of crypts:** Detected in crypts from the 16-year-old outlier PD44890, linked to mutagenic *E. coli* strains in the colonic microbiome; not MUTYH-related.
9. **Genotype-phenotype correlation:** Different MUTYH genotypes confer different absolute mutation rate increases (MUTYH^Y104*+/+^ > MUTYH^Y179C+/+^ > MUTYH^G286E+/+^), and severity of clinical phenotype (adenoma count, cancer onset age) correlates with elevation of mutation rate.

## Relevance

**h08 (agnostic covariate ↔ signature-exposure association; positive-control recovery):**

This paper is directly relevant to the h08 positive-control arm (H08a). It provides a well-powered, mechanistically validated exemplar of a germline BER-deficiency exposure (biallelic *MUTYH* mutation) producing a quantitatively and qualitatively distinctive mutational signature in tissue. Key connections:

- **Known exposure → known signature:** MUTYH deficiency → SBS36 is one of the cleanest aetiology assignments in the COSMIC catalogue, complemented by SBS18 (ROS). This paper provides the mechanistic validation for the exposure-signature link at near-single-cell resolution in normal tissue, which is exactly the kind of ground-truth exemplar that should be recoverable by an agnostic covariate-signature scan — if such a scan were run across cBioPortal studies that include MAP individuals or hereditary polyposis cohorts.
- **Tissue-specificity of signature rates:** The 13-fold enrichment of SBS18/SBS36 activity in intestinal epithelium vs blood illustrates that tissue-of-origin is a critical modifying covariate for signature exposure, consistent with h08 Prediction 4 (associations attenuate when tissue is not conditioned on). A naive cross-tissue association would confound tissue-specific ROS with MUTYH genotype.
- **Genotype as a germline covariate:** The graded mutation rate across MUTYH genotypes (truncating > missense homozygous > compound heterozygous with partial activity) demonstrates that germline variant status is a high-signal covariate that an agnostic scan should rank near the top of any cBioPortal-wide association when MUTYH status is captured.
- **Normal-tissue background vs tumour signal:** This paper works entirely in histologically *normal* cells, making it complementary to tumour-focused cross-study meta-analysis. It establishes the baseline elevated mutation burden that MAP individuals carry into malignant transformation, relevant to the pipeline's clonal hematopoiesis contamination correction (matched normal sequencing may itself carry elevated SBS18/SBS36 signal in MAP carriers).

**Cross-study meta-analysis:**

In the cBioPortal context, MAP/MUTYH-associated colorectal cancer cohorts (e.g. individual MAP studies or TCGA CRC) will show elevated SBS18/SBS36. Any aggregated gene-cancer mutation frequency table that includes MAP-enriched cohorts without flagging MUTYH germline status risks confounding: genes with C>A hotspots at specific trinucleotide contexts (e.g. ACA, CCA for OGG1-related) will be spuriously elevated. The pipeline's existing `annotate_ch.py` logic and hypermutator annotation pipeline address part of this, but germline repair-deficiency is a distinct category not currently captured by the `ch_priority_gene` list or the TMB-based hypermutator flags.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS18 (ROS/8-oxoguanine damage) | COSMIC SBS18 | Positive-control signature for h08 aetiology recovery |
| SBS36 (defective MUTYH function) | COSMIC SBS36 | MUTYH-specific signature; C>A dominant |
| SBSOGG1 (OGG1-deletion signature) | Novel / COSMIC-catalogued | Relevant only to biallelic OGG1+MUTYH deficiency |
| Biallelic MUTYH germline status | Germline covariate | Not currently tracked in cBioPortal pipeline config |
| ~13× tissue-specific SBS rate enrichment | Tissue-stratification requirement | Supports within-tissue conditioning for h08 |
| Candidate driver mutations in normal crypts | Pre-malignant driver signal (h06) | 15% crypts with driver mutations; relevant to h06 |
| HDP signature extraction | De-novo extraction method | Alternative to SigProfiler NMF; used in normal-tissue studies |

## Limitations

- Cohort is small (n=10 individuals, n=144 crypts) and biased toward colorectal phenotype. Non-intestinal tissues sampled (blood, lymphocytes) show smaller effect sizes; systematic multi-tissue sampling across MAP individuals was not performed.
- The outlier individual PD44890 (31-fold elevation, biallelic OGG1 + MUTYH) is exceptional and not representative of MAP phenotype; some conclusions about N2/SBSOGG1 signature are based on a single individual.
- Wild-type control crypts (Lee-Six et al. 2018) were sequenced at lower coverage (16-fold vs 28-fold for MAP); sensitivity correction was applied, but differential coverage may introduce residual bias in fold-change estimates.
- The study does not directly sequence matched tumours from the same individuals, so causal attribution of the elevated normal-crypt burden to cancer predisposition remains inferential (albeit strongly supported).
- MAP is a rare Mendelian syndrome; the direct translational applicability to common MUTYH heterozygous carrier status (which shows modest cancer risk) is not resolved by this data.

## Model / Tool Availability

- Code/software: https://github.com/PhilipSRobinson/mutyh; https://doi.org/10.5281/zenodo.6504797
- Raw WGS data: European Genome-Phenome Archive (EGA), accessions EGAD00001007958 and EGAD00001007997 (controlled access via WTSI CGP Data Access Committee)
- Mutation calling pipelines: https://github.com/cancerit; filtering code at https://github.com/TimCoorens/Unmatched_NormSeq
- Mutational signature software: https://github.com/nicolaroberts/hdp and https://github.com/kgori/sigfit

## Follow-up

- SBS36 and SBS18 as positive-control signatures for h08: verify that any cBioPortal cohort with MAP patients or hereditary colorectal polyposis labels shows elevated SBS36/SBS18 in within-tissue association scans.
- Interaction between MUTYH germline status and the pipeline's hypermutator annotation: MAP carriers at 2–4-fold elevated burden will not be flagged as hypermutators by GMM or absolute-TMB criteria (the elevation is modest); check whether matched-normal sequencing from MAP carriers inflates the unmatched-normal false-positive rate in mutation calling.
- Robinson et al. 2019 (Nat Commun) characterised *POLE*-exonuclease-domain mutation carriers in the same normal-tissue WGS framework — direct predecessor study in same lab/pipeline.
- Lee-Six et al. 2018 (LeeSix2018 in project) is the wild-type control dataset this study builds on — already summarised.
- The colibactin signature (SBS88) detected incidentally in PD44890's crypts intersects with microbiome-mutagenesis aetiology, a potential novel h08b discovery target.
