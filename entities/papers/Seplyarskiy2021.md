---
type: paper
title: The origin of human mutation in light of genomic data
status: active
created: '2026-05-31'
updated: '2026-06-28'
id: paper:Seplyarskiy2021
ontology_terms: []
datasets: []
source_refs:
- cite:Seplyarskiy2021
related: []
---

# The origin of human mutation in light of genomic data

- **Authors:** Vladimir B. Seplyarskiy, Shamil Sunyaev
- **Year:** 2021
- **Journal:** Nature Reviews Genetics
- **DOI/URL:** https://doi.org/10.1038/s41576-021-00376-2
- **BibTeX key:** Seplyarskiy2021
- **Source:** PDF

## Key Contribution

This review synthesises genome-scale sequencing evidence — primarily from parent–offspring trio studies and population-level SNV data — to build mechanistic models of spontaneous human mutagenesis. It argues that statistical footprints in sequencing data (context dependence, strand asymmetries, regional rate variation, parental age effects) can be interpreted in light of known DNA replication and repair biochemistry to identify the dominant mutagenic processes. A central conclusion is that DNA damage is widely converted to mutations during replication, making replication timing and cell division count critical determinants of the mutation rate, while sex-specific spectra and maternal-age-dependent clustered mutations point to distinct oogenesis- versus spermatogenesis-specific mechanisms.

## Methods

The review synthesises published empirical results rather than presenting new primary data. Key data sources discussed include:

- **De novo mutation (DNM) trio sequencing:** direct observation of germline mutations as parent–child differences absent in both parents; enables sex-specific attribution and parental-age dissection.
- **Population-level SNV data:** large-scale cohorts (gnomAD v2 and similar) as a statistical proxy for mutations at longer timescales, capturing context and regional patterns with higher power than trio studies.
- **Cancer somatic mutation data:** used to validate mechanistic models (e.g., POLE/MMR-deficient tumours for replication-fidelity inferences; UV-exposed tumour clones for damage-to-mutation conversion kinetics).
- **Mutation accumulation cell lines and experimental biochemistry:** cited as mechanistic anchors for statistical inferences.

The analytical framework links four main statistical signals to biochemical mechanisms: (1) nucleotide context dependence (trinucleotide to heptanucleotide spectra), (2) strand asymmetries (T-asymmetry from TC-NER, R-asymmetry from replication), (3) large- and small-scale regional rate variation (replication timing, chromatin, nucleosome positioning, recombination), and (4) parental age and sex effects.

## Key Findings

**Replication as the dominant damage-to-mutation converter**
- The majority of damage-induced mutations arise during S phase replication, not via direct damage permanence. UV-irradiation experiments show mutation numbers in clones drop ~30-fold when replication is delayed 48 h, supporting pre-replication repair as essentially error-free.
- Mutation signatures from bulky mutagens are strongly R-asymmetric, consistent with damage-induced replication errors on lagging vs. leading strands.

**DNA repair system footprints**
- Nucleotide excision repair (NER): Global GG-NER reduced at nucleosome dyads (10-nucleotide periodicity). TC-NER depletion on the transcribed strand generates T-asymmetry; at least 10% of germline mutations are attributable to bulky DNA damage from the degree of T-asymmetry.
- Mismatch repair (MMR): More active on the lagging strand; loss in cancers (POLE/MMR-deficient) gives order-of-magnitude rate increases with characteristic R-asymmetric spectra.
- Base excision repair (BER): Spatially variable activity; 10-nucleotide periodicity at nucleosome level; CpG>TpG mutagenesis involves multiple BER-interacting mechanisms.

**Context dependence and hotspots**
- Trinucleotide context alone explains a major fraction of rate variation; extended (up to heptanucleotide) contexts provide up to 100-fold rate differences for some mutation types.
- Some extended contexts link to known biochemistry (e.g., TTTAAAA context → polymerase slippage; APOBEC deamination of TC motifs in hairpin loops on single-stranded DNA exposed during replication).
- Single-nucleotide hotspots in the human genome show 2–3 fold enrichment at sites diverged between humans and other Hominidae; some sites have up to 100-fold elevated mutation rates.
- Recombination has a very localised mutagenic effect: 5–50-fold elevation within a 1-kb window around a crossover, but this accounts for <1% of all mutations genome-wide.

**Regional rate variation**
- Large-scale (Mb) correlates with replication timing, which co-varies with chromatin structure; the mechanistic interpretation is complicated by the tight correlation between these factors.
- Nucleosome positioning contributes a 10-nucleotide periodicity; the overall effect on total mutation rate is small (<5%) but mechanistically interpretable.
- Transcription factor binding sites show ~20% higher germline mutation rates, partly attributable to biased sequence composition but potentially also to NER access or DNA conformation changes.

**Sex-specific differences and parental age**
- Paternal mutations outnumber maternal mutations ~4:1, driven by continuous spermatogonial cell divisions versus oocytes arrested in prophase I.
- Mutation spectra are broadly similar between parents except for a few mutation types; extended-context analysis reveals 10 pentanucleotide contexts where the maternal:paternal ratio is ~2:1 or ~1:3, implying distinct sex-specific mutagenic processes.
- CpG>TpG mutations have a large paternal age effect (scaling with cell divisions) but a weaker, distinct maternal age effect; ACG>ATG mutations lack R-asymmetry, suggesting they may not originate primarily from replication-mediated CpG deamination.
- Maternal-age-dependent clustered mutations (C>G enriched, ~6-fold above background clustering, occurring in specific genomic regions) are a distinctive feature of oogenesis, possibly from double-strand break repair in aged oocytes — they cannot be explained by replication infidelity.

