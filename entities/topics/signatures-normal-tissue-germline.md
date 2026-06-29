---
type: topic
title: Mutational signatures in normal tissue and germline determinants
status: active
created: '2026-05-31'
updated: '2026-06-28'
id: topic:signatures-normal-tissue-germline
ontology_terms:
- mutational signatures
- normal tissue somatic mutations
- germline predisposition
- DNA damage repair
- immune cell mutagenesis
- de novo mutations
- paternal age effect
source_refs: []
related:
- paper:Faienza2025
- paper:Gillani2022
- paper:Machado2021
- paper:Machado2022
- paper:Shojaeisaadi2024
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
---

# Mutational signatures in normal tissue and germline determinants

## Summary

Somatic mutations accumulate in all human cells throughout life, driven by a combination of clock-like endogenous processes (SBS1, SBS5/SBSblood), cell-type-specific programmed activities (immunological diversification in lymphocytes), and exogenous mutagen exposures that leave tissue-specific imprints. Germline variants in DNA damage repair (DDR) genes modulate somatic mutation rate and spectrum — both through inherited effects on repair fidelity in the germline and through haploinsufficiency that predisposes specific cancer types. Together, this literature frames mutational signatures not as cancer-exclusive phenomena but as cumulative records of lifelong cellular history, grounding the use of signatures as covariates in cross-cancer meta-analyses and validating known aetiologies as positive controls.

## Key Concepts

**Clock-like signatures (SBS1, SBS5/SBSblood):** Signatures that accumulate proportionally with age and cell divisions regardless of tissue type or exogenous exposure. SBS1 reflects spontaneous deamination of 5-methylcytosine at CpG sites; SBS5 is of unknown mechanistic origin but also accumulates linearly with age. paper:Shojaeisaadi2024 confirms that COSMIC decomposition of germline de novo mutations requires only SBS1 and SBS5 (~15% and ~85% respectively), establishing these as the dominant clock-like processes operating in normal cells prior to any cancer-specific mutagenesis.

**SBSblood:** A novel haematopoietic-specific endogenous signature identified in paper:Machado2022, dominant in HSPCs and naive lymphocytes. It is distinct from SBS5 (cosine similarity 0.87 — close but separable) and may be collapsed with SBS5 in studies using standard COSMIC decomposition.

**Differentiation-associated signatures (SBS9):** In paper:Machado2022, the germinal-centre signature SBS9 accounts for ~42% of memory B cell mutations on average (mean ~780 mutations/cell). SBS9 exposure correlates with IGHV somatic hypermutation rate (R²=0.57), telomere lengthening, and germinal centre B cell epigenomic marks. The proposed mechanism is polymerase eta-mediated error-prone translesion synthesis during replicative stress in germinal centres, not direct AID deamination.

**Exogenous environmental signatures:** SBS7a (UV) and SBS17b appear sporadically in circulating memory lymphocytes as records of tissue-microenvironment residency. SBS7a in memory T cells (9/100 cells >10%) proves past skin residency — a landmark demonstration that signatures can infer cellular geography (paper:Machado2022; reviewed in paper:Faienza2025). SBS17b in memory B/T cells (independent of chemotherapy) may reflect GI mucosal residency but its aetiology is [SPECULATION, per authors].

**Germline DDR variants as upstream signature determinants:** paper:Gillani2022 documents that heterozygous pathogenic loss-of-function variants in Fanconi anemia genes (FANCC, FANCA) and CHEK2 are enriched in Ewing sarcoma, mechanistically predicting HRD-like somatic rearrangement signatures (SBS3, structural variant signatures) downstream. paper:Shojaeisaadi2024 establishes that declining MMR fidelity (EXO1, PMS1, PMS2) drives the age-associated paternal DNM accumulation in the germline, with spectral patterns overlapping COSMIC MMR-deficiency signatures (SBS6/15/26/44).

**Somatic mutations as non-reversible cumulative records:** paper:Faienza2025 positions this framing as the conceptual basis for signature-based tissue-of-origin inference, exposure tracking, and repair-system characterisation. The non-reversible, cumulative property is what makes mutational signatures viable covariates: a sample's SBS4 burden encodes lifetime tobacco exposure, not current smoking status.

