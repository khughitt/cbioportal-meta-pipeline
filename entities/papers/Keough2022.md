---
type: paper
title: Neural Signaling in Cancer
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: paper:Keough2022
ontology_terms:
- cancer neuroscience
- neural signaling
- glioma
- brain metastasis
- neurotrophins
- synaptic signaling
- tumor microenvironment
- perineural invasion
- autonomic innervation
datasets: []
source_refs:
- cite:Keough2022
related:
- paper:Mancusi2023
- paper:Venkatesh2019
- paper:Hanahan2023
- paper:Magnon2023
- paper:Hwang2025a
- paper:Huang2023a
- paper:Huang2025a
- paper:Wang2025b
- paper:Wu2025a
- paper:Kizil2024
- paper:Pu2025
- paper:Cortese2020
- paper:Mravec2008
- paper:Lu2026
- paper:Fan2024
- paper:Xiong2023
- paper:Cao2023
- paper:Kulke2012
- paper:Ahmed2020
- paper:Tan2024
---

# Neural Signaling in Cancer

- **Authors:** Michael B. Keough, Michelle Monje
- **Year:** 2022
- **Journal:** Annual Review of Neuroscience, 45:199–221
- **DOI:** https://doi.org/10.1146/annurev-neuro-111020-092702
- **BibTeX key:** Keough2022
- **Source:** PDF

```bibtex
@article{Keough2022,
  title   = {Neural Signaling in Cancer},
  author  = {Keough, Michael B. and Monje, Michelle},
  journal = {Annual Review of Neuroscience},
  year    = {2022},
  volume  = {45},
  pages   = {199--221},
  doi     = {10.1146/annurev-neuro-111020-092702}
}
```

## Key Contribution

This review from the Monje lab (Stanford) synthesizes the emerging field of cancer neuroscience, arguing that neural signaling mechanisms normally reserved for neurodevelopment and plasticity are systematically co-opted by tumors to drive malignant growth. The paper introduces a bidirectional, feed-forward model: neuronal activity stimulates tumor growth via paracrine and synaptic mechanisms, while tumors remodel neural circuits to amplify those same pro-growth signals. Coverage spans primary brain tumors (especially high-grade gliomas), brain metastases (breast, lung), and solid organ tumors innervated by the peripheral nervous system (prostate, stomach, pancreas, breast). The review is notable for grounding cancer-neural crosstalk firmly in normal neurodevelopmental biology — myelination, OPC proliferation, synaptic pruning, axon pathfinding — positioning tumors as developmental hijackers rather than purely novel entities.

## Methods

Review article synthesizing published experimental work (no original data). Key primary evidence cited includes:

- **In vivo optogenetics:** cortical neuron stimulation in glioma xenograft mouse models and optic pathway glioma models with visual deprivation.
- **Patient-derived glioma xenografts (PDX):** implanted into NLGN3 knockout vs. wild-type mouse brains; electrophysiology on hippocampal slices and cocultures.
- **Patch-clamp electrophysiology:** recordings from glioma cells in situ demonstrating fast (<5 ms) AMPAR-mediated postsynaptic currents spontaneously and evoked by neuronal stimulation [@Venkatesh2019].
- **Single-cell RNA-seq:** synaptic gene expression enrichment in OPC-like malignant cell subpopulations within patient glioblastoma biopsies.
- **Pharmacological/genetic perturbation:** AMPA receptor antagonists (NBQX, perampanel), ADAM10 inhibitors, gap junction blockers (meclofenamate), connexin-43-mediated gap junction analysis.
- **Peripheral nerve models:** surgical denervation, sympathectomy, parasympathectomy, adrenergic receptor blockade in prostate/stomach/pancreas mouse models.
- **Electron microscopy + immunolabeling:** ultrastructural confirmation of neuron-to-glioma synapses and pseudotripartite synapses in brain metastases.

## Key Findings

### Neuronal activity drives glioma growth (paracrine axis)

