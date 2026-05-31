---
id: "paper:Besselink2023"
type: "paper"
title: "The genome-wide mutational consequences of DNA hypomethylation"
status: "active"
ontology_terms:
  - DNA methylation
  - mutational signatures
  - chromosomal instability
  - epigenetics
  - DNMT1
  - CRISPRi
datasets:
  - "hTERT RPE-1 CRISPRi DNMT1-knockdown cell line (in vitro, 3 clones)"
source_refs:
  - "cite:Besselink2023"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# The genome-wide mutational consequences of DNA hypomethylation

- **Authors:** Nicolle Besselink, Janneke Keijer, Carlo Vermeulen, Sander Boymans, Jeroen de Ridder, Arne van Hoeck, Edwin Cuppen, Ewart Kuijk
- **Year:** 2023
- **Journal:** Scientific Reports
- **DOI/URL:** https://doi.org/10.1038/s41598-023-33932-3
- **BibTeX key:** Besselink2023
- **Source:** PDF (local); metadata confirmed via Europe PMC (PMC10140063, PMID 37106015)

## Key Contribution

Global DNA hypomethylation — a hallmark of cancer — does not increase single-nucleotide mutation
burden or enrich for any COSMIC mutational signature, including MMR-related ones. Instead, the
dominant consequence of genome-wide hypomethylation is chromosomal instability (CIN), driven by
pericentromeric methylation loss. The finding decouples point-mutation aetiology from
hypomethylation and reframes CIN as the primary engine through which cancer epigenetic
reprogramming fuels tumour heterogeneity.

## Methods

The study used CRISPRi (dCAS9-KRAB + doxycycline-inducible sgRNA) to conditionally knock down
DNMT1 in hTERT-immortalised RPE-1 cells (human female retinal pigment epithelium; near-diploid,
non-transformed), creating an isogenic model of global DNA hypomethylation. Cells were also made
TP53-null to increase tolerance for accumulated genomic variation. Three independent clonal
lines were generated; experiments used clone 2 for depth.

Key assays:

- **EPIC 850k methylation arrays** — genome-wide methylation quantification over 850,000 CpG
  sites (genes, promoters, CGIs) after 6 weeks of doxycycline.
- **RNA-seq** — differential expression profiling (TruSeq Stranded Total RNA).
- **Whole-genome sequencing (WGS)** — single-cell DNA sequencing for copy-number profiling;
  PURPLE VCF-based SBS/DBS/indel calling; MutationalPatterns R package (with COSMIC
  compatibility) for signature analysis.
- **Nanopore long-read sequencing** — pericentromeric methylation assessed via direct 5mC
  detection mapped against the T2T reference genome (repetitive regions inaccessible to
  array-based methods).
- **Microscopy** — nuclear morphology scoring.

Sample size: n = 3 per condition (knockdown vs. untreated controls), in line with comparable
published in-vitro mutational signature studies.

## Key Findings

1. **Methylation loss magnitude matches cancer.** DNMT1 knockdown produced a genome-wide mean
   β-value reduction of ~10% (regions with β > 0.5 showed −16%), comparable to reductions
   observed in colorectal, lung, and breast cancers. Loss was uniform across genes, promoters,
   and CpG islands.

