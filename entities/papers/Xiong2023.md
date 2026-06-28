---
type: paper
title: A brain-tumor neural circuit controls breast cancer progression in mice
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: paper:Xiong2023
ontology_terms:
- brain-tumor neural circuit
- breast cancer
- autonomic nervous system
- sympathetic innervation
- central amygdala
- corticotropin-releasing hormone
- norepinephrine
- cancer-induced anxiety
- antitumor immunity
datasets: []
source_refs:
- cite:Xiong2023
related: []
---

# A brain-tumor neural circuit controls breast cancer progression in mice

- **Authors:** Si-Yi Xiong, Hui-Zhong Wen, Li-Meng Dai, Yun-Xiao Lou, Zhao-Qun Wang, Yi-Lun Yi, Xiao-Jing Yan, Ya-Ran Wu, Wei Sun, Peng-Hui Chen, Si-Zhe Yang, Xiao-Wei Qi, Yi Zhang, Guang-Yan Wu (corresponding)
- **Year:** 2023
- **Journal:** Journal of Clinical Investigation
- **DOI/URL:** https://doi.org/10.1172/JCI167725
- **BibTeX key:** Xiong2023
- **Source:** PDF

## Key Contribution

This study establishes a causal, polysynaptic neural circuit running from the central medial amygdala (CeM) through the lateral paragigantocellular nucleus (LPGi) of the brainstem to sympathetic nerves newly formed within breast tumors. Using a combination of retrograde transsynaptic viral tracing, chemogenetics (DREADDs), optogenetics, and fiber photometry in two mouse breast cancer models, the authors demonstrate that cancer-induced anxiety activates CeM corticotropin-releasing hormone (CRH) neurons, which in turn drive intratumoral sympathetic nerve activity, elevate local norepinephrine (NE), suppress antitumor immunity, and accelerate tumor growth. Pharmacological suppression of this circuit with alprazolam (a benzodiazepine antianxiety drug) significantly slows tumor progression. This is the first study to trace a complete brain-to-peripheral-nerve-to-tumor circuit as a causal driver of breast cancer progression, and to show therapeutic benefit of targeting the anxiety arm of that circuit.

## Methods

**Mouse models.** Two complementary breast cancer models were used:
- Orthotopic transplanted model: 4T1-luc luciferase-expressing breast cancer cells injected into the mammary gland of female BALB/c mice (primary readout model, n = 12–17 per group in most experiments).
- Spontaneous model: MMTV-PyMT transgenic mice developing mammary tumors starting at approximately 10 weeks of age (used to validate key findings in a non-transplanted setting).

**Anxiety behavioral readouts.** Light-dark transition test (LDT), open field test (OFT), and elevated plus maze (EPM) were used to quantify anxiety-like behaviors. Anxiety index was computed as a composite score. Two-sided linear regression confirmed that anxiety severity correlated with tumor volume, weight, and bioluminescence intensity (all P < 0.001, R² ≥ 0.65) [@Xiong2023].

**Circuit mapping — retrograde transsynaptic tracing.** Pseudorabies virus expressing EGFP (PRV-CAG-EGFP) was injected into the 4T1 tumor stroma 6 days before perfusion. PRV traced retrogradely from tumor → spinal cord → brainstem → hypothalamus → forebrain, with prominent labeling of the CeM and the LPGi. Immunofluorescence confirmed that the majority of PRV-infected CeM neurons co-expressed CRH, and most PRV-infected LPGi neurons co-expressed tyrosine hydroxylase (TH), a catecholamine marker. A cell-type-specific retrograde transmonosynaptic tracing system (rAAV2/8-Dbh-Cre + Cre-dependent AAV-helper viruses into LPGi, followed by RV-EnvA-ΔG-EGFP at the same site) confirmed that CeM CRH neurons send monosynaptic projections to LPGi catecholaminergic (LPGi^CA) neurons.

