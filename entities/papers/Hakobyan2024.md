---
type: paper
title: Pan-cancer analysis of the interplay between mutational signatures and cellular
  signaling
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: paper:Hakobyan2024
ontology_terms:
- mutational signatures
- signaling pathways
- pan-cancer analysis
- signature interactions
- patient survival
datasets: []
source_refs:
- cite:Hakobyan2024
related: []
---

# Pan-cancer analysis of the interplay between mutational signatures and cellular signaling

- **Authors:** Anna Hakobyan, Mathilde Meyenberg, Nelli Vardazaryan, Joel Hancock, Loan Vulliard, Joanna I. Loizou, Jorg Menche
- **Year:** 2024
- **Journal:** iScience (Cell Press), vol. 27, 109873
- **DOI/URL:** https://doi.org/10.1016/j.isci.2024.109873
- **BibTeX key:** Hakobyan2024
- **Source:** PDF

## Key Contribution

This paper introduces a systematic framework for characterizing pairwise interactions between
mutational signatures (signature-signature) and between signatures and oncogenic signaling
pathway alterations (signature-pathway), applied across TCGA and PCAWG datasets. The framework
uses four complementary metrics — Fisher's exact test co-occurrence, bias-corrected mutual
information (BCMI), Spearman correlation, and compositional data analysis (CoDa) — to capture
linear and nonlinear relationships, then evaluates the clinical impact of detected interactions
via Cox regression survival models. The study identifies hundreds of positive and negative
interactions, both tissue-shared and tissue-specific, and shows that a subset have significant
independent effects on patient survival.

## Methods

**Data:** Mutational signature activities (SBS) extracted from TCGA (3,132 samples, 12 tissues
after quality filtering) and PCAWG (1,471 samples, 14 tissues). Signatures were grouped by
COSMIC v3.2 etiology annotation. Ten oncogenic signaling pathways (cell cycle, HIPPO, MYC,
NOTCH, NRF2, PI3K/AKT/RAS, RTK-RAS, TGFb, TP53, b-catenin/WNT) were mapped using previously
published driver mutation data harmonized to TCGA and PCAWG.

**Signature-signature interaction metrics:** Four complementary metrics computed per tissue
independently, with bootstrapped significance thresholds at 5th/95th percentile of a
signature-shuffled null model:
1. Fisher's exact test on binary co-occurrence of signature activities
2. Bias-corrected mutual information (BCMI) via jackknife correction for nonlinear/nonmonotonic
   associations
3. Spearman rank correlation
4. CoDa (compositional data analysis) using symmetric pivot coordinates + Pearson correlation
   — addresses the compositional nature of signature attribution (counts summing to the same
   total); applicable only when both signatures are present

Interactions supported by at least two metrics were retained and classified positive or negative.

**Signature-pathway interactions:** Two strategies — (1) Fisher's exact test on binary
co-occurrence/exclusivity across contingency tables; (2) linear and logistic regression models
of signature activity against driver event counts per pathway — providing both binary detection
and quantitative effect size.

**Survival analysis:** Cox proportional hazards models with age at diagnosis, cancer type, and
log-TMB as covariates. Two model classes: (1) full interaction model with interactor-specific
and interaction-term coefficients; (2) class-based model assigning samples to
(none/int1-only/int2-only/both) groups. Model selection via partial likelihood ratio test (PLR)
for non-nested models and likelihood ratio (LR) test for nested models. Analysis required ≥ 30
samples per tissue. A mutsigapp R package and web application were released.

**Tissues excluded:** Those with fewer than 25 samples (PCAWG) or 25 samples (TCGA); samples
with reconstruction accuracy < 0.85 or < 90 total mutations were removed.

## Key Findings

**Signature-signature interaction networks:**
- In PCAWG: 88 positive and 50 negative interactions across 25 tissues; in TCGA: 50 positive
  and 47 negative interactions.
- Cross-tissue core: strong positive interactions between clock-like signatures SBS1, SBS5, and
  SBS40 — by-products of basic cellular repair and aging shared across tissues.
- Endogenous processes (APOBEC, HRD/DDR) are densely interconnected, consistent with shared
  pathway membership.
- APOBEC (SBS2/13 family) interacts positively with HRD in three tissues (breast, esophageal,
  pancreatic), consistent with APOBEC dysregulation promoting genomic instability that triggers
  HR.
