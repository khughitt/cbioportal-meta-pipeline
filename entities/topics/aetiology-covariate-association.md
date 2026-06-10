---
type: topic
title: Agnostic covariate to mutational-signature-exposure association (signature
  aetiology inference)
status: active
created: '2026-05-31'
updated: '2026-05-31'
id: topic:aetiology-covariate-association
ontology_terms:
- mutational signatures
- signature aetiology
- covariate association
- NMF
- Bayesian inference
- SBS4 tobacco
- SBS7 UV
- SBS2/13 APOBEC
- MMR/MSI
- DNA repair deficiency
datasets: []
source_refs:
- paper:Adler2023
- paper:Afsari2021
- paper:Drummond2023
- paper:Ji2023
- paper:Kim2016
- paper:Park2023
- paper:Robinson2019
- paper:Rosales2017
- paper:Sorensen2023
- paper:ValiPour2022
- paper:Zito2025
related:
- paper:Adler2023
- paper:Afsari2021
- paper:Drummond2023
- paper:Ji2023
- paper:Kim2016
- paper:Park2023
- paper:Robinson2019
- paper:Rosales2017
- paper:Sorensen2023
- paper:ValiPour2022
- paper:Zito2025
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- method:h08-agnostic-association-model
---

# Agnostic covariate to mutational-signature-exposure association (signature aetiology inference)

## Summary

The question of *why* a tumour carries a given mutational signature — what upstream biological or
environmental cause drove that exposure — has generated a distinct computational literature.
Approaches range from supervised classifiers that learn signatures from annotated exposures
(paper:Afsari2021) to fully joint generative models that simultaneously infer signatures and their
covariate dependencies (paper:Robinson2019, paper:Drummond2023, paper:Zito2025), to large agnostic
screens that scan many covariates or germline variants against measured signature activities
(paper:Sorensen2023, paper:ValiPour2022). The textbook aetiology map — UV→SBS7, tobacco→SBS4,
APOBEC→SBS2/13, MMR-deficiency→SBS6/15/26/44 — has been recovered by every major method applied
to well-powered data, establishing it as a methodological positive-control benchmark. What remains
contested is the best statistical architecture for agnostic discovery of novel aetiologies, how to
handle tissue-of-origin as a master confounder, and how to adjudicate causality once an association
is found. These questions are the direct antecedents of hypothesis h08.

## Key Concepts

**Signature exposure (H matrix).** Per-sample scalar assigned by NMF or restricted refitting
quantifying "how much" of a given mutational process operated in that tumour. Distinct from the
signature spectrum (W matrix), which captures "which process." Approaches to h08 treat H as the
outcome variable.

**Textbook aetiology map.** A subset of COSMIC SBS signatures has robust, replicated aetiological
assignments: SBS7a–d (UV photoproduct misrepair, C>T at dipyrimidines), SBS4/SBS29 (tobacco
combustion carcinogens, C>A transversions), SBS2/SBS13 (APOBEC3 cytidine deaminase, TCA/TCG
context), SBS6/SBS15/SBS20/SBS21/SBS26/SBS44 (defective DNA mismatch repair / MSI), SBS10a/b
(POLE/POLD1 proofreading deficiency), SBS3 (homologous recombination deficiency, especially
BRCA1/2). SBS5 and SBS40 (clock-like, ubiquitous) have no cleanly established aetiology; SBS54
has recently been proposed as an additional dMMR marker (paper:Ji2023).

**Tissue specificity.** The same exogenous exposure produces different trinucleotide-context
signatures in different tissues (paper:Afsari2021). Tobacco smoking elevates SBS4 in lung but
SBS5 in urothelial cancer (paper:Kim2016). Ageing signatures are markedly tissue-specific at the
feature level. This is the strongest constraint on analysis design: aetiology associations must be
evaluated *within* tissue strata, not pan-cancer.

**Supervised vs. agnostic designs.** Supervised approaches (paper:Afsari2021) take an exposure
label and learn a signature optimised to classify it; they achieve higher precision for the
targeted exposure but cannot discover unknown aetiologies and require annotation. Agnostic designs
(paper:Robinson2019, paper:Sorensen2023) use signatures extracted without aetiology labels and
then correlate them against a covariate grid; they sacrifice per-exposure precision for
generalisability and discovery potential.

**Joint vs. post-hoc association.** Post-hoc methods fit signatures first (NMF, SigProfiler),
then regress exposures against covariates. Joint methods (paper:Robinson2019, paper:Zito2025)
condition the signature extraction itself on covariates, which improves separation of spectrally
similar processes (e.g. SBS3 vs SBS5) but requires covariate specification at training time and is
computationally heavier.