**CeM^CRH neuron manipulation — ablation.** Bilateral injection of rAAV2/2-CRH-Cre + rAAV2/9-EF1α-Flex-taCasp3-TEVp into CeM ablated CRH neurons (confirmed by reduced CRH immunostaining). Ablation significantly reduced anxiety behaviors, slowed tumor growth, decreased tumor weight and luciferase intensity, and lowered intratumoral NE content versus EYFP controls.

**CeM^CRH neuron manipulation — chemogenetics (DREADDs).** Inhibitory DREADD (hM4Di via rAAV2/9-EF1α-DIO-hM4Di-mCherry + rAAV2/2-CRH-Cre) with CNO delivery in food suppressed CeM^CRH activity, reduced anxiety, and slowed tumor growth. Stimulatory DREADD (hM3Dq, same Cre strategy) had the opposite effects — increasing anxiety and accelerating tumor growth. Both were validated by NE measurement, bioluminescence, Ki67 (proliferation), and TUNEL (apoptosis) immunostaining in tumor tissue.

**CeM^CRH neuron manipulation — optogenetics.** ChR2-mCherry (excitatory, rAAV2/9-EF1α-DIO-ChR2-mCherry) or eNpHR3.0 (inhibitory) were expressed in CeM^CRH neurons with implanted optical fibers. Optogenetic activation of CeM^CRH neurons increased sympathetic GRAB_NE2h fluorescence (a genetically encoded NE biosensor) in tumor stroma; optogenetic inhibition decreased it.

**CeM^CRH→LPGi circuit manipulation.** Retrograde rAAV2/retro-CRH-Cre was injected into LPGi to restrict Cre expression to LPGi-projecting CeM^CRH neurons; Cre-dependent hM4Di or hM3Dq was expressed in CeM. This circuit-level chemogenetic manipulation reproduced the tumor growth and anxiety effects seen with global CeM^CRH manipulation.

**Sympathetic nerve activity readout.** A GPCR activation-based NE sensor (GRAB_NE2h) expressed in 4T1 tumor stroma via intratumoral lentiviral injection, with fiber photometric recording during optogenetic CeM stimulation, was used to measure real-time NE release. Tissue NE concentration was also measured by ELISA as a static readout.

**Immune profiling.** Flow cytometry on tumors and spleens quantified CD45⁺ leukocytes, CD4⁺ and CD8⁺ T cells, Tregs (CD4⁺CD25⁺FOXP3⁺), CD4⁺PD-1⁺ and CD8⁺PD-1⁺ T cells, CD4⁺IFN-γ⁺ and CD8⁺IFN-γ⁺ T cells, and M1/M2 macrophages (CD11b⁺F4/80⁺CD86⁺CD206⁻ M1 vs. CD11b⁺F4/80⁺CD86⁻CD206⁺ M2) across ablation, chemogenetic, and alprazolam treatment experiments.

**Alprazolam pharmacological intervention.** 4T1-tumor-bearing BALB/c and MMTV-PyMT mice received twice-daily intraperitoneal alprazolam or vehicle for 4 weeks. Alprazolam significantly reduced c-Fos expression in CeM^CRH and LPGi^CA neurons, decreased anxiety behaviors, slowed tumor growth, and shifted the tumor immune microenvironment toward a more immunostimulatory profile.

**Statistics.** Two-tailed unpaired Student's t-test, 1-way ANOVA with Tukey post-hoc, and 2-way repeated-measures ANOVA; linear regression for correlations. P < 0.05 considered significant [@Xiong2023].

## Key Findings

1. **Breast tumor-bearing mice develop cancer-induced anxiety that correlates with tumor burden.** 4T1-luc tumor-bearing BALB/c mice showed significant anxiety-like behaviors across LDT, OFT, and EPM compared with vehicle controls at 28 days post-inoculation. Anxiety severity was tightly and linearly correlated with tumor volume, weight, and luciferase intensity (all R² ≥ 0.65, P < 0.001).