- Optogenetic stimulation of cortical neurons increases glioma proliferation in a circuit-specific manner; coculture with neurons induces ~10-fold glioma cell proliferation.
- Activity-regulated paracrine factors include **BDNF** and shed **NLGN3** (neuroligin-3).
- **NLGN3** is a postsynaptic adhesion molecule normally present at glutamatergic and GABAergic synapses. It is shed from synapses in a strictly activity-regulated manner by the sheddase **ADAM10**. Shed NLGN3 binds an unknown receptor on glioma cells, activating **FAK**, **SRC**, **RAS**, **PI3K-mTOR** pathways, and upregulating *NLGN3* itself and other synaptic genes in the malignant cell.
- NLGN3 is required for growth of all major high-grade glioma subtypes (IDH-wild-type GBM, IDH-mutant oligodendroglioma, `H3K27M`+ diffuse midline glioma) in mouse xenograft models; NLGN3 KO host brains fail to support glioma growth. NLGN3 expression inversely correlates with overall survival in adult GBM patients.
- **ADAM10** inhibition blocks glioma progression in PDX models and in the NF1-associated optic pathway glioma mouse model; an ADAM10 inhibitor is in early-phase clinical trials for pediatric high-grade glioma (NCT04295759).
- **NLGN3** also promotes neuroblastoma proliferation via PI3K/AKT signaling (Li 2019), extending the mechanism beyond glial cancers.

### Neuron-to-glioma synapses (electrochemical axis)

- ~5–10% of glioma cells within each tumor examined form bona fide **AMPA receptor (AMPAR)-mediated** postsynaptic synapses with neurons, confirmed by immunoEM and electrophysiology.
- Glioma cells, particularly the OPC-like subpopulation with highest synaptic gene enrichment, express under-edited **GluA2 (GRIA2)** AMPAR subunits — making the synapses calcium-permeable.
- Membrane depolarization alone (via optogenetic channelrhodopsin expression in glioma cells) is sufficient to increase glioma proliferation through voltage-sensitive downstream mechanisms.
- A second, slower (~>1 s) potassium-evoked current, proportional to local neural field potential, is also present in ~60% of malignant cells and propagates through **connexin-43**-mediated gap junctions between glioma cells.
- Gap junction blockade with **meclofenamate** disrupts synchrony of glioma calcium transients and reduces tumor growth in vivo.
- Glioma cells form long-distance microtube networks; **tweety-homolog-1 (TTYH1)** promotes microtube extension (also upregulated by neural activity-regulated factors).

### Neurotrophin signaling

- Gliomas express **BDNF**, **NGF**, **NT-3**, and receptors **p75**, **TrkB**, **TrkC**.
- **ProBDNF** (binds p75) inhibits adult GBM growth; **mature BDNF** (binds TrkB) increases GBM growth in vitro.
- TrkB on glioma stem cells receives BDNF from more differentiated neighbors, sustaining the stem cell population.
- TrkA expression correlates with favorable outcome in neuroblastoma; TrkC expression correlates with better outcome in medulloblastoma — in contrast to glial tumors.

### Axon pathfinding signals recapitulated in glioma

- **Ephrin-Eph** signaling: EphA2 promotes infiltrative GBM invasion (adult); EphB3 ligand drives invasion in `H3K27M`+ diffuse midline glioma.
- **Pleiotrophin** (secreted by SVZ stem cells): chemoattractant driving glioma spread to the subventricular zone niche; promotes glioma migration.
- **SEMA3A-neuropilin1** axis: promotes GBM cell invasion.
- **Slit-Robo** signaling: Slit2 expression inversely correlates with tumor grade; Robo1+ lines migrate away from Slit2; Slit2 overexpression reduces diffuse invasion in mouse models.

### Glioma-induced neuronal hyperexcitability (feedback loop)

- Gliomas promote neuronal hyperexcitability via: (a) non-synaptic glutamate secretion through **SLC7A11** (xCT, the x_c^- exchanger), (b) GABAergic interneuron loss, (c) impairment of neuronal **KCC2** cotransporter, rendering GABA excitatory in mature neurons.
- **PIK3CA** oncogene variants selectively regulate a synaptogenic astrocyte-like subpopulation (via glypican-3 secretion), differentially inducing neural hyperexcitability.
- High functional connectivity (fMRI) between glioblastoma and normal brain correlates robustly with poor survival.

### Brain metastases

- Breast/lung brain metastases exploit **connexin-43** gap junctions with astrocytes; carcinoma-astrocyte coupling transfers **cGAMP** → cGAS-STING → IFNα/TNF production → paracrine tumor support. Meclofenamate reduces breast/lung brain metastasis progression.
- Breast cancer brain metastases form **pseudotripartite synapses**, inserting metastatically into the perisynaptic position normally occupied by astrocytes, accessing glutamatergic transmission via **NMDA receptors (NMDARs)**. NMDA receptor antagonist dizocilpine (MK-801) suppresses brain-metastatic breast cancer growth via ERK.
- Breast cancer brain metastases upregulate **GABA receptors** and proliferate in response to exogenous GABA.

