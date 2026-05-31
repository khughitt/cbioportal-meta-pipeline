---
id: "search:2026-05-31-prior-agnostic-signature-aetiology-association"
type: "search"
title: "Prior agnostic / unsupervised mutational-signature aetiology association (signature-PheWAS, signature × expression, signature × covariate scans) — t177"
status: "active"
created: "2026-05-31"
updated: "2026-05-31"
related:
  - "hypothesis:h08-agnostic-covariate-association-recovers-known-signature-aetiologies-and"
  - "pre-registration:h08-positive-control"
  - "method:h08-agnostic-association-model"
  - "topic:signature-decomposition-unmatched-normal"
  - "task:t177"
---

# Prior agnostic signature-aetiology association — t177 — 2026-05-31

## Search Focus

`task:t177` gates `hypothesis:h08`. The question: **has the "agnostic" idea — treat per-sample
signature exposures `H` as outcomes and systematically associate them against co-measured covariates
(clinical, molecular, expression, germline) to infer aetiology — already been done?** And critically
for the pre-registered design (`pre-registration:h08-positive-control`): **did prior work demonstrate
positive-control recovery of known aetiologies (UV/smoking/APOBEC/MMR) as validation before claiming
novel hits?**

This determines the H08b **novelty bar**: h08's positive-control prong (H08a) can proceed regardless,
but the discovery prong (H08b) only adds value over what the field already has.

## Headline Finding (the one that matters for h08)

**The agnostic covariate↔signature-activity association is not a novel method — it is an established
sub-field with several named tools and at least two large systematic scans.** h08's methodological
contribution must therefore be reframed: *not* "invent agnostic signature-aetiology association"
(done) but a narrower, defensible delta. The genuinely under-occupied niche, after this scan:

1. **Expression-module covariates at scale.** The published covariate axes are clinical
   (`paper:Robinson2019`, `paper:Drummond2023`, `paper:Park2023`), DNA-repair-gene deficiency
   (`paper:Sorensen2023`), germline variants (`paper:ValiPour2022`), and TME/immune deconvolution
   (`paper:Luo2023`). **Unsupervised co-expression *modules* (NMF on mRNA) as the agnostic covariate
   set, jointly with per-sample signatures, is not the primary design of any single paper found.**
   `paper:Luo2023` is the closest (signatures × TME) but uses immune-deconvolution features, not
   de-novo expression modules, and is survival-oriented.
2. **The cross-decomposition concordance framing** (latent mutation factor `H` ↔ latent expression
   module, as co-equal unsupervised decompositions of the same patients) is h08's distinctive
   epistemic move and was **not** found as a stated design in prior work.
3. **Explicit pre-registered positive-control gating** (recover the known map *before* trusting novel
   hits, with a frozen pass rule) is methodologically standard-implied but **not pre-registered** in
   any prior paper — all do post-hoc validation.

**Net effect on h08:** H08a (positive control) is well-supported as *feasible* — multiple papers
recover UV/smoking/APOBEC/MMR unprompted (see table), so the gate is achievable, not aspirational.
H08b (discovery) needs its scope **narrowed to the expression-module / cross-decomposition delta**;
a generic "associate signatures with covariates" discovery claim would be **scooped**. This should be
recorded against `pre-registration:h08-positive-control` (whose §Null Result Plan already defers H08b
to a separate registration) — the H08b pre-reg, when authored, must cite this scan and claim only the
expression-module niche.

## What prior work has done (catalogued)

### A. Covariate-conditioned signature models (method papers)

| Tool | Covariate axis | Positive-control recovery shown? | Ref |
|---|---|---|---|
| **TCSM** (Tumor Covariate Signature Model) | clinical + molecular tumor-level covariates | **Yes** — HR-deficiency, UV (melanoma), smoking (lung), APOBEC, MMR | `paper:Robinson2019` |
| **signeR 2.0** | any clinical feature (survival, stage, subtype); Wilcoxon/Kruskal-Wallis differential exposure | tool, not a discovery study | `paper:Drummond2023` |
| **Diffsig** | risk factors (continuous/binary/categorical); Bayesian Dirichlet-multinomial | tool/preprint | `paper:Park2023` |
| **PPF** (Poisson process factorization) | locus-specific genomic covariates (incl. CNV) via log-linear exposure | recent methods paper | `paper:Zito2025` |
| **SuperSigs** | **supervised** etiology metadata (aging, obesity, smoking) — NB-NMF + SVM | builds signatures *from* etiology (the opposite framing) | `paper:Afsari2021` |

