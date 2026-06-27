---
type: search
title: 'TMB follow-up: hypermutator classification + empirical concordance + tooling
  (rescoped t025)'
status: active
created: '2026-04-14'
updated: '2026-04-14'
id: search:0006-tmb-hypermutator-followup
---

# TMB follow-up — hypermutator + empirical concordance + tooling — 2026-04-14

## Search Focus

**Rescoped t025.** The original t025 scope ("Follow-up search: TMB harmonization —
Friends-of-Cancer-Research / Buchhalter") was fully covered by the t026 topic
`cross-panel-normalization-methods` and the t060 guide update: Merino et al. [@Merino2020]
(FoCR Phase I), Vega et al. [@Vega2021] (FoCR Phase II), Buchhalter et al. [@Buchhalter2019],
and Fancello et al. [@Fancello2019] are all in `papers/references.bib` with project-specific
writeups.

This rescoped search covers three TMB-adjacent areas *not* yet addressed:

1. **Hypermutator / ultramutator classification** — cutoffs, etiology (POLE/POLD1,
   MMR-deficiency, MSI), per-cancer-type variation. Directly supports task `t081`
   (hypermutator-aware sample exclusion / covariate in the pipeline).
2. **Empirical panel-vs-WES concordance studies** — Chalmers et al. [@Chalmers2017] FoundationOne
   100k, Heydt 2021 multi-panel German consortium, Samstein et al. [@Samstein2019] MSK-IMPACT, real-world /
   in-silico benchmarks. The empirical complement to FoCR's calibration framework.
3. **TMB clinical cutoff / per-histology variation** — Marabelle et al. [@Marabelle2020]
   KEYNOTE-158, Samstein et al. [@Samstein2019] per-histology cutpoints, Rousseau et al.
   [@Rousseau2021SpectrumBenefit] universal-cutoff critique. Not a
   primary research target for this project (ICI response is out of scope) but load-
   bearing context for interpreting any TMB value the pipeline produces.

**Explicitly out of scope / not re-surveyed** (covered in `topic:cross-panel-normalization-
methods`, t026/t060): FoCR Phase I [@Merino2020], FoCR Phase II [@Vega2021],
Buchhalter et al.'s "Size matters" study [@Buchhalter2019], and Fancello et al.'s panel-TMB
review [@Fancello2019]. BED-level callability methods
(`topic:cross-panel-normalization-methods` Method B). Panel design decisions for TERT
promoter / fusions (`topic:targeted-panel-sequencing-bias`).

## Query Set

1. **Hypermutator classification anchors** — named-method lookup for Campbell et al.
   [@Campbell2017Hypermutation] ("Comprehensive Analysis of Hypermutation in Human Cancer");
   2020 Caris pan-cancer TMB reports; 2018 POLE-hypermutator reports.
2. **Empirical panel-vs-WES concordance** — Chalmers et al. [@Chalmers2017] FoundationOne
   (GM 9:34);
   Heydt 2021 multi-panel German consortium; Stetson 2019 Tempus; Hagemann 2023 Mayo.
3. **TMB clinical cutoff** — Marabelle et al. [@Marabelle2020] Lancet Oncology KEYNOTE-158
   (≥10 mut/Mb); Samstein et al. [@Samstein2019] MSK-IMPACT Nat Genet per-histology
   cutpoints; Rousseau et al. [@Rousseau2021SpectrumBenefit] 2021/2022
   universal-cutoff critique.
4. **TMB tooling** — jasonwong-lab/TMB (GitHub); pyTMB (IHEC); PureCN purity-adjusted
   TMB; MutationalPatterns.
5. **Recent (2023-2026)** — panel-based TMB enhancements; MSI-H / TMB-H
   intersection.

## Sources and Run Metadata

- Primary sources: **WebSearch** (OpenAlex/PubMed fallback) for specific title+author
  lookups plus LLM-knowledge seeding.
- Retrieved: 2026-04-14.
- Shared runtime (`uv run science-tool literature search …`): not available in project.
- Candidates retrieved (across all query variants, after dedupe): ~30.
- Shortlisted records in this report: **14** (5 `Core now`, 6 `Relevant next`, 3
  `Peripheral monitor`).

## Ranked Results

| # | Citation (short) | Year | IDs | Tier | Why it matters |
|---|---|---|---|---|---|
| 1 | Campbell BB, Light N, Fabrizio D, et al. "Comprehensive Analysis of Hypermutation in Human Cancer." *Cell* [@Campbell2017Hypermutation] | 2017 | PMID: 29056344 / DOI: 10.1016/j.cell.2017.09.048 | **Core now** | **The hypermutator/ultramutator classification reference.** >81,000 tumors pediatric + adult. Ultra-hypermutated (>100 mut/Mb) pediatric tumors **universally replication-repair-deficient**; adult ultra-hypermutators enriched for POLE/POLD1 mutations. Defines the two cutoffs we need for t081: hypermutator ≥10 mut/Mb; ultramutator ≥100 mut/Mb. |
| 2 | Chalmers ZR, Connelly CF, Fabrizio D, et al. "Analysis of 100,000 human cancer genomes reveals the landscape of tumor mutational burden." *Genome Med* [@Chalmers2017] | 2017 | PMID: 28420421 / DOI: 10.1186/s13073-017-0424-2 | **Core now** | **FoundationOne 100k-cohort TMB landscape.** Documents panel-TMB ↔ WES-TMB concordance; TMB increases 2.4× between age 10 and 90; per-tumor-type TMB distribution. Complements Campbell et al. [@Campbell2017Hypermutation] on the distributional side. |
| 3 | Samstein RM, Lee CH, Shoushtari AN, et al. "Tumor mutational load predicts survival after immunotherapy across multiple cancer types." *Nat Genet* [@Samstein2019] | 2019 | PMID: 30643254 / DOI: 10.1038/s41588-018-0312-8 | **Core now** | **MSK-IMPACT 1,662 ICI + 5,371 non-ICI.** Two load-bearing claims for our pipeline: (a) "capturing as little as 3% of the coding exome … provides sufficient estimation of total tumor mutational load" — small panels can give usable TMB rankings; (b) **per-histology TMB cutpoints vary markedly** (top 20% per histology) — rebuts universal-cutoff thinking. Both directly inform t081 design. |
| 4 | Marabelle A, Fakih M, Lopez J, et al. "Association of tumour mutational burden with outcomes in patients with advanced solid tumours treated with pembrolizumab: prospective biomarker analysis of the multicohort, open-label, phase 2 KEYNOTE-158 study." *Lancet Oncol* [@Marabelle2020] | 2020 | PMID: 32919526 / DOI: 10.1016/S1470-2045(20)30445-9 | **Core now** | KEYNOTE-158 established **≥10 mut/Mb as the clinically operational TMB-high cutoff** (29% ORR in tTMB-high vs 6% in non-TMB-high, 10 non-CRC cancer types). Led to the FDA's tissue-agnostic pembrolizumab TMB-H indication [@Marcus2021FDA]. Relevant only as the operational cutoff — ICI response is not our research target, but downstream consumers of our TMB annotations will interpret against this threshold. |
| 5 | Budczies J, Bockmayr M, Denkert C, et al. "Impact of panel design and cut-off on tumour mutational burden assessment in metastatic solid tumour samples." *Br J Cancer* [@Budczies2020BJC] | 2020 | DOI: 10.1038/s41416-020-0762-5 / PMID: 32055027 (not reconfirmed in this note) | Relevant next | In-silico analysis of 7 panels (incl. MSK-IMPACT, FoundationOne) vs WES; misclassification declined from up to 30% to <1% as the cutoff moved away from the noisy decision boundary. The **panel-TMB ↔ WES-TMB ROC analysis per panel**, complementary to Vega et al. [@Vega2021] calibration curves. |
| 6 | CRC-specific report: "Beyond microsatellite testing: assessment of tumor mutational burden identifies subsets of colorectal cancer who may respond to immune checkpoint inhibition." *J Gastrointest Oncol* | 2018 | PMID: 30505601 / DOI: 10.21037/jgo.2018.08.18 (identifier pairing not reconfirmed in this note) | Relevant next | CRC-specific: not all TMB-high CRC is MSI-H. **The MSI-H / TMB-H intersection is not 1:1** — a small fraction of MSS-CRC is TMB-high (POLE-hypermutator lineage). Relevant for t081 when we stratify TMB-high samples by MSI status. |
| 7 | Heydt C, Wolf J, Büttner R, et al. (and German NGS quality-assessment consortium). Multi-panel TMB correlation / comparability studies (2019–2021 cluster) | 2021 | DOI / PMID cluster not confirmed in this note | Relevant next | German quality-in-pathology consortium studies: 5+ large panels benchmarked against WES for TMB estimation; synonymous-variant inclusion has minor effect on correlation. Track as a cluster; individual paper identification needs OpenAlex verification. |
| 8 | Rousseau B, Foote MB, Maron SB, et al. "The spectrum of benefit from checkpoint blockade in hypermutated tumors." *N Engl J Med* [@Rousseau2021SpectrumBenefit] | 2021 | PMID: 33761214 / DOI: 10.1056/NEJMc2031965 | Relevant next | Critique / refinement of the pan-tumor ≥10 mut/Mb cutoff — not all TMB-high responds equally across tumor types. Important context when we surface TMB annotations: single-cutoff-only framings are known to be incomplete. |
| 9 | Marcus L, Fashoyin-Aje LA, Donoghue M, et al. "FDA Approval Summary: Pembrolizumab for the Treatment of Tumor Mutational Burden-High Solid Tumors." *Clin Cancer Res* [@Marcus2021FDA] | 2021 | PMID: 34083238 / DOI: 10.1158/1078-0432.CCR-21-1323 | Relevant next | Regulatory context for the ≥10 mut/Mb cutoff; explicitly defines how the FDA operationalized KEYNOTE-158 into a tissue-agnostic indication with FoundationOne CDx companion. Reference for downstream clinical-relevance framings. |
| 10 | Sha D, Jin Z, Budczies J, et al. "Tumor Mutational Burden as a Predictive Biomarker in Solid Tumors." *Cancer Discov* [@Sha2020TumorMutation] | 2020 | PMID: 32989011 / DOI: 10.1158/2159-8290.CD-20-0522 (identifier pairing not reconfirmed in this note) | Relevant next | Broader review of TMB-as-biomarker; good background reference. |
| 11 | Jason Wong lab / `jasonwong-lab/TMB` — "Two-layer Poisson panel-to-WES TMB correction." GitHub tool + associated 2021/2022 publication | 2021-2022 | GitHub: jasonwong-lab/TMB / PMID: not confirmed in this note | Relevant next | **Implementation tool** referenced in the Nat Rev Clin Oncol 2024 review. Two-layer Poisson model; public open-source. Direct candidate for our pipeline if we compute per-sample TMB from ingested MAFs. |
| 12 | Hypermutated Cancers 2021 Cancers (MDPI) — mutational-landscape synthesis | 2021 | PMID: 34503126 / DOI: 10.3390/cancers13174317 | Peripheral monitor | Recent review of hypermutator genomic landscape. Overlaps substantially with Campbell et al. [@Campbell2017Hypermutation]; cite only if needed. |
| 13 | Zhang Y, et al. "Enhancing the quality of panel-based tumor mutation burden assessment: a comprehensive study of real-world and in-silico outcomes." *npj Precis Oncol* [@Zhang2024EnhancinQuality] | 2024 | DOI: 10.1038/s41698-024-00504-1 / PMID: not confirmed in this note | Peripheral monitor | Recent panel-TMB benchmark; successor to Budczies et al. [@Budczies2020BJC] in spirit. Worth tracking for methodology. |
| 14 | Caris-cohort TMB landscape reports from 2020-2022 ASCO abstracts and follow-up papers | 2020-2022 | Conference abstracts + full-paper PMIDs not confirmed in this note | Peripheral monitor | Caris-specific TMB landscape work. Different panel from MSK-IMPACT / FoundationOne; complements the cross-panel picture if we ever ingest Caris cohorts. |

### Explicitly out of scope (covered in t026 / `topic:cross-panel-normalization-methods`)

- **Merino et al. [@Merino2020]** — FoCR TMB Harmonization Phase I. PMID 32217756. [already in bib]
- **Vega et al. [@Vega2021]** — FoCR TMB Harmonization Phase II. PMID 34606929. [already in bib]
- **Buchhalter et al. [@Buchhalter2019]** — "Size matters" panel-TMB floor. PMID 30238975. [already in bib]
- **Fancello et al. [@Fancello2019]** — panel-TMB review. PMID 31307554. [already in bib]

## Priority Reading Queue

**Core now (read first):**

1. **Campbell et al. [@Campbell2017Hypermutation] — hypermutator/ultramutator cutoffs + etiology** — read first for t081
   design (what does "hypermutator-aware sample exclusion" even mean operationally).
2. **Samstein et al. [@Samstein2019] — per-histology cutpoints** — read second. Argues against a single
   universal hypermutator cutoff applied pan-cancer; shows panel-TMB from 3% of exome
   gives usable ranking.
3. **Chalmers et al. [@Chalmers2017] — 100k-cohort TMB landscape** — read third for distributional shape,
   age correlation, panel-vs-WES concordance at population scale.
4. **Marabelle et al. [@Marabelle2020] — KEYNOTE-158 ≥10 mut/Mb cutoff** — read for the operational cutoff
   our downstream consumers assume (FDA TMB-H indication baseline).
5. **Budczies et al. [@Budczies2020BJC] — panel-design-and-cutoff impact** — read for the ROC-based view of
   misclassification near decision boundaries; complementary to Vega et al. [@Vega2021].

**Relevant next:**

6. 2018 CRC-specific MSI-H / TMB-H intersection report (stratification for t081).
7. Heydt / German-consortium cluster — multi-panel empirical concordance.
8. Rousseau et al. [@Rousseau2021SpectrumBenefit] NEJM letter — cutoff critique.
9. Marcus et al. [@Marcus2021FDA] — FDA approval summary (regulatory context).
10. Sha et al. [@Sha2020TumorMutation] Cancer Discov — broader TMB-biomarker review.
11. jasonwong-lab/TMB — implementation tool for two-layer Poisson panel→WES correction.

**Peripheral monitor:**

12. Cancers 2021 MDPI — hypermutator synthesis.
13. Zhang et al. [@Zhang2024EnhancinQuality] npj Precis Oncol — recent panel-TMB benchmark.
14. Caris-cohort TMB literature (if / when we ingest Caris).

## Coverage Notes and Gaps

- **Project-specific TMB computation path is not yet defined.** Our ingested cBioPortal
  MAFs carry per-variant records but no per-sample `tmb_mut_per_Mb` column. Any t081
  implementation has to (a) choose a per-study callable-coding denominator
  (canonical = per-panel callable Mb from `topic:cross-panel-normalization-methods`);
  (b) choose the variant filter (non-synonymous only vs all coding; which
  population-frequency filter); (c) decide whether to apply FoCR Phase-II calibration
  to make cross-panel TMB comparable. None of the 14 papers here prescribes a single
  answer — they are evidence for the design decisions.
- **Per-cancer-type hypermutator cutoffs are not published as a ready-to-use table.**
  Samstein et al.'s "top 20% per histology" [@Samstein2019] is a relative cutoff; Campbell et al.'s 10 and
  100 mut/Mb are absolute. A principled pipeline step would compute both and flag
  disagreements.
- **No project-scope-fit TMB tool.** jasonwong-lab/TMB, pyTMB, and the FoCR Phase-II
  release are all WES / panel-TMB tools — they assume you have either BAM-level input
  or a per-panel BED. Our pipeline ingests summary MAFs; implementing a simple
  `mutations_nonsynonymous / panel_callable_Mb` calculation from ingested data is a
  small pipeline script, not a tool-integration.
- **Age-TMB correction (Chalmers et al. [@Chalmers2017] ~2.4× 10→90y effect) is not handled by any tool
  surveyed.** If our t052 cohort-stage descriptor work also ingests age, flagging
  age-adjusted vs unadjusted TMB would be a cheap secondary column.
- **MSI-H and TMB-H are not 1:1.** The 2018 CRC-specific report documents MSS-CRC with high TMB (POLE
  lineage); Campbell et al. [@Campbell2017Hypermutation] document ultramutators with and without MSI. t081's binary
  "hypermutator" flag should be split into two flags (`is_hypermutator`,
  `is_ultramutator`) and paired with an `msi_status` column (we don't yet ingest the
  latter).
- **UNVERIFIED PMIDs flagged.** 8 of 14 entries have DOI-only provenance — verify via
  direct `esummary` before creating paper stubs. All 4 `Core now` entries with a
  specific PMID claim are verified via WebSearch (Campbell 29056344 [@Campbell2017Hypermutation],
  Chalmers 28420421 [@Chalmers2017], Samstein 30643254 [@Samstein2019], Marabelle 32919526
  [@Marabelle2020]).

## Recommended Next Actions

1. **Close-out t025** with this search report and the 7-ref core-plus-relevant delta
   over t026.
2. **Add BibTeX entries** for the 5 Core-now entries (Campbell et al. [@Campbell2017Hypermutation],
   Chalmers et al. [@Chalmers2017], Samstein et al. [@Samstein2019], Marabelle et al.
   [@Marabelle2020], Budczies et al. [@Budczies2020BJC]) and Marcus et al. [@Marcus2021FDA] to `papers/
   references.bib`.
3. **Update t081 (hypermutator-aware sample exclusion) scope** with the specific
   evidence anchors from this search:
   - Use Campbell et al. [@Campbell2017Hypermutation] absolute cutoffs (10 / 100 mut/Mb) as the primary flag.
   - Emit a second flag using Samstein et al. [@Samstein2019] per-histology top-20% logic.
   - Preserve both; downstream consumers pick.
   - Callable-Mb denominator from `topic:cross-panel-normalization-methods`.
4. **Cross-link** the rescoped search to `topic:tumor-mutational-burden` and to
   `topic:cross-panel-normalization-methods` (the empirical-concordance side of the
   calibration story).
5. **Stub paper notes** at `doc/background/papers/` for Campbell et al. [@Campbell2017Hypermutation],
   Chalmers et al. [@Chalmers2017], Samstein et al. [@Samstein2019], and Marabelle et al.
   [@Marabelle2020] (4 new stubs).
6. **Flag for future**: if MSI-status ingestion is added (not currently scoped), revisit
   the MSI-H / TMB-H intersection as a post-t081 refinement.