2. **Tumors recruit new sympathetic nerve fibers early in cancer development.** Immunofluorescence for neurofilament-L (NF-L) and tyrosine hydroxylase (TH) revealed that 4T1 mammary tumors displayed denser sympathetic innervation at days 5, 7, and 9 post-inoculation. PRV retrograde tracing showed these newly formed peripheral sympathetic nerves were polysynaptically connected to the brain, reaching the CeM via spinal cord, brainstem, and LPGi.

3. **The CeM→LPGi neural circuit is the identified brain node.** The specific circuit identified is: CeM CRH neurons → LPGi catecholaminergic (TH⁺) neurons → sympathetic preganglionic neurons → intratumoral sympathetic nerve fibers → NE release in tumor stroma. PRV tracing, monosynaptic retrograde tracing, fiber photometry, and IHC co-localization all converge on this polysynaptic chain. The CeM is the central hub; CRH is its marker neurotransmitter/neuropeptide.

4. **CeM^CRH neurons are activated in tumor-bearing mice.** Double immunofluorescence for c-Fos (immediate-early activity marker) and CRH showed significantly higher c-Fos⁺CRH⁺ cell percentage in 4T1 tumor-bearing mice versus controls in CeM.

5. **Optogenetic activation of CeM^CRH neurons directly drives NE release in tumor stroma.** GRAB_NE2h fiber photometry recorded a robust fluorescence increase in 4T1 tumor tissue during optogenetic stimulation of CeM^CRH neurons; EGFP control mice showed no change.

6. **Ablation or inhibition of CeM^CRH neurons or the CeM^CRH→LPGi circuit reduces anxiety, NE, and tumor growth.** Viral ablation (taCasp3), chemogenetic inhibition (hM4Di/CNO), optogenetic inhibition (eNpHR3.0), and circuit-specific inhibition via LPGi-targeted retrograde Cre + CeM hM4Di all significantly decreased tumor volume, tumor weight, luciferase intensity, intratumoral NE content, Ki67⁺ proliferating cells, and TUNEL⁺ apoptosis (in opposite direction from controls), while increasing effector T cell populations and M1 macrophage ratios.

7. **Activation of CeM^CRH neurons or the circuit accelerates tumor growth.** Chemogenetic (hM3Dq/CNO) and optogenetic (ChR2) activation produced significantly larger, heavier, more bioluminescent tumors with higher intratumoral NE, more Tregs, more exhausted T cells (PD-1⁺), and a lower M1/M2 macrophage ratio.

8. **The immune mechanism is NE-mediated suppression of antitumor immunity.** Sympathetic NE acts on adrenergic receptors (α- and β-AR) on immune cells and tumor stroma. Activation of the circuit suppressed CD4⁺ and CD8⁺ T cells and IFN-γ⁺ effectors, increased Tregs and exhausted T cell subsets, and decreased M1/M2 ratio. Reversal was seen upon circuit inhibition. The 4T1 cells themselves do not express functional adrenergic receptors, supporting an immune-mediated rather than a direct cancer-cell-intrinsic NE effect in this model.

9. **Alprazolam (benzodiazepine antianxiety drug) slows breast tumor progression.** Daily alprazolam treatment suppressed CeM^CRH and LPGi^CA neuron c-Fos expression, reduced anxiety, significantly slowed tumor growth, decreased tumor weight and bioluminescence, lowered intratumoral NE, and shifted the TME toward a more immunostimulatory state in both 4T1 and MMTV-PyMT models.

10. **Key named genes/markers:** CRH (corticotropin-releasing hormone, marker of the central amygdala output neurons); TH (tyrosine hydroxylase, sympathetic neuron marker); NF-L (neurofilament-L, pan-neuronal marker); GRAB_NE2h (genetically encoded NE biosensor); c-Fos (neural activity marker); Ki67 (proliferation); TUNEL (apoptosis); CD45, CD4, CD8, FOXP3, PD-1, IFN-γ (immune markers); CD11b, F4/80, CD86, CD206 (macrophage polarization markers).

## Relevance