**Uncertainty propagation.** A persistent problem with post-hoc tests is that NMF exposure
estimates are point estimates with poorly characterised sampling variance, especially at low
mutation counts. Bayesian methods (paper:Rosales2017, paper:Drummond2023, paper:Park2023)
propagate posterior draws of the exposure matrix through all downstream association tests, giving
calibrated uncertainty at the cost of higher computation.

## Current State of Knowledge

**The textbook map is recoverable.** Every published method applied to adequately powered cohorts
(>100 samples per stratum; WES or WGS) successfully recovers at least the core UV, tobacco, and
APOBEC aetiologies without being given them. This has been demonstrated by TCSM (paper:Robinson2019)
recovering UV→SBS7 in melanoma and smoking→SBS4 in lung; signeR 2.0 (paper:Drummond2023) recovering
MMR-deficiency signatures in gastric cancer with AUC 0.983; Diffsig (paper:Park2023) recovering HRD→
SBS3 and HER2→APOBEC in breast cancer; SuperSigs (paper:Afsari2021) achieving median AUC 0.90 for
all annotated exposures; and the GSGP gene-level approach (paper:Ji2023) recovering cholinergic
receptor genes under SBS4 and UV-response genes under SBS7. The convergence of methods gives the
textbook map strong empirical status.

**Novel aetiologies are discoverable via systematic screens.** paper:Sorensen2023 identified 24
DDR genes (24 of 736 tested) whose biallelic or monoallelic LOF is predictive from WGS mutational
patterns, including expected associations (BRCA1/2, MSH3, CDK12) and genuinely novel ones
(ATRX/IDH1→SBS8 depletion in CNS; PTEN-d→SV depletion in CNS and uterus). paper:ValiPour2022
identified 42 germline genes with replicated associations to somatic mutational components via rare
variant association study, including APEX1 as a novel upstream modifier of APOBEC mutagenesis.
paper:Kim2016 established ERCC2 somatic mutations as the first NER-deficiency predictor for a
SBS5-like signature in urothelial cancer, discovered without prior hypothesis. These demonstrate
that the agnostic-scan paradigm is productive beyond the textbook map.

**Tissue-specificity is not merely a confounder — it is an aetiological signal.** paper:Afsari2021
showed that aging, smoking, and environmental exposures all produce tissue-specific signature
spectra rather than a single pan-cancer profile. paper:Kim2016 provided a concrete case where
tissue biology reverses the expected signature identity (tobacco→SBS5, not SBS4, in urothelial
epithelium). This finding directly determines analysis design: within-tissue conditioning is not
optional and the pan-cancer version of any covariate→signature association is dominated by
tissue-of-origin confounding (paper:Robinson2019 found cancer type absorbed the smoking and UV
signals when used as the only covariate in a multi-tissue model).

**Stop-gain mutations provide a functional readout of signature aetiology.** paper:Adler2023
showed that the mechanistic specificity of SBS4 and SBS13 — their trinucleotide preferences happen
to convert serine and glutamic acid codons to stop codons at high rates — produces significant
enrichment of nonsense mutations in the same genes (TP53, FAT1, APC, STK11) across three
independent cohorts. This supplies an orthogonal, functional verification layer for covariate→
signature links: correct recovery of a smoking→SBS4 association should be accompanied by elevated
stop-gain burden in the expected gene set.

**Genomic covariates (histone marks, replication timing, methylation) are strong within-sample
signature determinants.** paper:Zito2025 showed that jointly fitting signature intensities with
genomic-locus covariates recovers SBS1 with near-perfect cosine similarity via the methylation
coefficient, and quantifies the replication-timing effect (late timing → +113% oxidative-damage
SBS18 activity). This establishes that per-sample-level covariate associations (the target of h08)
operate on top of large genome-level modifiers that are signature-specific.

## Controversies & Open Questions

**Joint vs. post-hoc: power tradeoff.** Joint models (paper:Robinson2019, paper:Zito2025) improve
separation of spectrally similar signatures (SBS3/SBS5 pair) and avoid post-hoc p-value deflation
from exposure uncertainty, but require covariate pre-specification and scale poorly to
phenome-wide grids of hundreds of covariates. The literature has not established whether the power
gain from a joint model is large enough to justify the loss of agnosticity for a discovery scan.
[SPECULATION: for well-separated signatures (SBS7 vs SBS4) the distinction is probably
negligible; for correlated pairs (SBS3/SBS5, SBS2/SBS13) it may matter.]