- Unexpected negative interaction between SBS38 and UV signature: UV and SBS38 appear mutually
  exclusive, suggesting SBS38 is UV-independent despite earlier speculation.
- 27 interactions shared between PCAWG and TCGA with matching tissue and directionality; SBS5
  was the most common shared interaction partner (linked to both environmental and endogenous
  signatures across tissues).

**Signature-pathway interactions:**
- HRD signature and TP53 pathway interact positively in breast adenocarcinoma but negatively in
  pancreatic neuroendocrine tumors — opposing directionality reflects alternative routes of
  tumorigenesis.
- In stomach adenocarcinoma, hierarchical clustering by signature activities separates two
  molecular subtypes: C1 (high dMMR, high NOTCH/WNT/TGFb/HIPPO/PI3K driver burden) vs C2
  (high SBS40/SBS17/APOBEC, low MMR, distinct driver profile) — demonstrating that signature
  compositions predict driver pathway enrichment.
- In melanoma, high-UV samples enrich for RTK-RAS mutations; UV-low samples carry HIPPO/NOTCH
  alterations and higher SBS38/APOBEC/SBS40.
- Clock-like signatures (SBS1, SBS5) show strong positive interactions with nearly all pathway
  alterations in TCGA — consistent with age as the dominant cancer risk factor.
- C>T mutations in CpG context (clock-like SBS1) are enriched among TP53 pathway mutations in
  pancreatic adenocarcinoma (hypergeometric p = 0.002), suggesting aging-related spontaneous
  deamination as a primary source of TP53 driver mutations in this cancer type.

**Survival effects:**
- In PCAWG hepatocellular carcinoma: positive SBS1 + SBS40 interaction associated with
  compromised survival, but co-carrying both rescues phenotype; negative SBS29 + SBS40
  interaction significantly worsens survival (HR = 6.42, 95% CI [1.22, 33.83]).
- In TCGA colorectal adenocarcinoma: positive MMR + SBS5 interaction significantly improves
  survival (HR = 0.037, 95% CI [0.007, 0.2]) when both are carried; negative MMR + SBS40
  interaction worsens it (HR = 24.54, 95% CI [3.9, 154.58]).
- In melanoma: positive UV + clock-like SBS1 interaction significantly ameliorates survival
  (HR = 0.14, 95% CI [0.036, 0.54]).
- In PCAWG, negative ROS (SBS18) + SBS40 interaction worsens survival across pancreatic,
  prostate, ovarian adenocarcinomas and medulloblastoma (pooled HR = 2.62, 95% CI [1.29, 5.29]).
- In TCGA, negative APOBEC + NOTCH pathway interaction worsens survival (HR = 10.92, 95%
  CI [1.33, 89.9]).
- TMB had no survival effect in 17 of 23 tissues evaluated; positive for 5 tissues.

**Framework validation:** Known causal relationships were recovered (UV → RTK-RAS mutations in
melanoma; aging/SBS1 → TP53 mutations in pancreatic cancer), confirming biological validity.

## Relevance

This paper is directly relevant to hypothesis **h08** (agnostic covariate-signature association,
positive-control recovery of known aetiologies):

- **H08a positive-control linkages recovered here:** The signature-pathway regression framework
  recovers the UV→RTK-RAS driver link in melanoma and the aging/clock→TP53 link in pancreatic
  adenocarcinoma — two of the three positive controls in h08's pre-registration (UV→SBS7 in
  skin is implicit; smoking→SBS4 is not examined in this pathway-level study, but UV and
  clock-like are confirmed). This demonstrates that covariate-association methods can recover
  known exposure→signature→driver chains from the same TCGA/PCAWG data we would use.

- **APOBEC-HRD interaction as a positive control for h08:** The positive APOBEC-HRD
  signature-signature interaction (breast, esophageal, pancreatic) is consistent with APOBEC
  expression being a mechanistic upstream input to the HRD signature. This provides an
  experimental grounding for h08's prediction that APOBEC3 mRNA expression will associate more
  strongly with SBS2/13 than any single clinical label.

- **SBS5 and SBS40 (clock-like / unknown aetiology) prominently emerge:** Both signatures are
  centrally embedded in the interaction networks and drive several survival effects; their
  aetiology remains only partly understood. The paper identifies SBS40 as behaviorally distinct
  from SBS5 (later-stage, subclonal, distinct interaction preferences) — directly motivating
  h08b's aim to use expression modules to resolve upstream causes of these clock-like signatures.