2. **No increase in SBS burden or signature enrichment.** SBS mutation counts did not differ
   significantly between hypomethylated and control cells (Student's t-test, p = 0.18). Indel
   counts likewise showed no significant increase (p = 0.33). The 96-channel mutational
   profiles and spectra were highly similar between conditions. Notably, MMR-associated
   signatures (anticipated because methylation loss had previously been linked to MMR deficiency)
   were not enriched.

3. **No structural variation accumulation.** Hypomethylation did not lead to detectable increases
   in structural variants.

4. **Transcriptional derepression and inactive-X reactivation.** RNA-seq identified 501
   upregulated and 73 downregulated genes (p_adj < 0.05). X-chromosome genes were
   disproportionately upregulated, indicating partial reactivation of the inactive X.

5. **Chromosomal instability (CIN) is the primary genomic consequence.** Single-cell DNA
   sequencing after 6 weeks revealed increased aneuploidy and higher cell-to-cell copy-number
   heterogeneity in knockdown clones. Nanopore sequencing confirmed pericentromeric hypomethylation
   in knockdown cells, consistent with CIN being driven by disrupted centromere function. Proposed
   (non-exclusive) mechanisms include: increased recombination of centromeric repeats, DNA breaks
   in centromeres, dysregulation of the centromeric protein network, increased α-satellite
   transcription, defective kinetochore assembly, and premature cohesion loss.

6. **Growth retardation without arrest.** Proliferation was reduced ~50% but cells continued
   dividing, enabling accumulation of chromosomal changes over time.

## Relevance

**h08 (agnostic covariate-signature association; H08a positive-control recovery; H08b discovery):**

The paper provides direct experimental evidence that global hypomethylation is not itself a
mutational process generating characteristic SBS patterns. This is directly relevant to h08
in two ways:

- **Null for a candidate confound (H08a/b):** The cross-study meta-analysis pipeline holds
  methylation-associated covariates only implicitly (through cancer type, tissue site). If an
  agnostic covariate scan were to associate a DNMT-expression module with SBS exposures, this
  paper constrains the causal interpretation: any such association would more likely reflect
  co-occurring processes (e.g., MMR-loss in hypermethylated tumours, or CIN-driven copy-number
  artefacts inflating apparent TMB) rather than methylation directly inducing a mutagenic
  process.
- **CIN as a confound in TMB-based analyses:** The paper underscores that hypomethylation
  promotes CIN. If hypomethylated tumours show elevated apparent TMB in cBioPortal studies,
  that elevation could reflect CIN-associated copy-number changes rather than increased point
  mutations — a potential confounder in the pipeline's `_inclusive` / `_exclusive` hypermutator
  stratification.
- **Positive-control recovery:** The paper confirms that MMR-loss/MSI (SBS6/15/26) and
  hypomethylation are separable processes — important for validating that the h08a scan does
  not erroneously fuse them.

**Cross-study meta-analysis:** Tumours with global hypomethylation (e.g., many colorectal,
lung, breast cancer studies in cBioPortal) carry increased CIN rather than increased point
mutation load per se. This supports treating CIN-driven heterogeneity as distinct from TMB
when characterising studies in the pipeline.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| DNMT1 knockdown → genome-wide hypomethylation | Epigenetic covariate (implicit, not currently measured) | Not a direct pipeline input; informative for causal interpretation |
| SBS burden (no change) | TMB (`compute_per_sample_tmb`) | Hypomethylation does not drive elevated TMB |
| Chromosomal instability (CIN) | Structural variation / aneuploidy | CIN is the primary consequence; not captured by SBS pipeline |
| MMR-related signatures not enriched | SBS6/15/26 (MMR-loss positive controls in h08a) | Methylation loss and MMR deficiency are separable |
| Pericentromeric hypomethylation → CIN | Potential CIN confounder in TMB estimation | Relevant to hypermutator annotation pipeline |

## Limitations

- Small sample size (n = 3 per condition); power sufficient to detect large effects but the
  authors acknowledge that subtle mutational processes cannot be fully ruled out.
- Single cell line (RPE-1, female, retinal pigment epithelium); generalisability across tissue
  types or transformed cell backgrounds is unclear.
- TP53 knockout required to permit mutation accumulation, which alters the cellular response to
  DNA damage; may not faithfully recapitulate p53-wild-type tumour contexts.
- Duration limited to 6 weeks; long-term or cumulative effects of hypomethylation on SBS
  processes cannot be excluded.
- The study cannot address whether hypomethylation acts synergistically with other oncogenic
  stressors (e.g., RAS activation, oxidative stress) to shape mutational output.

## Model / Tool Availability

- MutationalPatterns R package (used for COSMIC-compatible SBS/DBS/indel analysis) — available
  on Bioconductor (not the primary output of this paper, but mentioned as the analysis tool).
- No dedicated software or model released with the paper.

## Follow-up

- Does pericentromeric hypomethylation measurably inflate apparent TMB in cBioPortal studies
  via CIN-driven artefacts? Relevant to hypermutator annotation (t081/t092-t099).
- How does this finding interact with the known co-occurrence of hypomethylation and MMR loss
  in MSI-high colorectal cancer (MLH1 promoter methylation silencing)? That mechanistic link
  is distinct from hypomethylation itself being mutagenic.
- Are there COSMIC signatures attributed to CIN-related processes (e.g., SV signatures) that
  might show up as positively associated with DNMT-expression modules in an h08 scan?
