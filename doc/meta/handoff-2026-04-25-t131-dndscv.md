# Handoff — 2026-04-25 — t131 dNdScv chain

## What we're working on

**Headline question (from `discussion:2026-04-24-gene-length-bias`):** Does
gene length confound (a) mutation-count rankings of "highly mutated" genes
and (b) the *literature attention* given to those genes? `question:0011-gene-length-as-literature-attention-confounder` formalizes
the literature-attention conjecture with a pre-registered partial-slope
falsifier.

**Empirical kickoff (`question:0011-gene-length-as-literature-attention-confounder` notebook, `c389837`):** Confirmed raw vs
length-adjusted gene rankings are essentially disjoint at the head
(Spearman ρ = 0.37, Jaccard@100 = 0.015). Length-only adjustment swings
to the opposite extreme — tiny-protein artifacts (BAGE2, PYY2, DEFB119,
TMSB4X, SPRR4) dominate the top-100 instead of long-gene passengers.
Neither raw nor length-only is defensible. Motivated `t131`.

**`t131` deliverable:** dNdScv (Martincorena et al. [@Martincorena2017]) selection-based ranking
as a third axis, joined into the canonical `gene_cancer_study_ratio_annotated.feather`
and consumed by a per-gene three-way comparison feather + marimo notebook
that includes a PubTator literature-attention correlation panel (the
`question:0011-gene-length-as-literature-attention-confounder` falsifier readout).

**Companion follow-up tasks already filed:**
- `t129` — length × PubMed-mention regression pipeline step
- `t130` — Stoeger & Nunes Amaral 2018 paper summary
- `t136` — canonicalize-to-GRCh38 at ingestion (long-term build strategy)

## What's accomplished this session (5 commits on main)

- `4b825f6` — design v3 (post-review)
- `673b1a3` — t131 implementation (13 files, +2128 LOC)
- `021bc5b` — bug fixes from PoC end-to-end run

**Files shipped:**
- `code/envs/dndscv.yml` (conda env; r-base + Bioconductor + dndscv runtime deps)
- `code/scripts/prepare_dndscv_input.py` (validate + cancer_type join + SNV filter)
- `code/scripts/combine_mut_per_cancer_type.py` (per-(cancer_type, build) MAFs; checkpoint)
- `code/scripts/run_dndscv.R` (rewritten; closes latent column-name bug)
- `code/scripts/reconcile_dndscv_per_cancer.py` (combines per-build outputs per cancer type)
- `code/scripts/aggregate_dndscv_per_gene.py` (per-gene min-q rollup)
- `code/scripts/join_dndscv_into_annotated.py` (11-column schema-contract)
- `code/scripts/compare_three_way_rankings.py` (PubTator join, three rank columns)
- `code/scripts/convert_to_feather.py` (extended: NCBI_Build → study_build.txt)
- `code/scripts/process_mc3.py` (extended: hg19 study_build.txt for tcga_mc3)
- `code/workflows/Snakefile` (8 new rules + checkpoint + `all_with_dndscv` target)
- `code/config/config-pan-cancer-dndscv.yml`
- `code/notebooks/t131_three_way_ranking_comparison.py`

**Latent bug closed in passing:** `run_dndscv.R` had been checking for
MAF-style capitalized columns (`Tumor_Sample_Barcode`, `Chromosome`)
since it was first written; project feathers use lowercase
(`sample_id_tumor`, `chromosome`). The rule had never actually run
end-to-end against pipeline output. Fixed.

**Build-source decision:** Switched from `meta_study.txt` (sparse — ~3
of surveyed studies have `reference_genome` field) to `NCBI_Build`
column in `data_mutations.txt` (present in 234/234 surveyed studies,
populated in 232/234). `study_reference_build_override` config map
handles the 2 empty-cell edge cases. **No silent default** — fails
loudly per AGENTS.md (`task:t131`).

