---
type: topic
title: "Pan-cancer interpretive frames (cell-of-origin vs alterations vs pathways)\
  \ \u2014 synthesis"
status: active
created: '2026-04-13'
updated: '2026-06-28'
id: topic:pan-cancer-interpretive-frames
ontology_terms: []
source_refs: []
related:
- topic:pan-cancer-mutation-landscape
- topic:cancer-driver-genes
- paper:Hoadley2018
- paper:SanchezVega2018
- paper:Ciriello2013
- paper:Bandlamudi2026
- paper:Bailey2018
---

# Pan-cancer interpretive frames: cell-of-origin vs alteration-type vs pathway (synthesis)

## Summary

When clustering cancer types by molecular features, the field has converged on three
non-equivalent organizing frames: **cell-of-origin / tissue lineage** [@Hoadley2018],
**alteration-type axis (M-class vs C-class)** [@Ciriello2013], and **canonical signaling
pathway membership** [@SanchezVega2018]. Each frame produces a different cancer-cancer
similarity structure, surfaces different cross-tissue convergences, and has different
implications for trial design and biological interpretation. None is the "right" frame —
they are complementary lenses on the same underlying data.

For our pipeline (`summary/mut/clusters/cancer.feather`), this synthesis matters because
**we cluster cancers by mutation patterns alone**, which is none of the above three frames
in pure form. Knowing how the published frames compare lets us interpret what our
clustering does and doesn't capture.

## Key Concepts

### The Three Frames

### Cell-of-origin (Hoadley et al. [@Hoadley2018], PanCanAtlas)

- **Method:** integrative iCluster on 4 platforms (CNA, methylation, mRNA, miRNA),
  ~10,000 TCGA tumors, 33 cancer types. **Mutations excluded from clustering input due
  to sparsity.**
- **Result:** 28 integrated clusters. For 16/33 cancer types, >80% of samples land in one
  cluster — i.e., tissue lineage dominates. For 6/33 types (BLCA, UCS, HNSC, ESCA, STAD,
  CHOL), molecular heterogeneity overwhelms tissue.
- **Cross-tissue clusters:** pan-squamous (LUSC + HNSC + CESC + squamous ESCA, shared 3q
  amplification), pan-GI (COAD + READ + STAD subgrouped by MSI / CIN / EBV-CIMP), pan-
  kidney (KIRC + KIRP), pan-stromal/immune C20 catch-all (25 of 33 cancer types).
- **Important caveat:** the "cell-of-origin dominates" claim was *not* tested against
  mutations-only clustering. Mutations were excluded from input due to sparsity, not
  because they were tested and found uninformative.

### Alteration-type axis (Ciriello et al. [@Ciriello2013], Nat Genet)

- **Method:** 479 "Selected Functional Events" (high-level GISTIC SCNAs + recurrent gene
  mutations + 13 epigenetically silenced genes) on 3,299 TCGA tumors / 12 cancer types;
  recursive network modularity yields M (mutation-driven) vs C (copy-number-driven) split.
- **Result:** the **cancer genome hyperbola** — somatic mutation count anti-correlated
  with SCNA burden; 17 M-subclasses + 14 C-subclasses. KIRC, GBM, LAML, COADREAD, UCEC-
  endometrioid land in M. OV, BRCA, LUSC, HNSC, UCEC-serous land in C. **TP53 is the
  C-class exception** (chromosomal-instability enabler).
- **Hoadley et al. [@Hoadley2018] partially walk this back** — adding methylation/mRNA/miRNA shifts ~2/3
  of tumors to clustering by tissue rather than by alteration-type. But the **M/C
  hyperbola itself remains a real, observable structure** even after Hoadley's reanalysis;
  the squamous, basal, and pan-GI cross-tissue clusters Ciriello first surfaced *are*
  preserved by Hoadley.

### Pathway membership (TCGA pathway analysis [@SanchezVega2018], PanCanAtlas)

- **Method:** 10 curated canonical signaling pathways (RTK-RAS, PI3K, Notch, Wnt, TP53,
  cell-cycle, Myc, TGF-β, Hippo, Nrf2). Per-(sample, pathway) binary alteration call from
  mutation + CNA + fusion + methylation, projecting per-gene events onto pathway
  membership.
- **Result:** **89% of tumors carry an alteration in ≥1 of 10 pathways**. RTK-RAS most
  pervasive (median ~46%, up to ~95% in melanoma); Nrf2 least pervasive pan-cancer (~4%)
  but enriched in squamous lineages. **152 mutually exclusive + 116 co-occurring pathway
  pairs.** Notable: TP53 + cell-cycle co-occurring (broad); PI3K + Nrf2 co-occurring (lung
  / esophageal / H&N squamous); RTK-RAS internal mutual exclusivity (EGFR vs ERBB2 vs
  KRAS).