### Peripheral nervous system and solid organ tumors

- **Prostate cancer:** sympathetic adrenergic fibers (β2/β3 adrenergic receptors) drive initiation; parasympathetic cholinergic fibers drive spread. Adrenergic signaling also induces angiogenic state in tumor endothelial cells. Clinical trials targeting adrenergic blockade underway (e.g., NCT01847001, NCT03838029, NCT00502684).
- **Stomach/gastric cancer:** cholinergic innervation promotes tumor initiation; denervation markedly reduces gastric tumorigenesis in preclinical models.
- **Pancreatic cancer:** innervation precedes preneoplastic-to-cancer transition; sensory neuron ablation slows initiation (PDAC model); adrenergic β2 receptor promotes pancreatic cancer; cholinergic signaling suppresses pancreatic tumorigenesis (context-dependent). Aberrant innervation precedes transition from PanIN to PDAC.
- **Tumor-induced neurogenesis:** In prostate cancer, subventricular zone neuroblasts migrate out of the CNS via the bloodstream to initiate local neurogenesis in the tumor microenvironment (Mauffrey 2019) — a remarkable finding that the tumor can recruit CNS-derived neural progenitors peripherally.
- **NGF secretion by solid tumors** induces peripheral nerve branching into the TME (feed-forward amplification).
- Neurotransmitter signaling from tumor cells themselves: pancreatic neuroendocrine tumors secrete glutamate autocrinally via NMDAR/GKAP axis.

### Named genes and molecules (complete list from the paper)

**Synaptic/adhesion:** NLGN3 (neuroligin-3), NRXN (neurexin, implied), GluA2 (GRIA2), GRIA (AMPAR subunits), GRIN (NMDAR subunits), GJB2/GJB6 (connexin-26/43 implied via Cx43), CDH20 (protocadherin-7 in brain metastases), SLC7A11 (xCT).

**Sheddases/proteases:** ADAM10.

**Neurotrophins/receptors:** BDNF, NGF, NT-3, NT-4, NTRK1 (TrkA), NTRK2 (TrkB), NTRK3 (TrkC), NGFR (p75).

**Axon guidance:** EFNA/EPHA (Ephrin-A/EphA2), EFNB3/EPHB3 (EphB3), NRP1 (neuropilin-1), SEMA3A, SEMA3C, PLXN (plexins), ROBO1, SLIT2, PTN (pleiotrophin), TTYH1.

**Signaling effectors:** FAK (PTK2), SRC, RAS, PIK3CA, MTOR, MAPK/ERK.

**Ion channels/transporters:** KCNK (potassium channels implied), KCC2 (SLC12A5), SCN3A (Nav1.3), GRIN1/2 (NMDA), SLC12A2 (NKCC1).

**Oncogenes/drivers:** PIK3CA, NF1, `H3K27M` (`H3-3A`/HIST1H3B), IDH1/2.

**Gap junctions:** GJA1 (connexin-43), GJB2 (connexin-26), CDH20 (protocadherin-7).

**Other:** GLYPICAN-3 (GPC3; synaptogenic factor from PIK3CA astrocyte-like cells), THBS1 (thrombospondin-1; synaptogenic, correlates with high functional connectivity and poor survival in GBM), SLC7A11.

## Relevance

### `H1` — Tumors hijack top-down neural circuitry: **STRONGLY SUPPORTS**

This is the paper's central thesis. Neural activity directly and causally promotes tumor growth via synaptic integration (AMPAR synapses, potassium currents) and paracrine signaling (NLGN3, BDNF). The feed-forward loop (tumor induces hyperexcitability → more neural activity → more growth signals) is mechanistically established for gliomas. The peripheral nervous system section extends this to solid organ tumors via autonomic innervation. The paper provides strong mechanistic support for `H1` across CNS and peripheral contexts.

### `H2` — Via immune modulation: **PARTIAL/INDIRECT**

