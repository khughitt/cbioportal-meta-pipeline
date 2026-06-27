---
type: paper
title: Dissecting DNA-mismatch-repair-driven mutational processes in human cells
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Owusu2025
ontology_terms:
- mutational signatures
- mismatch repair
- MMR deficiency
- CRISPR knockout
- somatic mutation
- microsatellite instability
datasets: []
source_refs:
- cite:Owusu2025
related: []
---

# Dissecting DNA-mismatch-repair-driven mutational processes in human cells

- **Authors:** Michel Owusu, Jorg Menche, Joanna Loizou, Donate Weghorn
- **Year:** 2025
- **Journal:** bioRxiv (preprint; posted 2025-02-12)
- **DOI/URL:** https://doi.org/10.1101/2025.02.10.637460
- **BibTeX key:** Owusu2025
- **Source:** PDF

## Key Contribution

Using CRISPR-Cas9 knockouts of canonical MMR genes (MLH1, MSH2, MSH6) in isogenic human HAP1 cells followed by whole-genome sequencing, this study provides direct experimental characterisation of the mutational signatures driven by MMR deficiency. The study identifies and mechanistically explains SBS57 — previously classified as a "possible sequencing artifact" in COSMIC — as an alignment artifact caused by the synergistic effect of germline SNPs and MMR-related indels near thymine repeat regions, linking it to tensor signature TS27. It also provides the first in vitro experimental evidence that MMR repairs 5-methylcytosine deamination (CpG>TpG), thereby contributing to SBS1 accumulation.

## Methods

**Experimental design:** CRISPR-Cas9 frameshift knockouts of eight genes in human haploid HAP1 cells — canonical MMR genes (MLH1, MSH2, MSH6) and associated/interacting genes (ARID1A, EXO1, SETD2, NSD1, SMARCA4). Single cells were clonally expanded for one month (baseline timepoint), then cultured for a further three months before re-expansion into three technical replicates (endpoint timepoint). De novo mutations were defined as endpoint variants absent from baseline.

**Sequencing and variant calling:** Whole-genome sequencing on Illumina NovaSeq 6000 (2×151 bp paired-end). Somatic variants called with consensus between Strelka2 and MuTect2; additional filters applied: mappability (CRG GEM Alignability 36-mers, ≤2 mismatches), repeat-region masking (RepeatMasker), and exclusion of variants within ±6 bp of deletions.

**Signature analysis:** Mutational profiles refitted to COSMIC v3.4 SBS and indel (ID) signatures by NNLS. Tensor signatures (Vohringer et al. 2021) used as an alternative decomposition framework. Replication timing data from ENCODE RepliSeq (median of 12 cell lines). Transcription strand annotations from GENCODE (GRCh38 v38).

**Tumour data analysis:** COSMIC signatures refitted to 2778 PCAWG and 4672 HMF tumour samples (WGS; >1000 mutations filter). SBS57-positive tumours identified with a stringent probabilistic criterion (simulation-derived thresholds); 134 qualifying samples clustered by PCA on COSMIC signature weights + k-means with silhouette thresholding, yielding four clusters (MMRd, POLEd, SBS17, SBS12) from 80 robustly clustered samples.

## Key Findings

**MMR-associated signatures recovered in vitro:** All seven COSMIC signatures currently associated with defective MMR (SBS6, SBS14, SBS15, SBS20, SBS21, SBS26, SBS44) were detected in the MLH1, MSH2, and MSH6 knockout cells. SBS44 had the highest individual contribution in MMRd cells. ARID1A, EXO1, SETD2, NSD1, and SMARCA4 knockouts did not produce the MMRd mutational phenotype.

**SBS57 is an alignment artifact in MMRd cells:** SBS57 (5–15% weight in MMRd cells with relaxed filters) is characterised by TTT>TCT and TTT>TGT mutations. IGV inspection revealed a three-feature mechanism: (1) a germline C/G SNP within <10 bp of the mutated site, (2) a small deletion within <10 bp of the same site, and (3) the site is at or near a thymine repeat boundary. This combination causes erroneous alignment-shift of the SNP in reads carrying both the SNP and the deletion, generating false-positive mutations. Applying the strict filter (consensus calling + repeat masking + ±6 bp deletion exclusion) completely removes SBS57 from MMRd KO cells. The same artifact also generates double-base substitution signature DBS14 when unfiltered.