**`H1` (tumors hijack top-down neural circuitry) — direct, strong support.** This paper is the most direct available causal demonstration of the `H1` local note label: it shows that the brain (specifically a well-defined limbic-brainstem circuit) drives tumor innervation and progression via the autonomic nervous system, not passively, but through a feedforward loop initiated by the tumor itself (cancer-induced anxiety activates CeM, which amplifies sympathetic output back to the tumor). This is precisely the kind of top-down circuit engagement `H1` predicts.

**`H2` (via immune modulation) — supported as the proximate mechanism.** The data show that CeM→LPGi→sympathetic→NE circuit suppresses antitumor immunity (CD8⁺ T cells, IFN-γ effectors, M1 macrophages) and expands immunosuppressive populations (Tregs, exhausted T cells). `H2` is not an alternative to `H1` here — it is the mechanistic pathway through which `H1` operates.

**`H3` (aberrant oncofetal/developmental expression) — not addressed.** The study does not examine gene expression programs in tumor cells and says nothing about oncofetal or developmental transcriptional states.

**`H4` (brain/CNS cancer cohort artifact) — important indirect bearing.** The paper demonstrates a *systemic* brain→periphery circuit in a *non-CNS* cancer (breast). Neural circuit engagement is not confined to brain tumors. This is directly relevant to interpreting the "top mutated genes dominated by neural genes" pattern in our cBioPortal cohort: it means that neural pathway activity (and potentially expression of neural genes) could be a general feature of many solid tumors, not merely a confound of having CNS cancer studies in the cohort.

**`H5` (misannotation) — not addressed.** The study does not involve mutation frequency analysis or gene annotation.

**Critical distinction for our pipeline's question:** This paper establishes that neural involvement in breast cancer is *systemic circuit-level*, not cell-intrinsic somatic mutation of neural genes within tumor cells. The study examines the peripheral nervous system of the host, not the mutational landscape of the tumor genome. Therefore:
- It does NOT predict that neural genes (NKAIN2, KCNIP4, RBFOX1, LSAMP, etc.) should appear at elevated SOMATIC MUTATION frequency in breast tumors.
- It does, however, provide a coherent biological rationale for why neural gene EXPRESSION could be elevated in tumor stroma (newly formed sympathetic nerve fibers), which could influence which genes appear mutated if annotation or expression-based filtering is applied.
- The circuit finding strengthens the motivation to distinguish "neural gene expression in tumor microenvironment (stromal)" from "neural gene somatic mutation in tumor cells" when interpreting high mutation frequencies.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| Breast cancer mouse models (4T1, MMTV-PyMT) | Not directly represented (pipeline uses human cBioPortal data) | Mouse-to-human translation gap is substantial |
| Brain→sympathetic→NE→immune circuit | Not a pipeline variable; orthogonal to mutation frequency | Circuit acts at the level of tumor microenvironment, not somatic genome |
| CeM CRH neurons as anxiety hub | Background motivation for `H1` hypothesis | Provides mechanistic grounding for why neural genes matter in cancer biology |
| Intratumoral NE content (ELISA) | Not a cBioPortal clinical variable | NE levels are not available in mutation data; no mapping possible |
| Immune cell composition (flow cytometry) | Not currently extracted; some cBioPortal studies have immune deconvolution data | Could be a future integration if TIMER2 or CIBERSORT scores are fetched |
| Alprazolam → circuit suppression → slowed tumor growth | Not a pipeline variable | Suggests antianxiety medications could be a clinical covariate worth examining |
| TH⁺ sympathetic innervation density | Not in mutation tables; would require spatial/IHC data | Informative for understanding why neural gene expression (not mutation) elevates in TME |
| `H1`: top-down neural circuitry | Hypothesis `H1` in project framework | Strong mechanistic support for `H1` in a non-CNS cancer |

## Limitations

