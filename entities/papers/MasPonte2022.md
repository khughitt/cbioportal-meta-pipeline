---
type: paper
title: Spectrum of DNA mismatch repair failures viewed through the lens of cancer
  genomics and implications for therapy
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:MasPonte2022
ontology_terms:
- mismatch repair
- microsatellite instability
- mutational signatures
- MMR deficiency
- cancer genomics
- immunotherapy
datasets: []
source_refs:
- cite:MasPonte2022
related:
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
---

# Spectrum of DNA mismatch repair failures viewed through the lens of cancer genomics and implications for therapy

- **Authors:** David Mas-Ponte, Marcel McCullough, Fran Supek
- **Year:** 2022
- **Journal:** Clinical Science, vol. 136, pp. 383–404 (Portland Press)
- **DOI/URL:** https://doi.org/10.1042/CS20210682
- **BibTeX key:** MasPonte2022
- **Source:** PDF

## Key Contribution

This review synthesizes how DNA mismatch repair (MMR) deficiency creates characteristic mutational
landscapes in tumors, catalogued both through classical MSI detection and through modern mutational
signature analysis. It argues that MMR failure is more diverse — with multiple genomic subtypes,
broader cancer-type prevalence, and richer therapeutic consequences — than the binary
MSI-H / MSS classification captures. The authors propose that genomics-based pattern analysis
(SNV trinucleotide spectra, indel signatures, CNA patterns, strand-asymmetry, regional mutation-rate
redistribution) will enable subtyping of MMR failures and refined predictive biomarkers for
chemo-, radio-, and immunotherapy.

## Methods

Review article synthesizing the literature as of early 2022; no original data generated. Coverage
spans:

- **Biochemistry of MMR:** MutS (MSH2/MSH6, MSH2/MSH3) and MutL (MLH1/PMS2, MLH1/PMS1,
  MLH1/MLH3) complexes; EXO1 nuclease; distinction between MSH2 and MSH6 LOF phenotypes.
- **MSI detection methodology:** Bethesda 5-locus PCR panel; pentaplex mononucleotide alternative
  (BAT-25/26, NR-21/24/27); bioinformatics tools (MSISensor, mSINGs, Mantis, MSIseq) applied to
  WES/WGS; head-to-head concordance with PCR gold standard (83–97% across colorectal, uterine,
  stomach cancer [ref 43]).
- **Mutational signature frameworks:** NMF-based SBS/indel extraction; COSMIC signature catalog
  (SBS6, 14, 15, 20, 21, 26, 44 linked to MMR); indel signatures ID1, ID2, ID7.
- **Evidence sources:** human tumor cohorts (TCGA, PCAWG, HMF), engineered cell lines
  (isogenic CRISPR knockouts of MLH1, MSH2, MSH6, PMS2), model organisms (yeast, C. elegans, mouse).

## Key Findings

### MMR pathway and phenotypes

- Loss of MSH2 or MLH1 generates the most severe hypermutation phenotype; MSH6 and PMS2 losses
  produce milder or distinct spectra.
- **EMAST phenotype:** instability at tetranucleotide repeats (AAAG/ATAG) driven by MSH3 LOF —
  mechanistically distinct from classical MSI-H; ~40% of MSS colon cancers show partial EMAST;
  common in lung, skin, and bladder cancers.
- **MSI-L phenotype:** instability at ≥1 but <2 Bethesda loci; possibly a distinct biological
  class rather than a mild MSI-H; associated with dinucleotide rather than mononucleotide repeat
  instability; linked to PMS2 loss and BER/translesion polymerase contributions; more frequent
  in melanoma and pancreatic tumors.

### Multiple MMR-linked mutational signatures

- At least **7 SNV trinucleotide signatures** are associated with MSI-H across cancer types
  (COSMIC SBS6, 14, 15, 20, 21, 26, 44); some (SBS14, SBS20) co-occur with POLE/POLD1 mutations,
  suggesting mixed mechanisms.
- **PMS2 knockout** in cell lines generates an A>G/T>C-rich spectrum distinct from the
  C>T/G>A-rich spectra of MSH2 or MSH6 mutants — demonstrating gene-specific MMR mutational
  fingerprints.
- Indel signatures ID1, ID2 (MS indels) and ID7 are associated with MSI-H; a "RefSig MMR2"
  signature spans SBS12/SBS26 and appears in ovary, liver, lymphoid, bone, soft tissue, and CNS.