The brain metastasis section notes that connexin-43 gap junctions transfer cGAMP to astrocytes, activating cGAS-STING and inducing IFNα/TNF production — which then paradoxically supports tumor growth. This is a neural-adjacent (glial-immune) mechanism rather than direct neural-immune crosstalk. The paper does not substantially address neural regulation of anti-tumor immunity (NK cells, T cells), so `H2` is only weakly addressed. Neural signaling could modulate immune function indirectly via neurotransmitters (serotonin, catecholamines, acetylcholine), but this is not developed in this review.

### `H3` — Byproduct of aberrant developmental/oncofetal expression: **NEUTRAL / MECHANISTIC CONTEXT**

The paper provides extensive developmental context — gliomas arise from OPC-like progenitors, the spatiotemporal pattern of glioma incidence mirrors developmental myelination waves, and oncofetal programs are recapitulated. However, the paper frames this as a mechanistic explanation for *why* tumors respond to neural signals, not as evidence that neural gene expression in tumors is a byproduct without functional consequence. The developmental reactivation is treated as active (causally growth-promoting), not passive. `H3` is thus neither strongly supported nor refuted; it is reframed as a proximate cause of `H1`.

### `H4` — Artifact of brain/CNS cancer enrichment in cohort: **DIRECTLY RELEVANT — IMPORTANT CAVEAT**

The paper explicitly extends neural signaling beyond brain/CNS tumors to prostate, stomach, pancreas, breast, and skin. For peripheral solid tumors, the mechanism is peripheral nerve innervation rather than synaptic integration, but the growth-promoting logic is the same. This means that if the user's pipeline sees elevated neural gene mutations across a diverse cohort (including non-CNS cancers), `H4` (brain cancer enrichment artifact) is less likely to explain the full signal — neural signaling may genuinely be selected for across cancer types. However, the paper's depth of evidence is much greater for gliomas; peripheral tumor neural signaling is less mechanistically characterized.

### `H5` — Misannotation/non-neural function of "neural" genes: **PARTIALLY WEAKENS**