- **Pathway-collapsing reveals cross-cancer convergence that gene-level views miss**:
  squamous lineages converge on Nrf2 + PI3K despite different gene-level driver lists.

## Current State of Knowledge

### How the Frames Relate

| Frame | Top-level axis | What it captures | What it loses |
|---|---|---|---|
| **Cell-of-origin** (Hoadley) | Tissue lineage / developmental program | Why most lineage-matched tumors look similar across many platforms | Mutation-specific signal; treats mutations as overlay only |
| **Alteration-type** (Ciriello) | M-class vs C-class hyperbola | Genome-instability axis; cross-tissue squamous / BRCA-deficient subclasses | Lineage; pathway-level convergence |
| **Pathway membership** [@SanchezVega2018] | Functional signaling output | Cross-cancer convergence on shared pathway dysregulation; mutual-exclusivity signal | Driver-specific allele effects; non-canonical pathways; tissue context |

The frames are **not competing; they are complementary**. A complete cross-cancer view
includes:
- *Lineage* (Hoadley) as the primary organizing axis when integrating multi-omic features.
- *M/C class* (Ciriello) as a secondary genome-instability descriptor.
- *Pathway membership* (Sanchez-Vega) as a functional collapse layer that surfaces
  convergence the other two miss.

## Relevance to This Project

### What Our Mutation-Only Clustering Captures

Our pipeline currently produces `summary/mut/clusters/cancer.feather` from gene-level
mutation patterns alone. None of the three published frames did exactly this:

- Hoadley *excluded* mutations from clustering input (sparsity).
- Ciriello included mutations but at the SFE level (recurrent + filter for
  hypermutators); SCNAs co-equal in the model.
- Sanchez-Vega *collapsed* mutations to pathway membership; the unit is pathway, not gene.

So our mutation-only clustering is genuinely complementary, not redundant. **Concrete
hypotheses to test against published frames:**

1. **Pan-squamous cluster.** If our mutation clusters reproduce LUSC + HNSC + CESC +
   squamous ESCA grouping (shared TP53 + 3q-amp signature), that's strong concordance
   with Hoadley. If not, mutations alone may not be sufficient to recover this cluster.
2. **Pan-GI MSI subgroup.** Hypermutated MSI tumors across COAD / READ / STAD should
   cluster together by mutation pattern alone (extreme TMB + MMR signature). Worth
   verifying as a sanity check.
3. **C20-style stromal/immune catch-all.** Hoadley's 25-of-33-cancer-type cluster was
   driven by stromal/immune *expression*, not mutations. We should *not* see anything
   analogous in our mutation-only clustering. If we do, it likely indicates a confounder
   (cohort composition, panel coverage).
4. **Bandlamudi non-canonical context.** Mutations clustering by gene without tissue
   stratification may produce clusters that ignore the "tissue context matters" finding.
   A tissue-conditional driver flag (see `topic:cancer-driver-genes`) is the natural
   counterweight.

## Pipeline Implications

Concrete additions surfaced from this synthesis:

1. **Sanchez-Vega pathway overlay.** Tables S2/S3 (pathway membership) downloadable as
   supplements; pathway-collapsing rule analogous to Bailey driver overlay. Outputs:
   per-(cancer, pathway) alteration-rate table + per-tumor pathway-burden table.
   **Tractable, similar effort to Bailey overlay.**
2. **M/C-class descriptor.** Compute mutation-count vs SCNA-burden axis per tumor /
   per cancer; report cancer-type-level M-class fraction. Cheap secondary descriptor.
   **Requires CNA data ingestion, which our pipeline does not currently have.**
3. **Cluster comparison report.** Side-by-side: our mutation-only clusters vs Hoadley's
   integrated clusters. Where do they agree (validates our pipeline)? Where do they
   differ (where mutations carry non-lineage signal)?

## Key References

- Hoadley2018 — cell-of-origin / iCluster on multi-omics; 28 integrated clusters across
  10,000 TCGA tumors.
- Ciriello2013 — M-class vs C-class hyperbola; 17 + 14 subclasses.
- SanchezVega2018 — 10 canonical pathways; 89% tumors with ≥1 altered; pathway-pair
  exclusivity / co-occurrence.
- Bandlamudi2026 — non-canonical context finding; an extension of the tissue-conditional
  theme.
- Bailey2018 — per-cancer-type driver-gene rosters (an alternative tissue-aware view).
- See also: `topic:cancer-driver-genes`, `topic:pan-cancer-mutation-landscape`.
## Project Links

Key paper references are `paper:Hoadley2018`, `paper:SanchezVega2018`, `paper:Ciriello2013`,
`paper:Bandlamudi2026`, and `paper:Bailey2018`.
