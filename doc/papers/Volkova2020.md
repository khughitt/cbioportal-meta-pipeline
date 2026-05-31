---
id: "paper:Volkova2020"
type: "paper"
title: "Mutational signatures are jointly shaped by DNA damage and repair"
status: "active"
ontology_terms:
  - mutational signatures
  - DNA damage
  - DNA repair
  - translesion synthesis
  - nucleotide excision repair
  - C. elegans
  - somatic mutation
datasets: []
source_refs:
  - "cite:Volkova2020"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Mutational Signatures Are Jointly Shaped by DNA Damage and Repair

- **Authors:** Nadezda V. Volkova, Bettina Meier, Víctor González-Huici, Simone Bertolini, Santiago Gonzalez, Harald Vöhringer, Federico Abascal, Iñigo Martincorena, Peter J. Campbell, Anton Gartner, Moritz Gerstung
- **Year:** 2020
- **Journal:** Nature Communications
- **DOI/URL:** https://doi.org/10.1038/s41467-020-15912-7
- **BibTeX key:** Volkova2020
- **Source:** PDF

## Key Contribution

This study provides the most systematic experimental dissection to date of how specific DNA damage types and specific DNA repair pathways *jointly* determine mutational signatures. Using 2,717 *C. elegans* whole-genome sequences spanning 54 genotypes (wild-type + 53 repair-deficient backgrounds) crossed with 12 genotoxins at multiple doses, the authors show that 41% of genotoxin × repair combinations alter mutation rates or spectra — demonstrating that signatures observed in cancer genomes are not the fingerprints of damage alone but emergent products of the interplay between damage and repair. A key mechanistic insight is that error-prone translesion synthesis (TLS) causes the majority of genotoxin-induced base substitutions while simultaneously suppressing larger deletions, and that nucleotide excision repair (NER) prevents up to 99% of genotoxin-induced point mutations.

## Methods

**Experimental design.** 54 *C. elegans* strains (wild-type + 53 repair-deficient knockouts covering MMR, BER, NER, DSBR, TLS, CLR, DNA damage checkpoints, helicases, MGMT, and TR) were crossed with 12 genotoxic agents (UV-B, X-rays, γ-rays, EMS, DMS, MMS, aflatoxin B1, aristolochic acid, cisplatin, mechlorethamine, hydroxyurea, mitomycin C) at 2–3 doses each, yielding 2,717 sequenced genomes from either mutation-accumulation (5–40 generations, untreated) or single-generation genotoxin exposure experiments, all run in triplicate. 162,820 total mutations were acquired (135,348 SNVs, 937 MNVs, 24,308 indels, 2,227 SVs), classified across 119 mutation classes (96 SBS trinucleotide contexts + MNV + indel size/context + SV categories).

**Statistical model.** A Bayesian negative-binomial regression with genotype and mutagen dose as predictors, plus an explicit multiplicative interaction term, was fitted to count data for all 196 genotoxin × repair-background combinations. Interaction significance was tested by chi-squared test on the squared log-ratio of observed to expected mutations (FDR < 5%). Cosine distance was used to quantify spectrum changes. The model explicitly separates damage-driven mutagenicity from repair-deficiency background mutagenicity from their interaction, enabling attribution of 141,004 interaction-condition mutations to three additive components: genotoxin effect (54%), repair-deficiency effect (26%), positive interactions — genotoxin + repair deficiency synergizing to add mutations (23%) — and negative interactions — deficiency suppressing mutations (−3%).

**Translation to human cancer.** TCGA/PCAWG cancer data were queried for samples with high-impact mutations in DNA repair pathway genes, and the same interaction model (Hamiltonian Monte Carlo) was applied to human mutation count matrices to test whether repair-gene status predicted signature alteration.

## Key Findings

