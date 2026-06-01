# t182 — exploratory h08b SBS40-vs-SBS5 expression-module prototype

Date: 2026-06-01

## Question

Can the existing H08 expression-module substrate produce a coherent exploratory separation between SBS40 and SBS5 within tissue after conditioning on age?

This is explicitly exploratory.
H08a remains `[?]`, the repaired smoking-arm read remains `[?]`, and this result does not open H08b as confirmatory work.

## Artifacts

Run bundle:
`results/signature-h08-arms-2026-05-31/association/exploratory/h08b_sbs40_sbs5/`

- `h08b_sbs40_sbs5_module_contrast.feather`
- `h08b_sbs40_sbs5_target_genes.feather`
- `h08b_sbs40_sbs5.meta.json`

Script:
`code/scripts/run_h08b_sbs40_sbs5_prototype.py`

Plan:
`doc/plans/2026-06-01-t182-h08b-sbs40-sbs5-exploratory-plan.md`

## Primary Read

The primary outcome was the within-tissue, age-conditioned compositional contrast:

```text
clr_SBS40_minus_SBS5 = clr(SBS40_collapsed) - clr(SBS5)
```

SBS40 was collapsed only over active SBS40 components in each stratum's H08 manifest.
Models used trusted count-floor-passing MC3 exposures and adjusted for age, ancestry, and treatment when estimable.

Top primary contrast rows:

| Stratum | Covariate | n | coef | p | BH-q | Direction |
|---|---|---:|---:|---:|---:|---|
| SKCM | `module_04` | 363 | +0.154 | 8.70e-04 | 0.0348 | higher SBS40 relative to SBS5 |
| CESC | `module_02` | 184 | -0.638 | 4.29e-03 | 0.0858 | lower SBS40 relative to SBS5 |
| BLCA | `module_05` | 343 | +0.452 | 3.78e-02 | 0.451 | weak |
| BRCA | `module_09` | 176 | +0.572 | 4.51e-02 | 0.451 | weak |

Only the SKCM module survives an exploratory BH q < 0.05 threshold in the primary contrast family.
The CESC module is suggestive at q < 0.10 but not strong.

## Secondary Reads

The SKCM contrast is not a clean SBS40-elevation result.
For SKCM `module_04`, the separate fits are:

| Outcome | coef | p | BH-q |
|---|---:|---:|---:|
| `clr_SBS40` | +0.044 | 0.123 | 0.467 |
| `clr_SBS5` | -0.109 | 0.00185 | 0.148 |

The primary contrast is therefore driven mostly by lower SBS5 relative to the rest of the composition, not by a strong separate SBS40 increase.
The leading genes in SKCM `module_04` include immune/B-cell and antigen-presentation markers (`CXCL9`, `CXCL13`, `CD74`, `HLA-DRA`, `CD79A`, `MS4A1`), so the safest label is an immune-expression module associated with lower SBS5 relative to SBS40, not an SBS40 mechanism.

For CESC `module_02`, the separate fits point in the opposite direction:

| Outcome | coef | p | BH-q |
|---|---:|---:|---:|
| `clr_SBS40` | -0.186 | 0.0495 | 0.363 |
| `clr_SBS5` | +0.452 | 0.00545 | 0.218 |

Its leading genes include extracellular-matrix / stromal markers (`FN1`, `MMP2`, `POSTN`, `VCAN`, `MMP11`), again suggesting a substrate/context association rather than a signature-cause claim.

## Targeted LUAD REV3L / POLZ Check

`REV3L` was present in LUAD RSEM and was evaluable at n = 377.
It did not show an exploratory association:

| Gene | Outcome | n | coef | p | BH-q | Status |
|---|---|---:|---:|---:|---:|---|
| `REV3L` | `clr_SBS40_minus_SBS5` | 377 | -0.044 | 0.868 | 0.868 | evaluable |
| `REV3L` | `clr_SBS5` | 377 | +0.081 | 0.539 | 0.868 | evaluable |
| `POLZ` | both outcomes | 0 | NA | NA | NA | not evaluable: missing LUAD RSEM row |

`POLZ` absence is a data limitation, not a negative biological result.

## Interpretation

The prototype is candidate-bearing but not mechanism-bearing.
It shows that the H08 substrate can detect age-conditioned expression-module differences in the SBS40/SBS5 contrast, but the strongest signal is not cleanly SBS40-specific.

The best current read is:

- there is a detectable SKCM immune-expression module associated with lower SBS5 relative to SBS40;
- there is a weaker CESC stromal-expression module associated with higher SBS5 relative to SBS40;
- LUAD `REV3L` does not support the planned POLZ/REV3L polymerase-zeta mini-check on this substrate;
- `POLZ` cannot be evaluated from the LUAD RSEM matrix used here.

This does not promote H08b.
It does justify keeping SBS40-vs-SBS5 as an exploratory design target, but a future confirmatory version would need replication, module labeling, subtype controls, and the causal-direction guard from `question:q025`.

## Next Step

Do not broaden immediately into a full H08b scan.
The next useful refinement is either:

- label the SKCM and CESC modules more formally using top-gene enrichment before deciding whether they are biologically interpretable; or
- switch to the treatment-exposed cohort flag (`task:t181` / H10), which is now more directly connected to cross-study signature confounding.