- **Within-tissue, multi-tissue design mirrors h08's analysis strategy:** Using within-tissue
  independence tests corrected for the tissue-composition structure is exactly the design
  required by h08's Prediction 4 (associations attenuate when not conditioned on tissue). This
  paper provides a methodological template.

- **Signature-pathway interaction methods complement h08's expression-based approach:** The
  CoDa metric for compositional signature data and bootstrapped null models would be directly
  applicable when regressing signature exposures against co-measured expression covariates
  (export_study_expression.py outputs). CoDa handles the shared-attribution problem that would
  otherwise inflate cross-signature associations.

- **Potential covariate for the cross-study pipeline:** The driver pathway alteration tables
  used here (TP53, PI3K, RTK-RAS, etc.) are a complementary structured covariate that the
  cBioPortal meta-analysis could link to signature exposures from TCGA MC3.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Signature activities matrix (patients × signatures) | `H` matrix from NMF / SigProfiler assignment | Paper uses COSMIC SBS v3.2 pre-computed extractions |
| CoDa metric for compositional signatures | potential addition to h08 association layer | Addresses shared-attribution compositional problem |
| Signature-pathway co-occurrence (Fisher) | signature-covariate association (h08 agnostic scan) | Pathway binary is one type of covariate; expression module is another |
| Within-tissue bootstrap null | within-tissue FDR in h08 design | Same principle; paper uses percentile bootstrap, h08 plans BH FDR |
| dMMR/MSI-high samples (C1 cluster) | `is_hypermutator` / `msi_h` annotation | Paper clusters confirm that dMMR co-segregates with specific driver profiles |
| SBS40 (subclonal/late-stage) vs SBS5 (clonal) | unannotated clock-like target signatures for h08b | Paper's survival findings motivate resolving their expression correlates |
| mutsigapp R package | external tool (web app available) | Code + web app released; method reproducible |

## Limitations

- Only SBS signatures considered; indels, doublet-base substitutions, and copy-number variants
  are excluded — may miss important mutagenic processes.
- TCGA and PCAWG have vastly different sample numbers per tissue, limiting power for some
  tissue-specific interactions; the authors note interactions scale with sample count (Fig S1C).
- Signatures were extracted by Alexandrov et al.; different extraction methods can yield
  different signature activities.
- Spatial, temporal, and clonality structure of mutations were not accounted for — the
  framework treats all mutations as a single sample-level aggregate.
- The CoDa metric can only be applied to samples where both signatures are active,
  reducing effective sample size for rarer signatures.
- Survival analyses required relatively high sample numbers; many interactions could not be
  tested for clinical impact, and several survival estimates have wide confidence intervals due
  to small group sizes.
- Causal directionality of signature-pathway interactions cannot be definitively established
  from observational data alone (acknowledged by authors).

## Model / Tool Availability

- **mutsigapp R package:** released, implements signature-signature and signature-pathway
  interaction analysis
- **Web application:** https://ahakobyan.shinyapps.io/mutsigapp/ — provides a browser-accessible
  resource for querying PCAWG and TCGA signature interactions
- **License:** not specified in the accessible portions of the paper
- Data from TCGA and PCAWG (public)

## Follow-up

- The mutsigapp web app enables querying PCAWG/TCGA signature interactions by tissue, which
  could inform which signature pairs to prioritize as h08 positive controls.
- The CoDa approach to compositional signature data should be evaluated for inclusion in h08's
  association layer (relevant to the multi-signature attribution problem flagged in h08's R4
  alternative).
- The survival stratification by signature interaction (e.g., MMR+SBS5 in colorectal vs
  MMR+SBS40) raises a question for h08b: do expression modules that distinguish SBS5 from SBS40
  activity also predict survival in these tissues?
- The negative APOBEC-MMR interaction in breast, stomach, and uterine adenocarcinomas (mutual
  exclusivity) should be compared against h08's APOBEC3 expression-SBS2/13 positive control:
  if APOBEC expression associates with SBS2/13 but not dMMR signatures, the mutual exclusivity
  may be a clone-selection effect rather than a mechanistic interaction.
- Papers to read alongside: any work on the clonal vs subclonal origin of SBS40 vs SBS5 (to
  understand the survival divergence); Alexandrov 2020 (signature extraction), Degasperi 2022
  (refitting approaches).
