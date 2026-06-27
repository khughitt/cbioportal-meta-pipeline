---
type: discussion
title: 'Common mutational signatures: known vs learned, immune causes, and confounding'
status: complete
created: 2026-05-30
updated: '2026-05-30'
id: discussion:0004-common-mutational-signatures-known-vs-learned-immune-causes-and
related:
- topic:mutational-signatures
source_refs:
- paper:Alexandrov2020
- cite:Alexandrov2013CellRep
- cite:Alexandrov2013Nature
- cite:NikZainal2012
- cite:Kucab2019
- cite:Degasperi2022
focus_type: topic
focus_ref: topic:mutational-signatures
mode: qa
---
# Common mutational signatures: known vs learned, immune causes, and confounding

## Focus

A conceptual Q&A on the epistemics of mutational-signature analysis, framed by four
questions:

1. What are the most common signatures, split into (a) "known"/human-labelled aetiologies and
   (b) learned/unbiased latent factors — and what is the difference between the two framings?
2. How often is the immune system inferred as an *upstream* cause of a signature?
3. How likely are we to be biased by studying processes we already believe are causative — and
   for each curated aetiology (UV, smoking, …), what are the plausible confounders, mediators,
   or alternative causal explanations?

This project (`cbioportal`) does **not** currently extract signatures (see
`topic:mutational-signatures`). The discussion is therefore framed around what a downstream
signature step *would* import as assumptions, and where those assumptions are most fragile.

> Reference discipline: claims below are backed by the cited mutational-signature framework,
> catalog, breast-cancer, experimental-mutagen, and GEL WGS papers.
> Related tooling papers are cited only where they support a methodological claim.

## Current Position

The "known/labelled" vs "learned/latent" split is one factorization (NMF of the 96-channel SBS
catalog) followed by an optional, bias-laden recognition step against COSMIC — not two different
methods. Prevalence is decoupled from mechanistic understanding: the two most common signatures
(SBS1 mitotic clock, SBS5 unexplained flat spectrum) are precisely the ones whose aetiology is
weakest, so "unknown cause" is central rather than residual. The immune system is essentially
never a *labelled* upstream cause; its strongest claim is the APOBEC–antiviral mediator link,
and immunoediting acts on signature *burden* (`H`, selection) rather than signature *shape*
(`W`). For `cbioportal`, which does not currently extract signatures, this is a set of
import-time assumptions: *if* a signature step is added it must run de novo extraction (not
refit-only), report COSMIC matches with cosine similarity rather than bare labels, attribute
within tissue and treatment strata, and carry an artifact-signature flag from day one.

## Critical Analysis

The central threat is **structural confirmation bias**: refitting to COSMIC can only return
processes already in the catalog, most aetiology labels are post-hoc correlations, and each
discovery gate (high-rank de novo extraction → noticing an unmatched factor → finding a
wet-lab/epidemiological correlate to name it) selects for the already-expected. Identifiability
is the second threat: tissue ↔ exposure collinearity means "signature caused by exposure X" is
partly "signature characteristic of tissue T" absent within-tissue contrasts; treatment-induced
spectra overlay intrinsic ones in mixed pre/post-treatment cohorts; and artifact signatures
(SBS27/43/45–60, 8-oxo-dG) mimic oxidative biology — a problem sharpened on panel data, this
project's likely input. The naive `Exposure → Signature` model is almost never identified from
observational tumor catalogs: tissue and repair capacity are common causes of both exposure and
spectrum, and selection sits on the burden side, so any "X causes signature S" claim must
condition on tissue, treatment, and ancestry and separate spectrum-attribution from
burden-attribution.

## Prompt 1 — Most common signatures: known (labelled) vs learned (latent)

### The two framings are the same math, different epistemic commitments

Both COSMIC "known" signatures and a project's "learned" factors come from the **same
generative model**: a non-negative matrix factorization (NMF) of the 96-channel SBS catalog,
`M ≈ W·H`, where `W` are signature spectra and `H` their per-sample exposures
[@Alexandrov2013CellRep; @Alexandrov2020]. The difference is not algorithmic; it is what you do
*after* factorization:

