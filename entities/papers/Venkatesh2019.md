---
type: paper
title: The neural regulation of cancer
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: paper:Venkatesh2019
ontology_terms:
- neuroscience-oncology
- glioma
- tumor microenvironment
- neural plasticity
- synaptic signaling
- neuroligin-3
- cancer neuroscience
datasets: []
source_refs:
- cite:Venkatesh2019
related:
- paper:Mancusi2023
- paper:Magnon2023
- paper:Xiong2023
---

# The neural regulation of cancer

- **Authors:** Humsa S. Venkatesh
- **Year:** 2019
- **Journal:** Science, 366(6468): 965 (Grand Prize Essay, Molecular Medicine category, Science & SciLifeLab Prize for Young Scientists)
- **DOI/URL:** https://doi.org/10.1126/science.aaz7776
- **BibTeX key:** Venkatesh2019
- **Source:** PDF (local copy)

## Key Contribution

A prize essay summarizing the author's doctoral and postdoctoral research (Monje laboratory, Stanford) establishing that neuronal activity is a functional driver of glioma progression — not merely a passive microenvironmental bystander. The essay synthesizes three linked lines of work: (1) optogenetic demonstration that neuronal activity promotes circuit-specific glioma growth; (2) identification of soluble neuroligin-3 (NLGN3) shed by the ADAM10 sheddase as the principal activity-dependent mitogen, with loss of NLGN3 abolishing glioma growth in mouse models; and (3) evidence that glioma cells form functional AMPA receptor-dependent synapses with neurons and propagate depolarization across the tumor mass via gap junctions. The essay also notes that neural regulation of tumor growth has since been extended beyond glioma to prostate, pancreatic, skin, and gastric cancers, framing neural-circuit hijacking as a broadly applicable cancer-progression mechanism.

## Methods