Many genes named in the paper (NLGN3, NRXN, GluA2/GRIA2, NMDAR subunits) are indeed canonical neural genes. The paper shows they have bona fide neural signaling functions in cancer cells — ruling out simple misannotation for these specific genes. However, the paper does not address genes like NKAIN2, KCNIP4, TAFA2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ, OPCML (the user's neural-gene mutation list). These are not mentioned. The large-gene-length confound (many neural genes have very long introns) is not discussed; the paper's approach is mechanistic, not mutation-frequency.

### Label-free neural gene identification: **LIMITED DIRECT UTILITY**

The paper does not offer a data-driven definition of "neural genes." It relies on canonical neuroscience knowledge. However, it points toward useful resources:
- Single-cell RNA-seq of patient glioblastoma samples reveals an OPC-like malignant subpopulation with highest synaptic gene enrichment — this sc-RNAseq signature is conceptually a label-free neural gene set derived from tumor expression data.
- The paper cites Filbin 2018 (Science) single-cell RNA-seq of `H3K27M` gliomas and Neftel 2019 (Cell) integrative glioblastoma cell state model, both of which contain expression-based neural/OPC gene signatures that could be extracted as reference gene lists without using human labels.
- For truly label-free definition, the embryonic neural expression atlases cited (developmental myelination, OPC biology) are more useful than this review itself.

## Project Framework Mapping

| Paper concept | Project term / pipeline element |
|---|---|
| NLGN3, GluA2, NMDAR — neural gene mutations | Gene rows in `gene_cancer_study.feather`; target of the user's neural-gene enrichment observation |
| Glioma OPC-like sc-RNAseq synaptic subpopulation | Potential source of a data-driven "neural gene" reference list (Neftel 2019, Filbin 2018) for gene annotation |
| Pan-cancer peripheral nerve involvement (prostate, pancreas, stomach, breast) | Cross-study aggregation rationale: neural gene mutations may be selected for outside CNS cancers |
| NLGN3 expression inversely correlates with GBM survival | Driver gene annotation layer (`bailey2018_driver`-equivalent; NLGN3 not in Bailey et al. [@Bailey2018] driver list) |
| SLC7A11 (xCT glutamate transporter) secreting glutamate | Functional gene linking mutation burden to microenvironment; testable against TMB annotation pipeline |
| PIK3CA variants → glypican-3 → hyperexcitability | PIK3CA is a canonical oncogene; its neural effects are a secondary phenotype linkable to mutation frequency |
| ADAM10 — clinical trial target | Potential drug-target overlap with mutation-annotated genes |
| Tumor-driven neurogenesis (SVZ neuroblasts → prostate TME) | [SPECULATION] Could create a selection pressure for neural gene expression in prostate cancer specifically |
| Meclofenamate (connexin-43 blocker) reduces GBM + brain mets | Connexin-43 (GJA1) mutation frequency could be tested in our cross-study matrix |
| `H3K27M` (HIST1H3B/`H3-3A`) glioma subtype | Covered in `cancer_type` stratification; diffuse midline glioma is a distinct cancer type |

## Limitations

1. **No mutation data.** The review is entirely about expression, electrophysiology, and protein signaling. It does not address somatic mutations in neural signaling genes, so it cannot directly explain the user's mutation-frequency enrichment observations.
2. **Glioma-centric.** The vast majority of mechanistic detail is for high-grade gliomas (adult GBM and pediatric `H3K27M`). Evidence for peripheral tumors is less mechanistically developed.
3. **No gene-length or confounding discussion.** The review does not address whether neural genes are enriched for mutations due to their large genomic footprint — which is the core confound in the user's pipeline.
4. **No label-free definition of "neural genes."** The paper uses expert-curated neuroscience categories, not expression-atlas-derived or data-driven gene sets. It cannot directly provide the reference gene list the user needs.
5. **NLGN3 knockout mice are constitutive knockouts** in some cited experiments — potential for developmental compensation confounds.
6. **Human NLGN3 ADAM10 clinical trial (NCT04295759)** was in early phase at time of publication; outcome data not available in this review.
7. **Genes from user's neural-gene mutation list absent.** NKAIN2, KCNIP4, TAFA2/FAM19A2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ, OPCML are not discussed. The review focuses on synaptic/signaling genes rather than structural/adhesion/ion-channel genes.

## Model / Tool Availability

- No computational tools or datasets are released with this review.
- Primary experimental data are in the cited primary papers reviewed by Keough and Monje, including glioma synapse, optic-pathway glioma, prostate innervation, pancreatic innervation, and gastric-cancer neural signaling studies.
- **Potentially reusable datasets for a label-free neural gene definition:**
  - Neftel 2019 (Cell) — GBM single-cell atlas with OPC/NPC/AC/MES state gene signatures (publicly available).
  - Filbin 2018 (Science) — `H3K27M` diffuse midline glioma single-cell RNA-seq (GEO).
  - The Human Protein Atlas (neural enrichment scores) — not cited but conceptually consistent with the paper's developmental framing.
  - GTEx brain expression data — not cited; relevant for defining genes with high neural-tissue specificity without label dependency.

## Follow-up

1. **Check whether the user's neural-gene list (NKAIN2, KCNIP4, TAFA2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ, OPCML) contains known long-intron genes** — gene body length in kb is the primary null hypothesis for mutation enrichment. Extract gene lengths from Ensembl and compute correlation with rank in the user's neural-gene list.
2. **Extract OPC-like synaptic gene signatures from Neftel 2019 / Filbin 2018** and use them as a data-driven "neural gene" reference list — compare overlap with the user's top-mutated neural genes to assess whether the mutation enrichment is specifically in cancer-relevant neural signaling genes (`H1`) vs. generic neural-expressed genes (`H4`/`H5`).
3. **Test NLGN3 mutation frequency** in the cross-study aggregation pipeline — NLGN3 is mechanistically established as a glioma growth factor; if it is recurrently mutated (gain-of-function) across studies this would be strong `H1` support.
4. **Test ADAM10 mutation frequency** across cancer types — if ADAM10 loss-of-function mutations co-occur with NLGN3 expression changes, this could suggest a mutation-expression interaction.
5. **Stratify the top-mutated neural gene list by cancer type** in the pipeline — if the enrichment is driven by glioma/CNS cancer studies, `H4` (cohort artifact) is the dominant explanation. If the enrichment persists after removing CNS cancers, `H1`/`H3` are more plausible.
6. **Check SLC7A11 (xCT)** in the cross-study mutation table — it is mechanistically implicated in glioma-driven glutamate secretion and neural hyperexcitability; recurrent amplification/upregulation (rather than loss-of-function mutation) would be the expected signal.
7. **Literature bridge to Venkatesh et al. [@Venkatesh2019]** — if a paper summary for Venkatesh2019 is in the batch, that paper provides the primary experimental data underlying the synaptic integration mechanism reviewed here.