- **Tissue specificity:** different MS loci appear unstable in different cancer types; regional
  mutation-rate redistribution (loss of the late-replicating / gene-poor protection) is a WGS-only
  observable that can expose otherwise-cryptic MMR activity loss.

### MMR prevalence likely underestimated

- The binary Bethesda panel may undercount MSI in ovarian cancer (10–12% by locus assay vs.
  3.2% by genomics-based classifier), head-and-neck, cervical, adrenocortical, and mesothelioma
  tumors.
- MSI is better modeled as a continuous phenotype (supported by survival associations) rather
  than a two-class label.
- Indirect evidence: "flat" (de-regionalized) mutation-rate landscapes, comparable to confirmed
  MSI-H, are observed in non-MSI-H kidney and pancreatic tumors — possibly partial MMR dysfunction.

### MMR and cancer evolution

- MMR deficiency increases per-division mutation rates by ~100-150× in model organisms and ~31
  Gd⁻¹ in human cultured cells (core MMR KOs: MLH1, MSH2, MSH6, PMS2, EXO1 average ~93 SNV
  and ~69 indel per division).
- MS indels in coding regions generate frameshift → NMD → neoantigen axis; genes with recurrent
  MS mutations include ACVR2A, RNF43, JAK1, PRDM2, MSH3, MRE11, RAD50.
- Somatic mutation density redistribution in MSI tumors: early-replicating gene-dense regions
  suffer disproportionate rate increases, potentially altering the repertoire of driver genes
  selected for in MMR-deficient vs proficient tumors.

### Mutagenic MMR activity (non-canonical roles)

- Normal MMR, when co-opted for somatic hypermutation (SHM), recruits error-prone POLH — POLH
  mutational signatures are detectable in cancer and correlate with UV, oxidative stress, tobacco,
  and alcohol exposures.
- APOBEC activity partly depends on MMR: EXO1-mediated excision during BER can generate
  ssDNA substrates for APOBEC3 deamination, producing the "mutation fog" (omikli) clustering
  pattern. This MMR–APOBEC coupling may account for ~2/3 of APOBEC mutations and concentrates
  them in early-replicating gene-rich regions.

### Therapeutic implications

- **Sensitization via MMR failures:**
  - MSI ↔ irinotecan sensitivity via MRE11/RAD50 frameshift inactivation (≥75% of MSI cancers
    harbor MRE11 mutations).
  - Frameshift-derived neoantigen burden → immunotherapy efficacy (MSI the first FDA-approved
    pan-cancer genetic biomarker for ICI); frameshifting indels, not SNVs, are the more robust
    predictor of ICI response.
  - NMD inhibition can expose toxic frameshifted proteins (e.g. HSP110Δ9) — a proposed
    NMDi strategy.
  - ATR/WRN synthetic lethality: MSI tumors accumulate A:T expansions, creating dependency
    on WRN helicase; ATR inhibitors may proxy for WRN inhibition.
- **Resistance via MMR deficiency:**
  - Temozolomide (TMZ): MMR normally triggers apoptotic signaling on O6-MeG lesions; MMR
    deficiency (commonly MSH6 mutations) confers TMZ resistance.
  - 5-FU and 6-thioguanine: cytotoxicity requires functional MMR to process the misincorporated
    nucleotide analog; dMMR tumors are resistant and are not recommended for 5-FU adjuvant
    therapy in colorectal cancer.
  - Lynch syndrome (constitutional CMMRD): MLH1/MSH2 silencing + somatic second-hit required;
    epigenetic MLH1 promoter methylation is a common somatic silencing mechanism.

## Relevance

This review is directly load-bearing for hypothesis **h08** (agnostic covariate-signature
association):

1. **H08a positive-control specification (MMR/MSI arm).** The paper confirms the canonical
   MMR-failure signatures — SBS6, SBS15, SBS26, SBS44 (SNV), ID1, ID2, ID7 (indel) — as the
   expected recovery targets when MSI status is used as a covariate in the h08 association scan.
   It also names the gene-level indicators (MLH1 promoter methylation, MSH2/MSH6/PMS2 LOF) that
   should serve as the MMR-loss proxy covariate.

2. **Multiple MMR signatures complicate a clean positive control.** The review notes ≥7 distinct
   SNV signatures link to MSI-H, with overlapping tissue and mechanistic contributions. This
   means a single "MMR covariate → single signature" recovery test is an oversimplification; the
   h08 scan should expect a broad, multi-signature association with MSI rather than a sharp
   single-factor signal.