## Current State of Knowledge

### Normal-tissue mutation accumulation rates and spectra

WGS of single-cell-expanded normal lymphocytes (paper:Machado2022, 717 genomes, 6 donors) establishes quantitative baselines: HSPCs ~16 SNVs/year; naive lymphocytes ~15–22 SNVs/year; memory lymphocytes accumulate substantially more due to differentiation history (memory B +1,034 SNVs, memory T +277 SNVs above HSPC baseline). Accumulation rates 10–80 SNVs/genome/year across normal tissues are reported in review paper:Faienza2025, with tissue-specificity in rate and spectrum well-established.

For `topic:signatures-normal-tissue-germline`, variance in mutation burden across cells increases dramatically with differentiation state: within-donor SD in memory B cells (~820 SNVs) far exceeds between-person variation (~60 SNVs). This within-person heterogeneity is relevant to bulk tumour sequencing: the starting mutation burden of the cell of origin is a major contributor to inter-tumour variance even within histologically uniform cohorts.

### Immunological diversification as a structured mutational process

The Machado lymphocyte studies (paper:Machado2021; paper:Machado2022) establish that approximately half of the excess mutations in memory versus naive lymphocytes are attributable to off-target effects of programmed immune mechanisms:

- **SBS9**: Germinal centre off-target mutagenesis (estimated 18 genome-wide off-target mutations per 1 on-target IGHV mutation).
- **RAG off-target SVs**: ~15% of non-Ig/TCR deletions genome-wide carry RSS motifs, attributing ~12% of all non-Ig/TCR SVs to off-target RAG activity; 16-fold higher SV burden in lymphocytes than HSPCs.
- **AID/SHM off-target**: Class switch recombination is confined to switch regions; CSR motifs absent from non-Ig/TCR SVs.

Crucially, the mutational signature composition of common B-cell malignancies (CLL, Burkitt lymphoma, DLBCL) broadly mirrors normal memory B cells — suggesting lymphoid cancers amplify existing normal-cell mutational processes rather than acquiring cancer-specific ones. This distinguishes lymphoid from carcinomas (colorectal, breast) where cancer-specific signatures are more dominant.

### Germline MMR deficiency and the paternal age effect

paper:Shojaeisaadi2024 demonstrates that the age-dependent increase in paternal germline de novo mutations is best explained mechanistically by MMR inefficiency (EXO1, PMS1, PMS2) rather than increased replication errors per se. The CRISPR-KO signature decomposition achieves cosine similarity 0.915 using only three MMR gene knockouts. The overall PAE slope of +1.29 SNVs/year shows extensive inter-family variability (range −1.88 to +6.52), consistent with polygenic modulation of germline mutation rate. Maternally-phased DNMs show no significant age correlation — paternal spermatogenesis is the dominant age-dependent accumulation axis.

### Germline DDR predisposition to specific cancers

paper:Gillani2022 establishes that Ewing sarcoma has a distinct germline predisposition profile: enriched for Fanconi anemia pathway (FANCC, FANCA) and CHEK2 pathogenic variants but conspicuously lacking TP53 pathogenic germline variants (0% vs 1.6% pan-sarcoma, p=0.006). This is the opposite of osteosarcoma (TP53-enriched), reflecting the known absence of Ewing sarcoma from Li-Fraumeni families. Importantly, all identified DDR variants in trio probands were inherited (100% parent-of-origin confirmed), establishing these as moderate-penetrance autosomal risk alleles rather than de novo events.