**Early developmental mutations**
- Mutation rate is 3–10-fold higher in the first zygotic divisions versus differentiated germ-line; early developmental mutations have a distinctive spectrum (elevated TCT>TAT and GCA>GAA).
- Up to ~5% of de novo mutations arise as early developmental events and are detectable as mosaic variants.

## Relevance

**hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and (agnostic covariate ↔ signature-exposure association; positive-control recovery):** This review provides the mechanistic grounding for why mutational signatures carry aetiological information and which statistical properties encode which processes. Specifically:

- **Positive-control signatures for hypothesis:0007:** The paper enumerates the biochemical anchors for "canonical" signatures: UV (T-asymmetry from TC-NER + C>T at PyPy contexts), tobacco/PAH (G>T enrichment in dividing bronchial cells, R-asymmetric), APOBEC (C>G/T in TCA/TCT at hairpin single-stranded DNA during replication), and MMR deficiency (elevated rate, R-asymmetric, genome-wide). These are exactly the signatures hypothesis:0007 should recover as positive controls.
- **Covariates that map to known mechanisms:** Replication timing, transcription strand asymmetry, nucleosome positioning, and CpG methylation are all discussed as quantifiable genomic covariates that co-vary with specific signature exposures — directly relevant to hypothesis:0007's goal of associating covariates with exposures without prior aetiological assumptions.
- **Cross-study meta-analysis relevance:** The review explains why mutation spectra vary across cancer types (cell-type-specific replication schedules, tissue-specific mutagen exposures, DNA repair capacities) — the same heterogeneity the cbioportal cross-study aggregation pipeline must model. The CH-aware annotation in the pipeline (Bolton CH genes [@Bolton2020], matched-normal flag) is partly motivated by DNMT3A/TET2 activity that the review would classify as endogenous damage (oxidative, deamination).
- **Hypermutator annotation:** The mechanistic framework for POLE/MMR deficiency signatures described here directly underpins the pipeline's `is_hypermutator` classification and the `pole_hotspot`/`msi_h` reason codes.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Mutational signature (context-specific spectrum) | Mutational signature (COSMIC/SBS basis) | Same framework; paper is pre-COSMIC-v3.3 but compatible |
| T-asymmetry (TC-NER footprint) | Signature SBS4/SBS7 components | T-asymmetry is a positive-control observable for tobacco/UV |
| R-asymmetry (replication strand) | POLE/MMR signatures SBS10/SBS6 | R-asymmetry distinguishes replication-error vs. damage-induced |
| Paternal age effect / cell-division scaling | Study-level TMB (pipeline `compute_per_sample_tmb`) | Cell-division rate drives baseline TMB across tissues |
| CpG methylation × mutation rate | Pipeline `cancer_type_alias_map` / per-cancer GMM | CpG context contributes to per-histology TMB baseline |
| Maternal clustered mutations | Mutation clustering (not yet in pipeline) | Distinct from hypermutation; oocyte-specific DSB repair process |
| Early developmental mutation spectrum | Clonal hematopoiesis (CH) contamination | CH genes accumulate via early clonal expansions; distinct spectrum |

## Limitations

- As a review, it synthesises rather than tests — individual mechanistic claims cite primary sources that should be consulted for effect sizes and statistical power.
- Focus is on germline mutagenesis; somatic cancer applications are discussed by analogy, and the review cautions that some mechanisms (e.g., extreme mutagenic events) do not transfer directly to germline.
- The relative quantitative contributions of each mechanism to the total spontaneous mutation rate remain uncertain; the review explicitly flags this as a key open problem.
- Trio sequencing data available at time of writing was limited in power for rare mutation types and extended context analyses; some conclusions rest on population-level SNV proxies with their own confounders (selection, biased gene conversion, demography).
- Maternal clustered mutations remain mechanistically unexplained; the two leading hypotheses (DSB repair vs. unrepaired lesion accumulation) are not discriminated.

## Model / Tool Availability

No model or software tool is released with this review. Population-level SNV data referenced from gnomAD v2 (https://gnomad.broadinstitute.org/downloads). De novo mutation data come from published trio studies, including Jónsson et al. 2017 and Goldmann et al. 2016 and 2018 [@Seplyarskiy2021].

## Follow-up

- Seplyarskiy et al. 2021 (population sequencing study, bioRxiv) — companion empirical paper using population sequencing data to identify variation in mutational processes in the human germ line (REF 67 in this review; describes the first use of population variation in mutational spectra to dissect germline mutational processes).
- Jónsson et al. 2017 (Nature Genetics) — primary trio sequencing data for sex-specific and parental-age analyses.
- Goldmann et al. 2018/2019 — stochasticity and parent-of-origin signatures in de novo mutations.
- Volkova et al. [@Volkova2020] — mutational signatures jointly shaped by DNA damage and repair (cited as REF 15 here; relevant to hypothesis:0007 mechanism decomposition).
- For the project: the mechanistic taxonomy in this review (replication errors vs. damage conversion vs. repair deficiency) could serve as a structured vocabulary for annotating which hypothesis:0007 covariates are expected to correlate with which signature classes, providing an interpretability scaffold for agnostic association results.