| | "Known" (COSMIC / labelled) | "Learned" (de novo latent) |
|---|---|---|
| Source | Reference catalog, ~80 SBS signatures (COSMIC v3.x, `Alexandrov2020`) | NMF/SignatureAnalyzer run on *your* cohort |
| Identity | Fixed spectrum + curated aetiology label | Anonymous factor (rank-dependent) |
| Rank k | Implicit (catalog already chose it) | Chosen by you (stability/reconstruction trade-off) |
| Failure mode | **Refitting bias**: forcing data onto a basis that may not have generated it | **Splitting/merging**: one process split across factors, or two merged into one |
| Interpretability | High (label attached) | Low until matched back to catalog |

The standard pipeline does *de novo* extraction **and then matches** the resulting factors to
the catalog — so most "known" signatures in a paper are really learned factors that passed a
cosine-similarity threshold against COSMIC. The "human vs unbiased" dichotomy is therefore
softer than it sounds: the unbiased step is the NMF; the bias enters at (a) rank selection and
(b) the catalog-matching/labelling step.

### Most common signatures (the empirically dominant ones)

Across pan-cancer cohorts the consistently high-prevalence SBS signatures are:

- **SBS1** — spontaneous 5-methylcytosine deamination; a near-universal **clock-like** signature
  correlating with age across many cancer types [@Alexandrov2013Nature; @Alexandrov2020].
- **SBS5** — the second clock-like signature; flat spectrum, ubiquitous, **aetiology still
  poorly understood** despite being one of the most common — a key honesty check on "we
  understand signatures."
- **SBS2 / SBS13** — APOBEC cytidine deaminase activity; very common in breast, bladder,
  cervical, head/neck, lung.
- **SBS4** — tobacco smoking (lung, head/neck).
- **SBS7a–d** — UV (melanoma/skin).
- **SBS6/15/20/26/44** — mismatch-repair deficiency / MSI.
- **SBS10a/b** — POLE proofreading deficiency (ultra-hypermutators).

> Note the asymmetry: the two **most common** signatures (SBS1, SBS5) are a clock and an
> *unexplained* flat spectrum. The well-labelled, mechanistically satisfying ones (UV, smoking,
> POLE) are common only within specific tissues. "Common" and "well-understood" are not the
> same axis.

### Key difference in one line

The learned representation answers *"what independent processes best reconstruct this catalog?"*;
the labelled representation answers *"which of the processes we have already named is present?"*
The first can discover; the second can only recognize. Anything genuinely novel shows up only
in the de novo step, and only if rank `k` is large enough to resolve it without over-splitting.

## Prompt 2 — How often is the immune system inferred as an upstream cause?

**Rarely, and almost never as a *direct* mutagenic signature.** The dominant labelled
aetiologies are exogenous mutagens (UV, tobacco, aflatoxin), endogenous enzymatic processes
(APOBEC, POLE), and DNA-repair defects (MMR, HR/BRCA-associated SBS3; [@NikZainal2012; @Alexandrov2020]). The
immune system enters causal stories at three removes, none of which is a clean "immune
signature":

1. **APOBEC (SBS2/13) as an indirect immune link.** APOBEC3 enzymes are innate-immunity
   antiviral restriction factors; their mutagenesis is a *side effect* of an immune defense
   program, often triggered by viral infection or replication stress. So the immune system is
   plausibly *upstream* of one of the most common signatures — but this is a mediated,
   contested pathway, not a labelled "immune" signature.
2. **Inflammation / ROS.** Chronic inflammation produces reactive oxygen species; some
   oxidative signatures (e.g. SBS18, 8-oxo-dG) are *consistent with* an inflammatory upstream
   cause but are not labelled "immune" and overlap heavily with a sequencing/oxidation artifact
   (SBS18 vs SBS36/OGG1 vs 8-oxo-dG sample-handling artifact).
3. **Immunoediting acts on the exposure, not the spectrum.** The immune system shapes *which
   mutated clones survive* (neoantigen selection), changing the **exposure distribution `H`**
   and the dN/dS of immunogenic mutations — not the **spectrum `W`**. This is a selection
   effect downstream of mutagenesis, the opposite of an "upstream cause."