The mechanistic chain is: germline FANCC/FANCA haploinsufficiency → impaired Fanconi pathway DDR → elevated HRD-like rearrangement burden (SBS3, ID6, CN-HRD signatures) in tumours [UNVERIFIED in Gillani2022's cohort — the mechanistic link is inferred from prior in vitro FANCC KO studies, not directly demonstrated in these patient tumours].

### Signatures as tissue-of-origin and exposure tracers

paper:Faienza2025 reviews multiple landmark applications: SBS7a in circulating memory T cells proving skin residency; colibactin/SBS88 in colorectal cancer metastases enabling primary site inference; cisplatin chemotherapy footprints in normal blood, colon, and liver stem cells of cancer survivors. These applications confirm that signature aetiology recovery works even outside the primary exposed tissue and can persist across cell divisions.

## Controversies and Open Questions

**SBS9 mechanism — polymerase eta vs. AID indirect:** The paper:Machado2022 proposal that SBS9 arises from polymerase eta translesion synthesis during replicative stress in germinal centres (rather than direct AID deamination) is well-supported by the enrichment in inactive chromatin (vs. active chromatin targeted by SHM) and the correlation with germinal centre epigenomes. However, the mechanistic model is not directly proven — AID-mediated contributions via an indirect route cannot be fully excluded [SPECULATION, per authors]. This is a contested mechanistic detail; the epidemiological correlation with SHM rate (R²=0.57) is robust.

**SBSblood vs. SBS5 identity:** paper:Machado2022 introduces SBSblood as a distinct haematopoietic-specific endogenous signature with cosine similarity 0.87 to COSMIC SBS5. Whether SBSblood is a tissue-specific instantiation of SBS5 or a genuinely distinct process remains unresolved. Studies using COSMIC decomposition will collapse SBSblood into SBS5, potentially obscuring blood-lineage specificity in cross-cancer comparisons.

**SBS17b aetiology in normal lymphocytes:** SBS17b is well-established as a 5-FU chemotherapy signature in treated cancers (colorectal particularly), but paper:Machado2022 documents its presence in ~4% of memory B cells and ~1% of memory T cells from treatment-naive donors. Whether this reflects GI microenvironmental exposure during tissue residency, a distinct endogenous process with overlapping spectrum, or a rare artefact is unknown [SPECULATION, per authors]. This ambiguity limits SBS17b's use as an unambiguous treatment marker in cBioPortal cohorts.

**FANCC/Fanconi pathway → somatic HRD signatures in Ewing sarcoma:** The mechanistic chain from germline Fanconi pathway haploinsufficiency to elevated somatic HRD signatures is assumed from in vitro data but not demonstrated in patient tumours in paper:Gillani2022's cohort. Whether heterozygous carrier status, rather than biallelic loss, is sufficient to produce detectable signature enrichment in clinical WGS data remains an open question.

**Paternal vs. maternal age effects and MMR:** paper:Shojaeisaadi2024 lacked maternal age data; the mechanistic model for declining MMR fidelity driving paternal DNM accumulation is suggestive but not causally demonstrated (NER gene KOs cause lethality in the hiPSC model, so NER contributions could not be directly quantified). Inter-family PAE slope variability (negative slopes observed in one family) could reflect stochastic sampling artefacts or genuine polygenic buffering of germline mutation rate.

**Positive selection on somatic variants in normal lymphocytes:** paper:Machado2022 estimates dN/dS=1.12 across lymphocyte exomes (11% non-synonymous mutations conferring a selective advantage), with only ACTG1 significant at the gene level. Whether this constitutes genuine adaptive selection or technical biases (variant calling in repetitive regions) remains debated in the field.

## Relevance to This Project

### Implications for `h08` and the cross-study signature-aetiology aggregation

`hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`
proposes an agnostic covariate ↔ mutational-signature-exposure association whose first validation gate is recovery of known aetiologies (UV/SBS7, smoking/SBS4, APOBEC/SBS2-13, MMR/SBS6-26-44) as positive controls before claiming novel hits.

This topic provides the following load-bearing inputs:

1. **Tissue-specificity of positive-control aetiologies.** paper:Faienza2025 articulates the defining properties of a validated signature: tissue-specificity of exposure, dose-dependence, and non-reversibility. For `h08`, this means the smoking→SBS4 association should be recoverable preferentially in lung cancer studies; UV→SBS7 in melanoma and cutaneous squamous cell carcinoma; MMR deficiency signatures in MSI-H colorectal, endometrial, and gastric studies. The normal-tissue literature confirms these aetiologies are real and not cancer-specific artefacts.

2. **Clock-like signatures (SBS1, SBS5) as nuisance covariates.** paper:Shojaeisaadi2024 confirms SBS1 and SBS5 as the dominant drivers of germline de novo mutation accumulation, reinforcing that age must be included as a nuisance covariate in the `h08` association model. Discovering an "association" between age and SBS1 would be a confound, not a novel finding. The `method:h08-agnostic-association-model` should pre-specify age as a covariate to be modelled out.

3. **SBS9 in lymphoid malignancies as a tissue-of-origin confounder.** For cross-study aggregation including lymphoma, CLL, and multiple myeloma studies, SBS9 will be the dominant excess signature reflecting post-germinal centre differentiation of the cell of origin. In the `h08` agnostic scan, the covariate "lymphoid vs. non-lymphoid tissue of origin" will associate strongly with SBS9. This is a known biological positive control (germinal centre activity drives SBS9), not a novel hit — it should be documented as a positive control alongside UV/smoking/APOBEC/MMR. paper:Machado2022 provides the quantitative baseline to interpret SBS9 exposure levels across cBioPortal lymphoma studies.

4. **SBSblood as a lymphoid-lineage covariate candidate.** The SBSblood signature in HSPCs and naive lymphocytes, if distinguishable from SBS5 in COSMIC-based decompositions, could serve as a covariate for lineage purity in bulk tumour data. Tumour-infiltrating lymphocytes in non-lymphoid biopsies would contribute SBSblood to bulk signature profiles — a potential confound for pan-cancer analyses.

5. **RAG/AID off-target mutagenesis as a structural variant confound.** If the `h08` pipeline extends to structural variant signatures, ~15% of non-Ig/TCR deletions from normal lymphocytes bear RAG motifs (paper:Machado2022). Any SV-based covariate association in lymphoid tumours will need to account for this normal-cell baseline.

6. **Germline DDR variants as an extended `h08` covariate class.** paper:Gillani2022 establishes the germline FANCC/Fanconi pathway → HRD-like somatic signature chain. If cBioPortal Ewing sarcoma studies contain germline proxy data (e.g., SBS3 or HRD CN-signature exposure as a downstream readout), the `h08` scan could recover Fanconi pathway burden as a covariate — constituting an extended positive control beyond the current UV/smoking/APOBEC/MMR set. This is lower priority than the four canonical positive controls, but mechanistically well-grounded.

7. **SBS17b ambiguity limits its use as a treatment proxy.** Given paper:Machado2022's finding that SBS17b appears in treatment-naive normal memory cells, SBS17b cannot be used as an unambiguous 5-FU exposure marker in cBioPortal cohorts. This is directly relevant if SBS17b is considered as a covariate (prior chemotherapy) in `h08` associations — the signal will be noisy. [See also the pipeline's existing treatment-signal concern noted in AGENTS.md.]