**Two real bugs found during PoC run (committed in `021bc5b`):**
1. dndscv outputs `qallsubs_cv` (subs-only test, what we feed it after
   prepare_dndscv_input's SNV filter), not `qglobal_cv`. Reconcile
   normalizes on read.
2. pandas 2.2 `apply(include_groups=False)` excludes the grouping
   column. Replaced both apply calls with explicit `for sym, grp in
   groupby()` loops.

## Empirical results from PoC end-to-end run

PoC config: 4 studies (skcm, ucec, brca TCGA + msk_impact_2017),
57 cancer types after combine, 21,998 genes pan-cancer
(`results/poc-2026-04-17/summary/mut/table/three_way_ranking_comparison.feather`).

**Three-way Spearman matrix** (n=18,135 genes with all three signals from
`results/poc-2026-04-17/summary/mut/table/three_way_ranking_comparison.feather`):

| | raw | length-adj | dNdScv |
|---|---|---|---|
| raw | 1.000 | 0.124 | 0.088 |
| length-adj | | 1.000 | 0.015 |
| dNdScv | | | 1.000 |

Three rankings essentially uncorrelated.

**Bailey et al. [@Bailey2018] driver recovery @ top-N:**

| Scheme | @10 | @25 | @50 | @100 | @250 | @500 |
|---|---|---|---|---|---|---|
| raw | 1 | 1 | 3 | 5 | 10 | 17 |
| length_adj | 4 | 5 | 5 | 6 | 9 | 11 |
| **dNdScv** | **10** | **24** | **45** | **74** | **127** | **145** |

dNdScv recovers 74/199 Bailey drivers in top-100, 145/199 (73%) in top-500
(`task:t131`; `results/poc-2026-04-17/summary/mut/table/three_way_ranking_comparison.feather`).
14× better than raw, 12× better than length-adjusted at the head.

**`question:0011-gene-length-as-literature-attention-confounder` falsifier panel (Spearman vs PubTator log10 mentions):**

| Ranking | ρ_pubtator |
|---|---|
| raw | +0.127 |
| length_adj | -0.009 |
| dNdScv | +0.055 |

Raw mutation count is most-correlated with literature attention.
Length adjustment removes the correlation entirely. dNdScv
intermediate. **Direct empirical support for `question:0011-gene-length-as-literature-attention-confounder`'s conjecture**:
gene length confounds the literature-attention axis through the
mutation-count mediator.

**Top-15 by dNdScv** (all Bailey/CGC drivers, length range 313–2843 aa from `task:t131`):
FOXA1, GATA3, PTEN, RNF43, PIK3CA, SMAD3, AMER1, SETD2, TBX3, PIM1,
SMARCA4, APC, TCF7L2, NCOR1, PIK3R1.

## What remains

### Next session — start here

1. **`/science:review-pipeline`** with target = `t131` design plan
   (`doc/plans/2026-04-24-t131-dndscv-three-way-comparison-design.md`)
   plus this handoff. Goal: catch any methodology or scope issues
   before committing to the full pan-cancer compute spend.

2. **Full pan-cancer-dndscv run** once review is clean:
   ```
   uv run snakemake -s code/workflows/Snakefile \
     --configfile code/config/config-pan-cancer-dndscv.yml \
     -j8 --rerun-triggers=mtime -- all_with_dndscv
   ```

   - Dry-run shows ~147 jobs against the existing
     `/data/packages/cbioportal/pan-cancer/` out_dir (vs 82 for PoC).
   - Wall time estimate: 30-90 min depending on parallelism +
     per-cancer cohort sizes (some are very large — UCEC POLE
     hypermutators, melanoma).
   - dndscv failed_qc rate observed in PoC: ~5/57 cancer types
     (small / weird-distribution cohorts; pipeline catches and
     continues). Expect similar fraction at full scale.

3. **Render the marimo notebook** with the actual full-cohort outputs:
   ```
   uv run --with marimo --with polars --with altair --with pyarrow --with scipy \
     marimo run code/notebooks/t131_three_way_ranking_comparison.py
   ```

   Notebook generates the full-resolution recovery panel + failure-mode
   panel + scatter plots + PubTator correlation readout.

### Conda-env path (currently a known gap)

The PoC run used **system R 4.5.3** (which happens to have arrow + dndscv
+ Biostrings already installed) instead of the pinned conda env. This
violates the `feedback:r-reproducibility` memory; the conda env path
hasn't been validated end-to-end yet.

Two options for the full run:
- **(a)** Use system R again (faster, but doesn't validate the conda
  reproducibility path).
- **(b)** Use micromamba via `--use-conda --conda-frontend mamba`
  with a `mamba` shim to micromamba. The conda env was successfully
  built once during this session (`micromamba env create -f
  code/envs/dndscv.yml` succeeded), so the YAML is valid; the
  Snakemake-driven invocation is what's untested.

Recommend **(b)** for the full run since reproducibility is the whole
point of the conda decision. If snakemake's `--use-conda` doesn't see
micromamba cleanly, fall back to (a) and file a follow-up task to
validate the conda path before any external publication of results.

### Optional follow-ups (already-filed tasks)

- **`t136`** (P2) — canonicalize-to-GRCh38 at ingestion via liftover.
  Removes the per-study refdb-routing complexity entirely. Long-term
  destination flagged during t131 design.
- **`t129`** (P2) — length × PubMed-mention regression pipeline step.
  Phase-2 of the `question:0011-gene-length-as-literature-attention-confounder` program (the t131 PubTator panel is the cheap
  Phase-1 readout; t129 is the formal regression with bootstrap CIs
  and per-subgroup analysis).
- **`t130`** (P2) — Stoeger & Nunes Amaral 2018 paper summary.
  Methodological reference for the literature-attention bias side.

### Session-state snapshot

- 5 commits on `main` since session start.
- 13 (in-session) work items all marked `completed`.
- `tasks/active.md` has t131 in-progress (no marker yet — the task
  itself is functionally done modulo the full-cohort run + review;
  consider closing after the next session).
- Memory: no new entries written this session.

## Pointers

- Plan: `doc/plans/2026-04-24-t131-dndscv-three-way-comparison-design.md`
- Discussion: `doc/discussions/2026-04-24-gene-length-bias-in-mutation-rankings-and-literature.md`
- Question: `entities/questions/0011-gene-length-as-literature-attention-confounder.md`
- Question 0011 PoC notebook: `code/notebooks/q011_length_adjustment_topn_comparison.py`
- T131 notebook: `code/notebooks/t131_three_way_ranking_comparison.py`
- T131 conda env: `code/envs/dndscv.yml`
- T131 side config: `code/config/config-pan-cancer-dndscv.yml`
- Three-way comparison feather (PoC): `results/poc-2026-04-17/summary/mut/table/three_way_ranking_comparison.feather`
- Joined annotated feather (PoC): `results/poc-2026-04-17/summary/mut/table/gene_cancer_study_ratio_annotated_dndscv.feather`