**SBS57 links to tensor signature TS27:** Refitting with the tensor signatures framework yields TS27 (which has a strong replication strand bias and unknown aetiology in COSMIC) as the counterpart to SBS57 in MMRd cells. TS27 and two other MMRd-associated tensor signatures (TS16, TS26) co-occur with Jaccard index 0.83 in the HMF cohort.

**SBS57 in tumours without the MMRd phenotype:** 134 SBS57-positive tumours were identified in PCAWG + HMF. After clustering, three non-MMRd subclusters were found (POLEd, SBS17, SBS12). In these non-MMRd tumours, strict variant filtering did NOT remove SBS57, confirming that SBS57 has a distinct biological context outside MMRd — not a pure artifact in these cases. SBS57 in these tumours increases with replication time, unlike the early-replication enrichment seen in MMRd cells.

**In vitro evidence for MMR-mediated CpG deamination repair:** SBS1 (CpG>TpG clock-like signature, associated with 5-methylcytosine deamination) was detected substantially in MSH2 and MSH6 KOs but not in MMR-proficient cells, providing direct experimental evidence for the MutSα-mediated repair of deamination-related CpG>TpG mutations, confirming a link previously inferred only from tumour sequencing data.

**In vitro vs in vivo MMR signature differences:** SBS6 (damage accumulation-dependent) was nearly absent in KO cells but contributes substantially in cancer tumours, indicating SBS6 requires extended time-based damage accumulation. SBS44 was 3-fold greater in KO cells (0.25 vs 0.08 in tumours), suggesting it is replication-driven. SBS20 (POLD + MMR co-deficiency) was increased in vitro. Replication timing profiles confirmed that MMRd KO cells show "filling up" of early-replicating region mutations (SBS1, SBS6, SBS15, SBS20, SBS26), while SBS14 and SBS44 were enriched in late-replicating regions.

**Indel signatures:** ID1 and ID2 (polymerase slippage in thymine homopolymers) dominated MMRd indel profiles. ID12 (2-bp deletions in repeat-rich regions, unknown aetiology) was also identified in MMRd KOs, suggesting a novel MMRd association.

## Relevance

This paper is directly relevant to hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate–signature-exposure association recovering known aetiologies):

- **H08a positive-control arm — MMR/MSI recovery:** The paper exhaustively maps which COSMIC SBS and ID signatures are mechanistically produced by MLH1/MSH2/MSH6 loss. This characterisation provides the ground-truth positive-control labels needed for the H08a MMR↔SBS6/15/26 arm: within a dataset where MSI status is measured, the agnostic association must recover this mapping.

- **SBS57 as a confounding signature in pipeline:** SBS57 is flagged as a potential artifact driven by SNP–indel alignment errors at thymine repeat boundaries — the same filtering sensitivity the cbioportal pipeline faces. The paper's strict filtering criteria (consensus calling, repeat masking, ±6 bp deletion exclusion) offer actionable guidance for distinguishing true MMRd signal from this artifact class in the cross-study aggregation. Studies with matched normals (the `matched_normal_studies` config key) are less susceptible.

- **Biological context dependence of MMR signatures:** The systematic in vitro vs in vivo comparison demonstrates that signature weights are not portable across biological contexts: SBS6 requires extended time for damage accumulation, SBS44 is replication rate-dependent. This is a caution for hypothesis:0007: interpreting a "low SBS6 weight" in short-passage tumour data as evidence against MMRd would be misleading. The within-tissue, per-study normalisation design of hypothesis:0007 partially mitigates this.

- **SBS1 / CpG deamination connection to MMR:** The first in vitro confirmation that MutSα repairs 5-methylcytosine deamination products means SBS1 (normally treated as a pure clock signature) is partially an MMR-activity readout. This could be relevant for H08b discovery: an agnostic scan may surface MMR-pathway expression as partially associated with SBS1, which this paper would retrospectively explain.