**The causal direction of expression→signature associations is not identified by association
alone.** paper:Afsari2021 notes that obesity may accelerate cell division rather than directly
cause DNA damage; paper:Adler2023 flags that APOBEC3A upregulation could be downstream of
replication stress rather than upstream. paper:Rosales2017 and paper:Drummond2023 surface group
differences but do not resolve direction. The expression↔signature edge in the h08 DAG has a
bidirected component (paper:Kim2016's clonality argument is the strongest counter-example, using
temporal ordering of clonal expansion to argue ERCC2 loss precedes signature accumulation). No
consensus method for causal adjudication from cross-sectional tumour data exists beyond mediation
analysis and clonal timing arguments.

**SBS5 aetiology.** SBS5 is active pan-cancer and correlates with age in many tissues, but
paper:Kim2016 showed it is specifically elevated by ERCC2 somatic mutation and tobacco in
urothelial cancer — a tissue-specific genetic covariate absent from the clock-like narrative.
paper:Sorensen2023 found ARID1A-d in prostate also associates with SBS8 depletion independently
of BRCA status. Whether SBS5/SBS40 have a universal mechanistic explanation or are heterogeneous
sums of processes remains unresolved.

**What constitutes a valid positive control for the agnostic approach?** The field consensus is
that UV→SBS7 (skin), tobacco→SBS4 (lung), and MMR-loss→SBS6/15/26 (multiple cancers) are the
strongest positive controls; APOBEC3A/B expression→SBS2/13 is also standard (paper:Adler2023,
paper:Afsari2021) but noisier because APOBEC activity is episodic while steady-state mRNA is
measured at a single timepoint. There is no published study directly comparing the rank-recovery
fidelity of the different positive-control proxies under the same agnostic framework, leaving
uncertainty about which arms are most likely to be "tolerated misses" in a 2-of-3 gate (per
paper:Park2023 and paper:Drummond2023 designs).

**Panel-sequencing limitations.** Most published methods (paper:Sorensen2023, paper:Zito2025,
paper:Rosales2017) assume WGS or WES. Per-sample signature assignment on targeted panels is
unreliable below ~100 mutations per sample (paper:Park2023 raises heteroskedastic concerns at low
count). The cBioPortal corpus is dominated by targeted panels; this is a material constraint for
any direct h08 implementation on that substrate rather than on MC3.

**Germline vs. somatic covariate space.** paper:ValiPour2022 showed that germline rare pLoF
variants in 42 genes explain a detectable fraction of somatic signature variance. h08's agnostic
scan targets somatic and clinical covariates rather than germline; the germline signal constitutes
a background that should be treated as a confounder or stratification variable if ancestry and
germline sequencing are available.

## Implications for h08 and the Cross-Study Signature-Aetiology Aggregation

**The textbook-map recovery is well-precedented and confirmatory, not novel.** TCSM
(paper:Robinson2019) already demonstrates recovery of UV/smoking/APOBEC/MMR by an agnostic
tumour-covariate model. Signerimport (paper:Drummond2023), Diffsig (paper:Park2023), and SuperSigs
(paper:Afsari2021) repeat it with different architectures. H08a (the pre-registered positive-
control gate) should therefore be framed as *confirmatory re-validation on MC3* using a pre-
registered pipeline, not as a primary discovery claim. The claim to novelty lives entirely in H08b:
the use of unsupervised co-expression modules as the agnostic covariate set, plus the cross-
decomposition concordance (latent H ↔ latent expression module) logic, plus the pre-registered
gating framework itself.

**Design consequence — within-tissue stratification is non-negotiable.** paper:Robinson2019 showed
cancer type absorbs smoking/UV signal if used as the sole covariate; paper:Afsari2021 showed
tissue-specific signature spectra; paper:Kim2016 showed tobacco→SBS5 (not SBS4) in bladder. Any
h08 association run without within-tissue conditioning will conflate tissue-of-origin with genuine
covariate effects. The method:h08-agnostic-association-model adjustment set is correct.

**The Diffsig Dirichlet-multinomial architecture (paper:Park2023) is the best current answer to
low-count uncertainty.** For panel-sequenced samples with few mutations per patient, naive NNLS
contribution estimates are highly variable (paper:Park2023 Figure 3 demonstration). Diffsig's
heteroskedastic treatment of compositional uncertainty is directly applicable to the MC3 WES
substrate but will require careful prior recalibration for the multi-cancer, multi-assay
cBioPortal corpus. TCSM (paper:Robinson2019) is an alternative with a full joint-inference design,
but its covariate-prespecification requirement limits phenome-wide use.