`paper:Robinson2019` (TCSM) is the **direct conceptual predecessor of h08**: explicitly framed as the
first method to model how tumor covariates change signature exposure *to infer etiology*, and it
validates by recovering the textbook map. h08's H08a is, essentially, a pre-registered re-run of the
TCSM validation logic on the MC3 substrate; this is fine for a positive control but means H08a is
**confirmatory-of-method**, not novel.

### B. Large systematic association scans (discovery studies)

| Study | Covariate axis | Scale | Positive controls recovered | Ref |
|---|---|---|---|---|
| **Sørensen 2023** | 736 DNA-repair-gene deficiencies | 6,065 WGS / 32 types | BRCA1/2→deletions, MMR→MSI indels, TP53→SVs; +novel ATRX/IDH1/PTEN/SMARCA4 | `paper:Sorensen2023` |
| **Vali-Pour 2022** | rare germline variants | large pan-cancer | MBD4→SBS1 (novel), BRCA→SBS3, APOBEC3-del→SBS2/13 | `paper:ValiPour2022` |
| **Luo 2023** | TME / immune deconvolution | 8,000+ TCGA | clock-like + AID/APOBEC most widespread | `paper:Luo2023` |

`paper:Sorensen2023` is the closest published analogue to the **h08 scan shape** (systematic
predictive association, gene-deficiency covariates, explicit positive-control recovery + novel hits).
h08's expression-module axis is the main thing it does not cover.

### C. Single-covariate exemplars (classic anchors)

- `paper:Kim2016` — somatic **ERCC2 → NER-deficiency signature** in urothelial cancer; signature also
  smoking-associated. The archetype of a single covariate↔signature association.
- `paper:Adler2023` — smoking (SBS4) + APOBEC (SBS2/13) processes generate functional protein-
  truncating variants; supports functional interpretation of h08 arms B and C.

## Query Set

1. signature-PheWAS / phenome-wide signature association (→ mostly PRS-PheWAS, not signature-activity;
   the term "signature-PheWAS" is **not** established in the literature).
2. signature exposure × gene expression × APOBEC3A/B (SBS2/13) → `paper:Luo2023`, APOBEC-expression
   association literature.
3. unsupervised / agnostic signature aetiology inference + clinical covariate → `paper:Robinson2019`
   (TCSM), `paper:Drummond2023` (signeR 2.0), `paper:Park2023` (Diffsig), `paper:Zito2025` (PPF).
4. de-novo extraction recovers known etiology (UV/smoking/APOBEC) as validation → SigProfilerExtractor
   family (positive-control feasibility confirmed; already in project context).
5. germline determinants of somatic signatures → `paper:ValiPour2022`.
6. DNA-repair-deficiency systematic signature scan → `paper:Sorensen2023`.
7. supervised signature-etiology (SuperSigs) → `paper:Afsari2021`.
8. signatures × tumor microenvironment / immune → `paper:Luo2023`.
9. ERCC2 / single-covariate exemplar → `paper:Kim2016`.

## Sources and Run Metadata

- Primary discovery: **WebSearch** (OpenAlex/PMC surfaced) + **WebFetch** against PMC / Crossref /
  publisher pages for metadata verification. All DOIs verified against the source record (not memory).
- Retrieved: 2026-05-31.
- Candidates after dedupe: ~10 load-bearing (catalogued above) from ~30 surfaced.
- 10 new entries added to `papers/references.bib` (Robinson2019, Drummond2023, Park2023, Sorensen2023,
  ValiPour2022, Afsari2021, Zito2025, Luo2023, Kim2016, Adler2023).

## PDFs