8. **Power constraints for rare germline effects.** paper:Gillani2022's finding that FANCC enrichment in Ewing sarcoma involves only 3–6 individuals across two cohorts (0.8–1.5% case frequency) illustrates the power challenge. Cross-study aggregation in cBioPortal is the appropriate strategy, but per-variant germline effects may remain undetectable even after aggregation without pre-stratification by cancer type and ancestry.

### Connection to adjacent topics

- topic:normal-tissue-mutation-atlas — quantitative mutation burden baselines across normal tissues that contextualise the lymphocyte findings here.
- topic:signature-decomposition-unmatched-normal — methodological considerations for decomposing signatures without matched normals, directly relevant when applying `h08` to unmatched cBioPortal studies.

## Key References

- paper:Machado2022 — Canonical normal lymphocyte WGS study; defines SBSblood, SBS9 germinal centre basis, SBS7a skin-residency proof. The primary reference for lymphoid signature baseline.
- paper:Machado2021 — Preprint companion to Machado2022; same cohort, overlapping findings; prefer Machado2022 (Nature peer-reviewed) for citation.
- paper:Faienza2025 — Review covering the full breadth of somatic mutation applications in non-cancer biology; useful conceptual anchor for `h08` positive-control design.
- paper:Shojaeisaadi2024 — Germline de novo mutation signatures; establishes SBS1+SBS5 as clock-like germline processes and MMR pathway (EXO1, PMS1, PMS2) as age-related DNM accumulation mechanism.
- paper:Gillani2022 — Germline DDR predisposition in Ewing sarcoma; establishes FANCC/Fanconi pathway → HRD-like somatic signature causal chain as a candidate extended positive control for `h08`.