**Bottom line:** in the standard catalog, the immune system is essentially never the *labelled*
upstream cause. Its strongest claim is the APOBEC-antiviral link (mediator, not label) and a
weak ROS/inflammation association. This is itself a candidate **labelling blind spot** (see Prompt 3):
the catalog was built to recognize chemical/enzymatic mutagens, so an immune-driven process
would more likely be absorbed into SBS5-like "unexplained flat" factors or APOBEC than be
discovered as its own aetiology.

## Prompt 3 — Confirmation bias and the confounders behind each labelled aetiology

### How likely are we biased toward processes we already think are causative? — High.

Three structural reasons the field is biased toward "things we already think cause mutations":

1. **The catalog is a labelled prior.** Refitting to COSMIC can only return processes already
   in the catalog. A novel process is invisible unless someone runs a high-rank de novo
   extraction *and* notices an unmatched factor *and* finds a wet-lab/epidemiological correlate
   to name it. Each gate selects for the already-expected.
2. **Aetiology assignment is correlational and post-hoc.** Most labels were assigned by
   correlating an extracted spectrum with a known exposure (smokers have SBS4; melanomas have
   SBS7). Correlation across heterogeneous cohorts, confounded by tissue, ancestry, age, and
   treatment. Experimental validation in mutagen-exposed cell systems exists for *some*
   signatures, especially environmental agents, but not most [@Kucab2019].
3. **SBS5 is the cautionary tale.** It is among the most common signatures and remains
   essentially unexplained — direct evidence that abundance does not imply we have identified
   the cause, and that "unknown" factors are not rare leftovers but central.

### Per-aetiology: confounders, mediators, alternative causal explanations

| Labelled signature | Stated cause | Confounders / mediators / alternatives |
|---|---|---|
| **SBS4** | Tobacco smoking | **Confounders:** alcohol co-use, occupational/air-pollution PAH exposure, ancestry. **Mediator:** the actual mutagen is benzo[a]pyrene–DNA adducts processed by transcription-coupled NER — "smoking" is a behavioral proxy for a chemical mechanism that other PAH sources also produce. **Alt:** SBS4-like spectra appear in some non-smokers (other combustion exposures). |
| **SBS7a–d** | UV light | **Confounders:** latitude, skin pigmentation/ancestry, immunosuppression (transplant patients). **Mediator:** CPD/6-4 photoproduct formation + repair capacity — inter-individual NER efficiency modulates dose→signature. **Alt:** tanning-bed vs solar UV indistinguishable in spectrum; the "cause" is conflated with behavior. |
| **SBS2/SBS13** | APOBEC enzymes | **Upstream causes contested:** viral infection (HPV), replication stress, episodic "kataegis" bursts, possibly innate-immune activation (see Prompt 2). **Confounder:** strong tissue tropism (breast/bladder) confounds APOBEC with tissue. **Mediator:** APOBEC is itself the *mediator* of some upstream trigger we mostly cannot name. |
| **SBS1** | 5mC deamination (age clock) | **Confounder:** cell-division rate, not chronological age per se — proliferative tissues accrue SBS1 faster. **Alt:** "age" is a proxy for mitotic count; tissue stem-cell dynamics, not time, drive it. |
| **SBS6/15/20/26** | MMR deficiency / MSI | **Confounders:** Lynch-syndrome germline status, tissue, hypermutation co-occurrence. **Mediator:** loss of a specific MMR gene (MLH1 methylation vs MSH2 mutation) gives subtly different spectra collapsed into one label. |
| **SBS3** | HR deficiency (BRCA) | **Confounder:** platinum/PARP-inhibitor treatment history (treatment-induced signatures mimic/overlay). **Alt:** flat, hard to distinguish from SBS5 / sequencing noise — low identifiability. |
| **SBS10a/b** | POLE proofreading | Among the cleanest (specific hotspot context), but **confounded with MMR co-loss** in ultra-hypermutators; exposure attribution between POLE and MMR is ambiguous when both present. |

### Cross-cutting confounders that threaten *all* aetiology labels

- **Tissue ↔ exposure collinearity.** Each exposure is enriched in specific tissues, so
  "signature caused by exposure X" is partly "signature characteristic of tissue T." Without
  within-tissue contrasts, exposure and tissue are not separately identifiable.