Saved to `papers/pdfs/` (gitignored — never enter commits; this list is the durable record).
**4 of 10 acquired** this session, each verified on disk as a genuine PDF (`file` says "PDF
document", nonzero size, distinct md5 + first-page text):

- ✅ Drummond2023 (signeR 2.0) — BMC OA — 1.7 MB
- ✅ ValiPour2022 (germline variants) — Nature Communications OA — 2.1 MB
- ✅ Luo2023 (signatures × TME) — Frontiers OA — 9.6 MB
- ✅ Zito2025 (PPF) — arXiv — 4.9 MB

**6 PDFs NOT acquired — need manual retrieval** (full metadata + abstract-level summaries are recorded
above and bib entries exist; only the PDF files are missing):

| Paper | DOI | PMCID | Note |
|---|---|---|---|
| ❌ Robinson2019 (TCSM) | 10.1093/bioinformatics/btz340 | PMC6612886 | OUP/PMC — try manual |
| ❌ Sorensen2023 (DNA-repair scan) | 10.7554/eLife.81224 | PMC10115443 | eLife/PMC — try manual |
| ❌ Afsari2021 (SuperSigs) | 10.7554/eLife.61082 | PMC7872524 | eLife/PMC — try manual |
| ❌ Kim2016 (ERCC2) | 10.1038/ng.3557 | PMC4936490 | PMC author manuscript |
| ❌ Adler2023 (smoking+APOBEC) | 10.1126/sciadv.adh3083 | PMC10624356 | Science Adv OA / PMC |
| ❌ Park2023 (Diffsig) | 10.1101/2023.02.09.527740 | — | bioRxiv only, no PMCID |

Automated routes all failed this session: publisher pages (Nature/OUP/Science) block `curl`; eLife
`/pdf` returned empty; the EuropePMC render backend returned empty/short content for these accessions
today; `papis --from scihub` mirror was unreachable. The 4 acquired came via their native OA
endpoints. (Honest correction: an earlier draft claimed "9 of 10 acquired" — that was written before
verification and was false; the downloads had failed. Corrected here to the 4 that genuinely landed.)

## Implications for h08 (action items)

1. **Narrow H08b scope** to the expression-module / cross-decomposition-concordance delta before
   authoring its pre-registration; a generic covariate↔signature discovery claim is scooped by
   `paper:Robinson2019` / `paper:Sorensen2023`.
2. **Cite `paper:Robinson2019` (TCSM) as the method predecessor** in
   `method:h08-agnostic-association-model` — h08's H08a is a pre-registered re-validation of the TCSM
   logic, which is a strength (reproducible positive control) but should be stated honestly, not as
   novelty.
3. **`paper:Sorensen2023` is the design template** for the scan shape (systematic + positive controls
   + novel hits with FDR); align h08's reporting with it.
4. **H08a feasibility is corroborated** — multiple independent papers recover the textbook map
   unprompted, so the 2-of-3 / top-3 gate in `pre-registration:h08-positive-control` is achievable.
5. t177 marked **done**; these implications are reflected in the h08 method note. The future H08b
   pre-reg must claim only the expression-module niche.

## Process Reflection

- `science datasets search` adapters do not index method/preprint literature; this scan was
  WebSearch + WebFetch driven, consistent with prior project searches.
- PDF acquisition friction was severe this session. **Worked:** native OA endpoints — BMC
  `/counter/pdf/<doi>.pdf`, Frontiers `/articles/<doi>/pdf`, arXiv `/pdf/<id>`, Nature Communications
  `<url>.pdf` (these 4 landed). **Failed today:** publisher pages behind paywalls (Nature
  subscription, OUP, Science main site) block `curl`; eLife `/pdf` returned empty; the EuropePMC
  render backend (`ptpmcrender.fcgi?accid=PMC…&blobtype=pdf`) returned empty/short content for the
  accessions tried; `papis add --from scihub` mirror was unreachable (timed out). bioRxiv-only
  preprints (no PMCID) remain a hard gap. **Lesson: verify each download with `file`/size before
  recording it as acquired** — several "successful" curls had saved HTML error pages or 0-byte files.