- **TS27 / tensor signatures as an alternative framework:** The paper's use of tensor signatures (Vohringer 2021) alongside COSMIC SBS provides a richer characterisation linking SBS57 to replication strand bias (TS27). The hypothesis:0007 pipeline currently plans COSMIC SBS refitting; consideration of tensor signatures for a follow-up could sharpen MMR-linked associations.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| MMRd (MLH1/MSH2/MSH6 KO) | MSI-H / matched_normal_studies config | Canonical MMR gene loss drives MSI; studies with matched normals better capture true MMRd signal |
| SBS57 artifact mechanism | Variant filter design in `create_freq_tables.py` | SNP+indel alignment errors near thymine repeats — pipeline's RepeatMasker and consensus calling reduce but may not fully eliminate |
| SBS6 (damage-time dependent) vs SBS44 (replication-rate dependent) | Signature context-dependence caveat | In vitro / short-time-window data may underrepresent SBS6 relative to tumours |
| ID12 (unknown aetiology → MMRd) | Novel aetiology discovery | Relevant to h08b: unlabelled indel signatures may have detectable covariate associations |
| TS27 (tensor signature) | Alternative to COSMIC SBS | Not currently in pipeline; possible future extension |
| PCAWG + HMF tumour cohorts | tcga_mc3 pseudo-study | Different cohorts; PCAWG overlaps TCGA; HMF is metastatic |

## Limitations

- **Preprint status:** Not peer reviewed at the time of reading (posted 2025-02-12).
- **HAP1 cell system:** Haploid near-haploid cell line; most cells diploidised by the end of experiments. Mutation rate and spectrum may differ from diploid cancer cells, particularly for dosage-sensitive pathways.
- **Short in vitro time window:** Three months of culture is insufficient to accumulate the full damage-dependent signature repertoire seen in long-lived tumours; SBS6 was nearly absent. Caution in extrapolating absolute signature weights.
- **Single gene knockouts:** Cancer MMRd often involves promoter methylation (MLH1) or multiple gene co-silencing. The pure single-KO system may not fully replicate the heterogeneous MMRd landscape in clinical tumours.
- **SBS57 in non-MMRd tumours:** The mechanism generating SBS57 in the POLEd, SBS17, and SBS12 tumour clusters remains unexplained; the paper explicitly notes it is not FFPE artifact or sequencing noise in these cases, but the biological driver is unresolved.
- **Compositional interpretation caveat:** The authors correctly note that signature weights are compositional data — an absolute increase in one signature's activity forces a relative decrease in all others, making it impossible to cleanly distinguish cause from consequence in relative weight shifts.

## Model / Tool Availability

No standalone software tool or model released with this preprint. Cell lines can be purchased from Horizon Genomics. COSMIC v3.4 signature refitting used NNLS (standard tooling). Data availability statement not visible in the preprint text reviewed; raw WGS data presumably deposited but specific accession not confirmed in the main text.

## Follow-up

- The unresolved mechanism of SBS57 in non-MMRd tumour contexts (POLEd, SBS17, SBS12 clusters) warrants investigation — these are likely biologically distinct from the MMRd alignment-artifact mechanism.
- ID12 (2-bp deletions at repeats, now proposed as MMRd-associated) could be checked in the cross-study aggregation for correlation with MSI-positive study subsets.
- The paper's SBS6 vs SBS44 context-dependence finding is worth encoding as a caveat in hypothesis:0007's positive-control design: within-tumour MMR-loss association tests should target the ensemble of MMR signatures (SBS6/14/15/20/21/26/44), not rely on any single one, because relative weights shift with replication kinetics.
- Consider whether the strict variant filtering criteria from this paper (consensus calling + RepeatMasker + ±6 bp deletion exclusion) are already applied in the cbioportal pipeline's data ingestion, or whether SBS57-type artifacts may be present in the aggregated MAF data from studies using only single callers.