1. **TLS dominates base-substitution mutagenesis.** Error-prone TLS polymerases (REV-3/Pol ζ, POLH-1/Pol η, POLQ-1/Pol θ) are responsible for 60–80% of genotoxin-induced base substitutions across UV, aflatoxin B1, AA, DMS, and MMS exposures. Counterintuitively, TLS *suppresses* large deletions and SVs — e.g. *rev-3* knockouts reduce MMS-induced base substitutions but increase small deletions ~20-fold.

2. **NER prevents up to 99% of point mutations.** NER (via XPC-1 and XPF-1) prevents up to 99% of MMS-induced mutations through error-free repair, and similarly large fractions for other bulky-adduct genotoxins. NER deficiency leads to uniform rate increases (not spectrum changes) for most genotoxins, indicating NER acts on a broad lesion substrate.

3. **AGT-1 (MGMT ortholog) specifically suppresses C>T from O6-meG.** AGT-1 deficiency in *C. elegans* exposed to MMS elevates C>T from ~15 to ~200 mutations/mM while leaving T>M unchanged — a mechanistically clean demonstration that MGMT reverses O6-methylguanine adducts in an error-free manner. In human glioblastomas, MGMT silencing increased mutation burden ~10× (p < 10⁻¹⁶), confirming the cross-species relevance.

4. **41% of genotoxin–repair combinations show significant interaction.** In 88/196 tested combinations (FDR < 5%), DNA repair status significantly altered either the rate or the spectrum of genotoxin-induced mutations. Interactions were most dramatic for TLS and NER deficiencies; crosslink repair (CLR) and checkpoint deficiencies had surprisingly modest effects at tested doses.

5. **Same genotoxin, different lesions repaired by different pathways.** For MMS alkylation, distinct adducts (N3-meA, O6-meG, N7-meG) are repaired by NER, BER/direct repair, and TLS respectively — so the MMS signature is the superposition of multiple lesion-specific sub-signatures, each sensitive to a different repair gene. This explains why single repair-gene mutations in human cancers often produce subtle signature shifts rather than clean exposure signatures.

6. **Cancer data translation (moderate effects).** In TCGA/PCAWG cohorts, the known signature interactions — POLE exonuclease domain + MMR deficiency, UV damage + NER deficiency, APOBEC + TLS, temozolomide + MMR — were detectable but of moderate magnitude, because human cancers have unknown exposure histories, unknown timing of repair defects, and biallelic inactivation is rare (detected in supplementary analysis).

7. **Mutation rate and cancer risk are super-linear.** A modelling exercise using the multi-hit cancer evolution model shows that small fold-changes in mutation rate (as observed experimentally, typically 2–50×) translate to large relative risk increases (8-fold higher mutation rate in MMR-deficient colorectal cancer → >115-fold cancer risk increase), explaining why even mild mutator phenotypes can be strongly selected in cancer.

## Relevance

This paper is directly relevant to **hypothesis h08** (agnostic covariate↔signature-exposure association; positive-control recovery):

- **H08a positive-control grounding.** Volkova et al. establish the mechanistic ground truth for the known signature-aetiology links that h08's positive-control arm must recover: UV → SBS7 (C>T in YpCpH, suppressed by NER/XPC, XPF), smoking-related alkylation → SBS-like substitution spectra, APOBEC → C>G via REV1/UNG-dependent BER, MMR deficiency → high base-substitution with 1-bp indels at homopolymers. The paper also documents *why* these links are impure in cancer (unknown dose, unknown timing, partial repair proficiency, multiple co-active processes), which anticipates the confounding the h08 association scan will need to control for.

- **TLS as a confounding modifier.** Because TLS is responsible for the majority of observed mutations (not the primary damage), the "signature" seen in a cancer genome reflects TLS activity as much as the upstream genotoxin. This means h08's agnostic associations may surface TLS pathway expression (e.g. *REV1*, *POLK*, *POLH*) as mediators of damage signatures — an unregistered but biologically grounded prediction. The APOBEC–REV1/UNG interaction (Fig. 4c) is a clean example of this for the APOBEC positive-control arm.