- All experiments are in mice (BALB/c orthotopic 4T1 and MMTV-PyMT). Direct translation to human breast cancer is unproven; the specific polysynaptic circuit (CeM→LPGi→sympathetic→tumor) has not been mapped in humans.
- The 4T1 model is immunocompetent but does not express functional adrenergic receptors on the cancer cells themselves; the immune-mediated NE effect may not generalize to all breast cancer subtypes (e.g., AR-expressing subtypes where direct cell-autonomous NE signaling has been described).
- The study characterizes circuit-level function but does not identify the downstream molecular mechanisms by which sympathetic NE remodels the immune microenvironment (e.g., which specific adrenergic receptor subtypes on which immune cell populations mediate T cell suppression vs Treg expansion).
- CeM is one node in a larger anxiety-processing network; the study does not rule out parallel pathways (e.g., via the hypothalamic-pituitary-adrenal axis, glucocorticoid release, or other limbic structures) contributing independently to sympathetically driven tumor progression.
- Anxiety was measured behaviorally; the study does not demonstrate that inter-individual variation in human anxiety levels (e.g., as assessed by clinical anxiety scores in cBioPortal clinical data) predicts tumor innervation or NE levels.
- The temporal window studied (4 weeks post-injection) may not fully represent the chronic, years-long progression of human breast cancer.
- Alprazolam has off-target effects beyond CeM/LPGi suppression; circuit specificity of the therapeutic benefit is supported by the DREADD/optogenetics data but the drug is not a clean tool compound.

## Model / Tool Availability

No new computational tool or dataset is released. Experimental tools used:
- Pseudorabies virus (PRV-CAG-EGFP) for retrograde transsynaptic tracing (standard neuroscience reagent).
- rAAV2/2-CRH-Cre for CRH neuron-specific Cre expression.
- rAAV2/9-EF1α-Flex-taCasp3-TEVp for Cre-dependent neuronal ablation.
- hM4Di and hM3Dq DREADDs (standard chemogenetic reagents).
- ChR2-mCherry and eNpHR3.0 for optogenetics.
- GRAB_NE2h genetically encoded NE biosensor (key tool for real-time NE recording in vivo; developed by the Yulong Li lab, Peking University).
- Fiber photometry system for in vivo fluorescence recording.

Raw data available in the JCI Supplemental Supporting Data Values file or from the corresponding author.

## Follow-up

- **For our mutation meta-analysis:** This paper does not justify expecting elevated somatic mutation frequencies in neural genes due to the CeM→tumor circuit. The mechanism is at the level of autonomic innervation and host immune remodeling, not tumor cell mutation. Our primary alternative explanations for the neural gene pattern remain `H4` (CNS cancer cohort composition) and gene-length confounding.
- **Testing `H1` with our data:** A tractable proxy for "neural circuit engagement" in cBioPortal studies is intratumoral sympathetic innervation, which is not directly measurable from mutation tables. However, if expression data is available (via `export_study_expression.py`), checking whether TH (gene: TH), NF-L (gene: NEFL), or CRH (gene: CRH) expression is elevated in breast cancer vs other solid tumors would provide a data-driven test of whether the neural microenvironment signature is detectable at the expression level.
- **Defining neural genes from data (`H4` test):** The paper's use of TH and NF-L as sympathetic nerve markers is relevant: TH and NEFL are expression-based neural identifiers that could anchor a data-driven neural gene set (not human/AI labels). Combined with expression datasets from the Human Protein Atlas or GTEx (brain enrichment), these markers could define a reference neural gene list for testing whether our top-mutated genes are enriched for neural expression patterns.
- **Clinical covariate:** Antianxiety medication use (including benzodiazepines such as alprazolam) is a candidate clinical covariate in cBioPortal studies. If available, testing whether patients on antianxiety medication show different mutation frequencies in neural genes or different tumor immune profiles would be a human-level analog of the alprazolam experiment here.
- **Relevant genes for expression-based neural label definition:** TH (tyrosine hydroxylase), NEFL/NF-L (neurofilament light), CRH (corticotropin-releasing hormone), ADRB1/ADRB2/ADRA2A (adrenergic receptors as tumor/immune readouts), PTPRC (CD45), FOXP3 (Tregs), IFNG (IFN-γ effectors).