This is a prize essay (narrative synthesis of the author's own published experimental work), not a primary methods paper. The underlying experimental platforms described include:

- **Optogenetic-transplantation mouse model:** patient-derived glioma cells transplanted into mice in which specific neuronal circuits can be activated or silenced via optogenetics; enables causal manipulation of the neuronal component of the tumor microenvironment.
- **Acute optogenetic slice culture + proteomics:** acute brain slice cultures with optogenetic stimulation, combined with biochemical and proteomic assays, to identify activity-dependent secreted proteins from neurons.
- **Genetic mouse models + protease inhibitor analysis:** used to identify ADAM10 as the sheddase responsible for cleavage and secretion of NLGN3 from neurons, oligodendrocyte precursor cells (OPCs), and glioma cells themselves.
- **Single-cell transcriptomics + immuno-electron microscopy:** to identify synaptic structures between neurons and malignant glioma cells.
- **Whole-cell patch clamp of xenografted glioma cells:** simultaneous with afferent neuron stimulation, to detect AMPA receptor-dependent postsynaptic currents in glioma cells.
- **Two-photon calcium imaging:** real-time imaging of depolarization propagation through gap-junction-connected tumor cell networks in response to neuronal stimulation.
- **In vivo glioma depolarization:** optogenetic depolarization of xenografted glioma cells, with pharmacological and genetic block of electrochemical signaling as controls.

Primary results cited are from Venkatesh et al. Cell 161:803 (2015), Nature 549:533 (2017), and Nature 573:539 (2019).

## Key Findings

- **Neuronal activity drives circuit-specific glioma growth:** Optogenetic stimulation of neuronal circuits containing transplanted patient-derived glioma cells robustly promoted glioma growth and progression — the first causal demonstration of neurons as tumor microenvironmental drivers in brain cancer.
- **NLGN3 is the key activity-dependent mitogen:** Proteomics of activity-conditioned media identified soluble NLGN3 (a cleaved ectodomain of the synaptic adhesion molecule neuroligin-3) as the most robustly differentially secreted protein. Soluble NLGN3 promotes glioma proliferation via PI3K pathway activation and induces upregulation of synapse-related genes in glioma cells.
- **NLGN3 is essential for glioma growth:** Higher NLGN3 expression predicts significantly worse prognosis in adult glioma patients. In mice genetically deficient for NLGN3, patient-derived pediatric and adult gliomas fail to grow — underscoring NLGN3 as a non-redundant dependency in the tumor neuromicroenvironment.
- **ADAM10 is the sheddase; its inhibition blocks tumor growth:** ADAM10 cleaves and secretes NLGN3 from neurons, OPCs, and glioma cells. ADAM10 inhibitor treatment in tumor-bearing mice phenocopies NLGN3 genetic loss (glioma growth stagnation), providing the rationale for clinical trials of ADAM10 inhibition in pediatric and adult high-grade glioma.
- **Gliomas form functional synapses with neurons:** Single-cell transcriptomics and immuno-electron microscopy revealed synaptic structures between neurons and malignant cells. Patch-clamp recordings confirmed AMPA receptor-dependent postsynaptic currents in xenografted glioma cells, and two-photon calcium imaging showed that synaptic depolarization propagates rapidly through gap-junction-coupled tumor cell networks.
- **Glioma depolarization promotes proliferation:** In vivo optogenetic depolarization of glioma cells promoted proliferation; pharmacological or genetic block of electrochemical signaling inhibited xenograft growth and extended mouse survival.
- **Extension to other cancer types:** Neural regulation of tumor growth has been reported in prostate (Magnon et al. Science 2013), pancreatic (Renz et al. Cancer Cell 2018), skin (Peterson et al. Cell Stem Cell 2015), and gastric cancers (Zhao et al. Sci Transl Med 2014; Hayakawa et al. Cancer Cell 2017), establishing this as a pan-cancer mechanism.

## Relevance

### Connection to H1–H5 (project hypotheses about neural gene enrichment)

The project's observed enrichment of neural genes (NKAIN2, KCNIP4, TAFA2/FAM19A2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ, OPCML) at the top of cross-cancer somatic mutation frequency rankings prompted five competing explanations:

- **H1 (cancers hijack top-down neural circuitry):** This essay is the canonical primary literature for H1. It provides experimental proof-of-concept that gliomas exploit neuronal-activity signaling (NLGN3/ADAM10/PI3K, neuron-to-glioma synapses, gap-junction depolarization) to drive proliferation. It therefore strongly motivates H1 as a biologically real mechanism. However, the essay is focused exclusively on glioma (and briefly mentions prostate, pancreatic, skin, gastric cancers as extensions) — the identified driver is NLGN3, not the large-gene synaptic scaffold proteins (NKAIN2, KCNIP4, etc.) that dominate this project's mutation lists.
- **H2 (via immune modulation):** Not addressed.
- **H3 (aberrant developmental / oncofetal expression):** Indirectly relevant — the essay frames cancer neural hijacking as recapitulating mechanisms of normal neurodevelopment (NPC activity-regulation), and NLGN3 is described as upregulating synapse-related gene programs in glioma. This aligns with H3 conceptually, but the essay does not frame it as oncofetal re-expression.
- **H4 (brain/CNS-cancer artifact):** The essay's focus on glioma makes H4 a live concern for this project: if the neural gene enrichment in cross-cancer mutation tables is driven by CNS tumor studies, the Venkatesh mechanism is the correct biology but the wrong cancer type. The essay does not address whether neural gene mutations confer selective advantage in non-CNS cancers. **This paper does not resolve H4; it amplifies the need to control for it.**
- **H5 (misannotation):** Not addressed.

**Net assessment:** This paper strongly supports H1 as biologically feasible for glioma, but does not provide a data-driven definition of "neural genes" from somatic mutation data, does not address confounding by gene length or CNS study prevalence, and does not directly explain why NKAIN2, KCNIP4, and similar large-footprint synaptic scaffold genes would be selected for somatic mutation in pan-cancer cohorts. The NLGN3/ADAM10 axis it identifies is paracrine signaling, not a cell-autonomous somatic driver in the conventional oncogenomics sense.

### Connection to this project's pipeline

- This paper provides biological context for interpreting neural gene hits in cross-cancer somatic mutation frequency tables, specifically the hypothesis that such genes could be functionally relevant rather than purely length-confounded noise.
- The essay's mention of PI3K pathway activation downstream of NLGN3 is notable: PI3K pathway genes (PIK3CA, PTEN, etc.) are established pan-cancer drivers; if NLGN3 activates PI3K, neural-to-PI3K crosstalk could be a cell-non-autonomous layer atop canonical driver pathways.
- No pipeline-ready data or computational resources are provided.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Neuronal activity → NLGN3 secretion → glioma PI3K activation | H1: neural hijacking mechanism | Experimentally validated in glioma; not tested in pan-cancer somatic mutation context |
| NLGN3 as essential glioma dependency (KO = no tumor) | Functional selection for neural gene retention | Argues against pure length confound for NLGN3; does not address other genes in project's top list |
| ADAM10 sheddase as therapeutic target | Not directly in pipeline scope | Potential therapeutic relevance |
| Neuron-glioma synapse (AMPA receptors, gap junctions) | H1, H4 | Biologically real for glioma; H4 risk: pipeline's neural-gene enrichment may be CNS-study-driven |
| Extension to prostate / pancreatic / skin / gastric cancer | Pan-cancer neural hijacking (H1 generalization) | Claims are secondary citations; experimental depth varies across cancer types |
| Normal neurodevelopment recapitulation | H3 (oncofetal expression) | Framing overlap; essay does not operationalize H3 |

## Limitations

- Prize essay format (~2 pages): no new data, no methods section, no supplementary material; all claims cite published primary papers (Venkatesh et al. 2015, 2017, 2019).
- Focused almost exclusively on glioma; extension to other cancer types is asserted (one paragraph, citing others' work) but not deeply analyzed.
- Does not address gene-length confounding or explain why somatic mutations in neural genes (as opposed to their expression or cleavage) would be positively selected in pan-cancer cohorts.
- Does not provide a transcriptomic, genomic, or proteomic definition of "neural" gene sets — genes are identified through proximity to synaptic biology, not from data-driven criteria. This is the most important gap relative to this project's goal of defining neural genes purely from somatic mutation data.
- The NLGN3-dependency result (glioma fails to grow in NLGN3-null mice) is a host-tissue result, not a tumor cell-autonomous somatic mutation result — distinct from the question of whether somatic mutations IN neural genes are positively selected.
- Clinical trial rationale (ADAM10 inhibitor) is stated; trial outcomes are not reported in this essay (2019 publication; results, if any, would be subsequent).

## Model / Tool Availability

None. This is a narrative prize essay; no software, datasets, or atlases are released. The primary experimental papers (Venkatesh et al. Cell 2015, Nature 2017, Nature 2019) would contain the data and any associated resources.

## Follow-up

- Read Venkatesh et al. Nature 573:539 (2019) — the primary paper on neuron-to-glioma synapses; contains the single-cell transcriptomics, patch-clamp, and calcium imaging data summarized here. This is the most recent primary paper and likely the most methodologically relevant.
- Read Venkatesh et al. Nature 549:533 (2017) — the primary NLGN3/ADAM10 paper with the genetic knockouts; key for the therapeutic target claim.
- Check the status of ADAM10 inhibitor clinical trials in high-grade glioma (pediatric and adult) that this essay said were upcoming as of 2019.
- For project relevance: check whether NLGN3 or ADAM10 appear in the project's observed top-mutated neural gene list — they are not in the current list (NKAIN2, KCNIP4, TAFA2/FAM19A2, RIT2, CALN1, RBFOX1, LSAMP, SGCZ, OPCML), which suggests the project's signal may originate from a different class of neural gene (large synaptic scaffold proteins vs. the signaling ligand/receptor axis studied here).
- For H4 resolution: stratify the project's cross-cancer neural-gene mutation frequency analysis by whether CNS/glioma studies are included or excluded. If the enrichment disappears without CNS studies, H4 (brain-cancer artifact) is the leading explanation and this paper's biology is the correct context but the wrong scope.
- For H1 generalization: read Magnon et al. Science 2013 (prostate/adrenergic nerves) and Renz et al. Cancer Cell 2018 (pancreatic/cholinergic nerves) to assess whether the neural-dependency mechanism generalizes beyond glioma in ways relevant to the project's pan-cancer mutation analysis.
- Consider whether the neuron-to-glioma synapse model predicts any specific somatic mutation patterns: if glioma cells must express functional AMPA receptors and gap junctions, are mutations in these components under negative selection (loss-of-function mutations depleted) in glioma sequencing data? This would be testable in the project's pipeline.