- **Cross-study aggregation implications.** The finding that repair-gene inactivation in human cancers produces only moderate and hard-to-detect signature changes (due to unknown exposure history and mono-allelic vs bi-allelic status) is a caution for the cBioPortal meta-analysis: even well-powered cross-study aggregation may see only 8% shifts in signature-relevant substitution classes (APOBEC C>G example) — below the signal-to-noise floor of panel-based mutation calling for many studies. This supports h08's design choice to prioritize WES/WGS substrates (tcga_mc3) for per-sample signature decomposition.

- **NER uniform-rate interaction as a confounder archetype.** NER deficiency raises mutation rates uniformly without changing the spectrum — this means NER status is a confound on TMB (h08's within-tissue strata would mix NER-proficient and NER-deficient samples), but would *not* appear as a signature-specific association in h08's scan unless the absolute-rate signal is modelled. Worth flagging when designing the nuisance-covariate list.

- **Quantitative scale reference.** The paper establishes that mutation rates in the C. elegans system are 0.8–2 mutations/generation/background, rising to thousands/generation/dose under strong genotoxin + repair-deficiency combinations. The log-linear relationship between mutation rate fold-change and cancer risk (Fig. 6) provides a quantitative framework for interpreting h08 association effect sizes in terms of biological relevance.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Genotoxin-induced mutational spectrum | Signature aetiology (COSMIC SBS) | Paper's experimental spectra match COSMIC signatures with c = 0.85–0.95 |
| DNA repair pathway knockout | Repair-gene somatic mutation (TCGA) | Used in Fig. 2d for human cancer translation |
| Interaction term (genotoxin × repair) | Covariate × signature-exposure association | The interaction model is analogous to h08's association layer |
| TLS contribution fraction | Mediator variable (expression module?) | h08 could test POLK/POLH/REV1 expression as mediators |
| NER uniform rate increase | TMB confounder | Should be included as nuisance covariate in h08 within-tissue model |
| AGT-1 / MGMT silencing effect | Epigenetic covariate (MGMT methylation) | MGMT methylation status is available in TCGA; a clean positive control for expression-mediated signature change |

## Limitations

- *C. elegans* is a model organism: some DNA repair pathways (e.g. global NER tissue specificity, immune-related damage) do not translate directly to human tumour biology.
- Biallelic inactivation of repair genes was confirmed to be rare in cancer (Supplementary Note 3), limiting the human translation in most cohort studies.
- The genotoxins tested are mostly well-characterized environmental or chemical agents; endogenous sources of replication errors (deamination, ROS) are less systematically covered.
- Dose–response relationships in *C. elegans* may not match human tissue exposures quantitatively, and exposure history in cancer is unknown and cumulative.
- The 119-class mutation spectrum used here (96 SBS + MNV + indel + SV) maps cleanly to COSMIC-style decomposition, but the paper does not perform formal NMF/SigProfiler decomposition — it uses per-class regression models, so it does not directly identify latent COSMIC components.
- APOBEC and immune-editing signatures are not well-represented in the *C. elegans* screen (APOBEC section relies on human cell lines and cancer cohorts, not the worm model).

## Model / Tool Availability

- Code for downstream analyses and figures: https://github.com/gerstung-lab/signature-interactions
- Raw sequencing data: ENA ERP000975 and ERP004086
- TCGA somatic mutation and methylation data: NCI GDC (https://gdc.cancer.gov/)
- XP patient tumour data: dbGaP phs000830.v1.p1

## Follow-up

- Kucab2019 (already summarized) complements this paper with a human iPSC compendium of environmental mutagen signatures — compare SBS11 (temozolomide/EMS) between species.
- Manders2022 (already summarized) extends the *C. elegans* approach to a larger repair-pathway screen.
- For h08: design the nuisance-covariate list for the association layer to include DNA repair pathway expression modules (NER/MMR/TLS) as potential mediators rather than only confounders.
- Consider whether MGMT methylation status (available for TCGA glioblastoma) could serve as a clean positive-control arm for h08's expression-mediated signature association (MGMT expression ↔ temozolomide/alkylator SBS signature).
