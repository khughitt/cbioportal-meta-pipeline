---
id: "paper:Chang2016"
type: "paper"
title: "Identifying recurrent mutations in cancer reveals widespread lineage diversity and mutational specificity"
status: "read"
ontology_terms: []
datasets: []
source_refs: ["article:Chang2016"]
related: ["paper:Cerami2012", "paper:Chakravarty2017", "topic:hotspot-based-driver-detection", "topic:cancer-driver-genes", "topic:mutation-rate-normalization"]
created: "2026-04-13"
updated: "2026-04-13"
---

# Identifying recurrent mutations in cancer reveals widespread lineage diversity and mutational specificity

- **Authors:** Chang MT, et al.
- **Year:** 2016
- **Journal:** Nature Biotechnology
- **PMID:** 26619011
- **DOI:** 10.1038/nbt.3391
- **BibTeX key:** Chang2016

## Key Contribution

Introduces a residue-level statistical framework that identifies single-amino-acid
mutational hotspots independently of gene-level recurrence, and applies it to an
11,119-tumor pan-cancer cohort to produce a catalog of 470 statistically significant
hotspots across 275 genes. The work reframes driver discovery away from gene counts
toward allele-specific recurrence and documents pervasive lineage diversity among
hotspot alleles.

## Methods

The authors model the number of tumors bearing a mutation at a given residue as
a binomial random variable, Pr(X = k) = C(n,k) p^k (1-p)^(n-k), where the
per-codon background probability p is the product of (i) a trinucleotide-context
mutability coefficient m_t capturing sequence-context variation in substitution
rates, (ii) a gene-level mutation rate μ_g normalized by gene length in amino
acids, and (iii) a within-gene relative codon mutability r_{c,g}. Background rates
are computed on a truncated distribution that excludes the top 99th-percentile
positions, preventing dominant hotspots (e.g., BRAF V600, KRAS G12) from
inflating their own gene's baseline. A floor is applied by taking the max of the
computed p' and the 20th percentile of all p' across the dataset, further
guarding against under-dispersion. Per-gene false discovery is controlled with
the Benjamini–Yekutieli procedure at q < 0.01. Input: 2,007,694 somatic
coding substitutions from 11,119 tumors across 41 cancer types spanning 9 major
organ systems, pooled from TCGA, ICGC, and published studies (exome / WGS;
median 57 mutations per tumor). Code and hotspot calls are released at
<https://github.com/taylor-lab/hotspots>.

## Key Findings

470 significant hotspots were identified across 275 genes, and 54.8% of all
tumors carried at least one. Of these, 243 (≈51.7%) are novel "Level-1" alleles
with no prior recurrence or functional annotation, 46 are newly multi-cancer
("Level-2"), and 181 are previously characterized ("Level-3"). Lineage
distribution is broad: 81% of hotspots recur in ≥2 tumor types and only 7.6%
of multi-type hotspots stay within a single organ system — arguing that most
hotspot alleles are not lineage-specific, though 27 hotspots (5.7%) are
significantly enriched in squamous lineages. 49 genes harbor ≥2 hotspots.
Hotspot alleles are more often clonal than non-hotspot mutations in the same
genes (χ², p = 1×10⁻¹⁴). 34 of 35 novel hotspots tested were confirmed by
reprocessing raw reads through an independent pipeline. Experimental validation
of RAC1 A159V (a long-tail allele) showed PAK1 activation matching or exceeding
constitutively active RAC1-GTPγS, and greater than the known oncogenic RAC1
P29S; RAC1 Q61R was similarly activating. RRAS2 Q72 is flagged as paralogous to
KRAS Q61 (q = 8×10⁻¹⁵).

## Relevance

Residue-level, recurrence-based driver detection is a complementary axis to the gene-level counting
this pipeline currently performs. Directly informs any future "functional-filter" pass on our gene
x cancer matrices. The 3D-spatial generalization (Gao et al. 2017, *Cancer Cell*) builds on this
residue-level model.

## Limitations

- Substitutions only: no indels, copy-number alterations, structural variants,
  fusions, or epigenetic events, despite their driver roles.
- Single-residue resolution: clusters of nearby residues in primary sequence or
  3D space that share a mechanism but spread their signal across codons are
  underpowered; this is the gap the later 3D-hotspot generalizations target.
- Sensitivity to input quality: relies on heterogeneous mutation calls
  aggregated from many studies with different callers and filters; private /
  ultra-rare driver alleles remain difficult to distinguish from background.
- Cohort representativeness: treatment-naïve primaries dominate, so
  resistance-associated hotspots are under-sampled.
- Mechanism is not inferred — most novel hotspots lack functional confirmation
  beyond statistical recurrence.

## Follow-up

- 3D spatial generalization: the same group (Gao et al., 2017, *Cancer Cell*)
  extended the residue-level model to detect hotspots that are adjacent in
  protein tertiary structure rather than in primary sequence, recovering
  additional low-recurrence drivers missed by the 1D method.
- Clinical / knowledge-base integration: hotspot calls from this catalog feed
  into [OncoKB](Chakravarty2017.md) variant-effect annotations and are surfaced
  in cBioPortal's OncoPrint and mutation views.
- The public GitHub release (`taylor-lab/hotspots`) provides the hotspot list as
  a reusable reference — usable as a residue-level overlay on top of the
  gene-level matrices this pipeline produces.