**signeR's Differential Exposure Score (DES) is a practical baseline.** paper:Rosales2017 and
paper:Drummond2023 provide DES (Kruskal–Wallis over posterior draws of the exposure matrix) as a
computationally accessible association primitive for categorical and continuous covariates. Applying
DES to binary clinical covariates (smoking status, MSI status) within each tissue stratum is a
direct feasibility check before committing to a heavier Diffsig or TCSM-style model.

**SBS54 should enter the MMR/MSI positive-control set.** paper:Ji2023 showed SBS54 outperforms
all seven established dMMR signatures at discriminating MSI from MSS colorectal and gastric cancer
(FDR 1.1×10⁻¹⁶). If SBS54 is absent from the restricted SigProfiler assignment used in the h08
positive-control run, the MSI arm could miss; it should be added to the active-signature
denominator for the MSI stratum.

**ERCC2→SBS5 in urothelial cancer is a fourth positive control, not in the pre-registered gate.**
paper:Kim2016's clean recovery of a somatic-gene→signature association without prior knowledge
demonstrates the discovery mode that h08b targets. Including it as an exploratory secondary check
(alongside MMR→SBS6/15/26 and POLE→SBS10) would increase confidence that the pipeline is
genuinely agnostic rather than overfitted to the three primary arms.

**Stop-gain enrichment (paper:Adler2023) provides functional validation for any hit.** For
signatures where the trinucleotide preference intersects stop-codon codons (SBS4/13/18 primarily),
a confirmed covariate→signature association should be accompanied by elevated stop-gain burden in
the signature-implicated driver genes (TP53, FAT1, APC). This is an orthogonal cross-check that
does not depend on signature decomposition at all and is directly computable from the pipeline's
existing per-gene mutation-frequency tables via the Bailey 2018 driver overlay.

**The PPF genomic-covariate framework (paper:Zito2025) is the locus-level analogue of h08** but
requires WGS with positional information — not available at cBioPortal panel scale. Its key
practical lesson is that apparent covariate effects (e.g., replication timing→signature) can be
estimated as confounders: any per-tissue association between a clinical covariate and signature H
must account for the fact that tumours with different histologies have different replication timing
and chromatin landscapes, and these genomic properties are independently strong signature
determinants.

**Expression modules as novel covariates (the H08b claim) are supported by the ValiPour network
logic.** paper:ValiPour2022 showed that PPI-network modules of germline repair genes predict
signature components, not just single genes. The analogous somatic claim is that expression
modules of HR, MMR, or APOBEC-pathway genes should predict respective signature exposures as
composite features, with higher power and robustness than any single mRNA. This is the mechanistic
rationale for the NMF module design in the h08 pre-registration.

**Reverse causation must be addressed per-hit.** Every paper in this topic that reports an
expression→signature association acknowledges the possibility that signature accumulation reshapes
the transcriptome rather than the converse. The only robust published mitigation is paper:Kim2016's
clonality approach (ERCC2 clonal mutations → signature is clonal, arguing ERCC2 loss is early).
For h08b discovery hits, mediation analysis and cross-study replication are the primary defences;
the pipeline's existing hypermutator flag and CH-contamination stratification address adjacent
confounders but not reverse causation per se.

## Key References

- paper:Robinson2019 — TCSM: the direct methodological predecessor for joint tumour-covariate
  signature modelling; validates UV/smoking/APOBEC/MMR recovery agnostically.
- paper:Drummond2023 — signeR 2.0: uncertainty-propagating association toolkit (DES + survival);
  MMR/MSI recovery in STAD at AUC 0.983.
- paper:Park2023 — Diffsig: Bayesian Dirichlet-multinomial model addressing low-count composition
  uncertainty; recovers HRD→SBS3 and HER2→APOBEC in BRCA.
- paper:Afsari2021 — SuperSigs: tissue-specific supervised signatures; establishes pan-cancer
  tissue-specificity constraint and the obesity signal in kidney/uterine cancer.
- paper:Sorensen2023 — pan-cancer systematic DDR-gene LOF → signature screen; the best design
  template for agnostic association scan shape and PR-AUC-E benchmarking.
- paper:Kim2016 — ERCC2→SBS5 in urothelial cancer; tissue-specific tobacco→signature identity
  and clonal-timing causality argument.
- paper:Adler2023 — SBS4/SBS13 trinucleotide preference → stop-gain enrichment; functional
  readout and orthogonal validation layer for covariate→signature recovery.
