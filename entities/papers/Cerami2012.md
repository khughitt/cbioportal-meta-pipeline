---
type: paper
title: 'The cBio cancer genomics portal: an open platform for exploring multidimensional
  cancer genomics data'
status: read
created: '2026-04-13'
updated: '2026-06-28'
id: paper:Cerami2012
ontology_terms: []
source_refs:
- article:Cerami2012
related:
- paper:Gao2013
dataset_usage:
- ref: dataset:cbioportal
  role: analyzed
  overlap: full
---

# The cBio cancer genomics portal: an open platform for exploring multidimensional cancer genomics data

- **Authors:** Cerami E, et al.
- **Year:** 2012
- **Journal:** Cancer Discovery
- **PMID:** 22588877
- **BibTeX key:** Cerami2012

## Key Contribution

This cBioPortal platform note links paper:Gao2013.

Introduces the cBio Cancer Genomics Portal as a web resource that lowers the barrier
to reusing large-scale cancer genomics data (TCGA, ICGC, and published studies) by
integrating mutations, copy number, expression, methylation, RPPA, and clinical
attributes under a single query model. The central abstraction is the
"altered gene" — a per-sample binary call combining mutation, homozygous deletion,
amplification, and thresholded expression — which makes heterogeneous multi-platform
data directly comparable across genes, samples, and studies.

## Methods

The portal is organized around three entities: **cancer studies**, **genomic
profiles** (one per data type / platform), and **patients/samples** with clinical
metadata. Supported data types at publication: somatic mutations, copy-number
alterations (amplification / homozygous deletion), mRNA expression (microarray and
RNA-seq), DNA methylation, protein and phosphoprotein levels (RPPA), and clinical
attributes including overall and disease-free survival.

The user workflow is a four-step query: pick a study, select genomic profiles,
choose a case set, enter a gene list or pathway. An **Onco Query Language** allows
fine-grained filtering of which alteration types count (e.g., homozygous deletions
and mutations only).

The platform exposes a web-service API with MATLAB and R client libraries. Source
code is released under the GNU LGPL (hosted on Google Code at publication), and
prebuilt Amazon Machine Images are provided for local installation.

## Key Findings

At publication (May 2012) the portal hosted **~5,000 tumor samples across 20 cancer
studies** — 5 published datasets with mutation data (including GBM, ovarian,
prostate, soft-tissue sarcoma) plus 15 provisional TCGA datasets refreshed monthly.
The platform enables several concrete analyses from a single query: **OncoPrint**
summary matrices (genes x samples) showing mutual-exclusivity patterns (demonstrated
on the RB pathway in GBM); **Mutation Details** with MutationAssessor functional-impact
scores, multiple-sequence alignments, 3D structure viewing, and Pfam-domain hotspot
plots (e.g., BRCA1 185delAG / 5382insC); **correlation plots** linking copy number
to mRNA (CDK4 amplification in GBM); **Kaplan-Meier survival** comparing altered vs.
unaltered cases (RB-pathway-altered GBM, p = 0.0513); **protein/phospho-protein
t-tests** (PTEN loss vs. AKT phosphorylation in ovarian); and an interactive
**network view** built on Pathway Commons that overlays alteration frequencies. A
worked example uses BRCA1/BRCA2 as seeds to nominate EMSY and Fanconi Anemia genes
as alternative routes to HR deficiency in ovarian cancer.

## Relevance

Required citation whenever this project publishes results derived from cBioPortal data.

## Limitations

Data coverage in 2012 was small by current standards (20 studies, ~5,000 samples),
with most TCGA cohorts still "provisional" and mutation calls pending for 15 of
them. OncoPrints were static images rather than interactive, bulk/batch download
of full datasets was not yet supported, miRNA expression support was incomplete,
and per-study summary reports (e.g., recurrently mutated genes) were not yet
available. Local installation required system-administrator effort. The authors
frame cBio as complementary to — not a replacement for — the TCGA/ICGC data
portals, IGV, the UCSC Cancer Genomics Browser, and IntOGen.

## Follow-up

- Gao2013 — companion paper on integrative analysis and API.
- Authors' stated roadmap (targeted for the third quarter of 2012): add >=5 additional cancer types
  and >1,000 samples, full miRNA support, interactive OncoPrints, batch dataset
  download, per-study summary reports, and expanded cross-cancer query capabilities.