3. **MSI is a continuous, not binary, phenotype.** The paper's argument that Bethesda-based
   MSI-H/MSS classification is a coarse approximation is relevant to how MSI is encoded as a
   covariate in the h08 scan. A continuous MSI score (e.g. from MSISensor) may perform better
   than the binary clinical label.

4. **APOBEC–MMR coupling.** The mechanistic link (EXO1-generated ssDNA → APOBEC3 substrate)
   provides a reverse-causation hypothesis for the APOBEC/SBS2-SBS13 arm of h08: APOBEC3A/B
   expression is expected to associate with SBS2/13, but some of the SBS2/13 signal may track
   *with* partial MMR activity — making APOBEC3 expression and MMR status co-regulators rather
   than independent predictors.

5. **Frameshifting indels as TMB component.** The emphasis that frameshift-indel burden (not
   just SNV TMB) predicts ICI response reinforces that the pipeline's hypermutator / TMB
   annotation should include indel burden alongside SNV TMB, particularly for MSI-context
   samples.

6. **Cross-study MMR signal heterogeneity.** Tissue-specific MSI loci and tissue-specific
   MMR-associated signatures suggest that the within-tissue conditioning design of h08
   (Prediction 4) is essential — pooling across tissues would blur the MMR covariate↔signature
   link.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| MSI-H / MSS binary label | `msi_status` clinical field post-t083 | Continuous MSISensor score preferred per paper; project ingests binary label |
| MMR-linked SNV signatures (SBS6/15/26/44) | h08 positive-control MMR arm | Recovery target for within-tissue covariate scan |
| Indel signatures ID1/ID2/ID7 | Not yet in pipeline scope | Would require indel-spectrum extraction step |
| MSH2/MLH1/MSH6/PMS2 LOF | `ch_priority_gene` flag (partial overlap) | CH gene list is distinct; MMR gene LOF requires separate annotation |
| EMAST / tetranucleotide instability | No current representation | Beyond binary MSI; future subtying |
| Continuous MSI score | `hypermutation_score` (partial analog) | Hypermutator score is TMB-based, not MS-instability-based |
| MMR–APOBEC coupling via EXO1 | h08 reverse-causation guard | APOBEC3 expression association with SBS2/13 may partly reflect MMR state |

## Limitations

- Review article: no new empirical analysis; conclusions reflect author interpretation of
  heterogeneous study designs and signature catalogs that were still evolving as of 2022.
- Signature catalog is pre-COSMIC v3.3/v3.4; some referenced signature numbering may have
  shifted or been merged in subsequent releases.
- The "higher MMR prevalence" claim (Section 5) is acknowledged by the authors as speculative
  and requiring further validation; circumstantial genomic evidence, not confirmed by functional
  assays.
- Continuous MSI score arguments are based on computational studies; biological relevance of
  the continuum vs. a sufficiently sensitive binary has not been fully established.
- Therapeutic recommendations (irinotecan, NMDi strategies, WRN/ATR synthetic lethality) are
  based on cell-line and early clinical data; most have not been validated in prospective RCTs.

## Model / Tool Availability

Review only; no new model or tool released. Referenced bioinformatics tools for MSI detection:
MSISensor (doi:10.1093/bioinformatics/btt755), mSINGs, Mantis (doi:10.18632/oncotarget.13918),
MSIseq, MMRDetect (ref 60/63 in paper).

## Follow-up

- Check current COSMIC v3.4 catalog for updated MMR signature set (SBS6/15/26/44 may have
  refined spectra or companion signatures added post-2022).
- Investigate whether MSISensor continuous scores are available in cBioPortal clinical tables
  for studies already downloaded — if so, encode as a continuous covariate for h08 rather than
  the binary MSI flag.
- Consider indel signature extraction (ID1/ID2/ID7) as a complementary positive control arm
  for h08 MMR recovery, alongside SNV signatures.
- The APOBEC–MMR coupling via EXO1 (omikli mechanism) is a candidate alternative explanation
  for the APOBEC arm of h08 and should be flagged as a reverse-causation candidate in the
  pre-registration if the APOBEC arm is added.
- Paper ref 52 (Meier 2018, Genome Res): MMR deficiency signatures in C. elegans and human
  cancers — primary data source for cell-line MMR signature characterization; consider
  summarizing alongside this review.
- Paper ref 63 (Degasperi 2020, Nat Cancer): practical framework for signature analysis with
  inter-tissue variation; directly relevant to the h08 within-tissue conditioning design.