- **Treatment-induced signatures.** Chemo/radiotherapy imprint their own spectra; cohorts mixing
  pre/post-treatment samples confound iatrogenic with intrinsic processes.
- **Sequencing & sample-handling artifacts.** SBS27, SBS43, SBS45–60 are artifactual; 8-oxo-dG
  from FFPE/oxidation mimics oxidative biology — artifact vs aetiology is a real identifiability
  problem, sharpened on panel data (this project's likely input).
- **Ancestry / germline background** confounds exposure proxies and repair-capacity variation.
- **Selection vs mutagenesis.** Exposures (`H`) are shaped by clonal selection and immunoediting
  *after* mutations occur, so abundance of a signature reflects both generation and survival —
  reverse-causation risk when reading exposure as dose.

### Causal-DAG framing (for any downstream signature work)

The naive model `Exposure → Signature` is almost never identified from observational tumor
catalogs. The minimally honest DAG is:

```
Ancestry/Germline ─┐
                   ├─→ Repair capacity ─┐
Tissue ────────────┤                    ├─→ Spectrum W (signature shape)
Exposure (proxy) ──┘                    │
Treatment ─────────────────────────────┘
Selection/Immunoediting ──→ Exposure H (signature burden)   [acts post-mutagenesis]
```

Tissue and repair capacity are common causes (confounders) of both exposure and spectrum;
selection sits on the burden side, not the spectrum side. Any "X causes signature S" claim
needs to condition on tissue, treatment, and ancestry, and to separate spectrum-attribution
from burden-attribution.

## Evidence Needed

| Claim under test | Evidence / analysis that would settle it |
|---|---|
| De novo vs refit give materially different exposures on *this* cohort | Run both on the aggregated catalog; compare exposure correlation + count unmatched de novo factors |
| Panel data (project's likely input) can support signature inference at all | Down-sample WES to panel footprints; measure spectrum reconstruction error vs mutation count; set a minimum-mutations threshold |
| Immune/inflammation has any detectable upstream signal | Test APOBEC (SBS2/13) and oxidative (SBS18) exposures vs immune-infiltration / viral-status covariates, within tissue |
| Exposure labels survive confounder adjustment | Within-tissue, treatment-stratified association of each labelled exposure with its proxy covariate |
| Artifact vs biology separable on aggregated data | Quantify SBS27/43/45–60 and 8-oxo-dG loads; flag studies/batches with excess |

## Prioritized Follow-Ups

| # | Action | Type | Priority |
|---|---|---|---|
| 1 | Open question: "Can signature decomposition be added downstream of aggregation, and is panel data adequate?" (formalizes a `topic:mutational-signatures` open question) | question | High |
| 2 | Open question: "Does de novo extraction on the aggregated cohort surface factors *not* in COSMIC v3.x (novel/immune candidates)?" | question | Medium |
| 3 | If signatures are added: enforce within-tissue + treatment-stratified attribution and an artifact-signature flag from day one `[actionable now — design constraint, not code]` | design note | Medium |
| 4 | Decide the labelling policy: report de novo factors *and* their COSMIC match + cosine, never the label alone (prevents refitting bias from being invisible) | decision | Medium |

## Synthesis

The "human-labelled vs unbiased-learned" split is really one factorization (NMF) followed by an
optional, bias-laden recognition step against COSMIC. The most *common* signatures (SBS1, SBS5)
are a mitotic clock and an *unexplained* flat spectrum — so prevalence is decoupled from
mechanistic understanding, and "unknown cause" is central rather than residual. The immune
system is almost never a *labelled* upstream cause; its best claim is the APOBEC–antiviral
mediator link, and immunoediting acts on signature *burden* (selection), not signature *shape*
— a likely blind spot of a catalog built to recognize chemical/enzymatic mutagens. Confirmation
bias is structurally high: refitting can only return known processes, and most aetiology labels
are post-hoc correlations confounded by tissue, ancestry, treatment, and repair capacity, with
behavioral proxies ("smoking", "UV") standing in for chemical mechanisms. For this project, the
operational lesson is conditional: *if* a signature step is added, it must run de novo
extraction (not refit-only), report COSMIC matches with similarity rather than bare labels,
attribute within tissue and treatment strata, and carry an explicit artifact-signature flag —
especially given panel-data input where signature inference is fragile.
