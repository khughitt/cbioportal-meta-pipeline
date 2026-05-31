---
id: "paper:Diamond2023"
type: "paper"
title: "Tracking the evolution of therapy-related myeloid neoplasms using chemotherapy signatures"
status: "active"
ontology_terms:
  - mutational signatures
  - therapy-related myeloid neoplasm
  - clonal hematopoiesis
  - whole genome sequencing
  - chromothripsis
datasets: []
source_refs:
  - "cite:Diamond2023"
related: []
created: "2026-05-31"
updated: "2026-05-31"
---

# Tracking the evolution of therapy-related myeloid neoplasms using chemotherapy signatures

- **Authors:** Benjamin Diamond, Bachisio Ziccheddu, Kylee Maclachlan, Justin Taylor, Eileen Boyle, Juan Arango Ossa, Jacob Jahn, Maurizio Affer, Tulasigeri M. Totiger, David Coffey, Namrata Chandhok, Justin Watts, Luisa Cimmino, Sydney X. Lu, Niccolò Bolli, Kelly Bolton, Heather Landau, Jae H. Park, Karuna Ganesh, Andrew McPherson, Mikkael A. Sekeres, Alexander Lesokhin, David J. Chung, Yanming Zhang, Caleb Ho, Mikhail Roshal, Jeffrey Tyner, Stephen Nimer, Elli Papaemmanuil, Saad Usmani, Gareth Morgan, Ola Landgren, Francesco Maura
- **Year:** 2023
- **Journal:** Blood (Vol. 141, No. 19, 11 May 2023, pp. 2359–2371)
- **DOI/URL:** https://doi.org/10.1182/blood.2022018244
- **BibTeX key:** Diamond2023
- **Source:** PDF

## Key Contribution

Using whole-genome sequencing (WGS) of 39 therapy-related myeloid neoplasm (tMN) cases alongside de novo AML controls, this study demonstrates that chemotherapy-associated mutational signatures (SBS31/SBS35 for platinum; SBS-MM1 for melphalan) act as molecular barcodes that can time the acquisition of chromosomal gains, structural variants, and new driver mutations relative to treatment. The central finding is a dichotomy: tMN arising with evidence of chemotherapy-induced mutagenesis (particularly platinum/melphalan-exposed) are hypermutated, enriched for chromothripsis and complex structural variants, and frequently carry TP53 loss — whereas tMN lacking chemotherapy signatures are genomically similar to de novo AML. A second major finding is that for post-melphalan/ASCT cases, tMN can arise via two distinct routes: (1) reinfusion of a CH clone that escaped melphalan exposure via leukapheresis, or (2) a TP53-mutant CH clone that survived myeloablative conditioning and acquired melphalan-induced DNA damage directly.

## Methods

**Cohort:** 40 tMN WGS samples from 39 patients (16 platinum-exposed, 17 melphalan/ASCT-exposed [14 MM, 2 B-ALL], plus others); 21 de novo AML WGS (TCGA); 298 de novo AML WES (Beat AML); 22 tMN WES (Beat AML). Latency to tMN ranged from 2.4–7.2 years (median 5.5 years).

**Mutational signature analysis:** Signatures quantified using a published workflow (Degasperi et al.) applied to all WGS samples. Five SBS processes identified in tMN: SBS1 (aging), SBS-HSC (hematopoietic clock), SBS31 and SBS35 (platinum intercalation), SBS-MM1 (melphalan alkylation). Double-base substitution (DBS) and indel (ID) signatures also extracted. Wilcoxon tests compared mutational burden across groups.

**Targeted prechemotherapy sequencing:** 11 of the newly sequenced hematologic malignancy patients underwent targeted sequencing of blood mononuclear cells, granulocytes, and CD34+ apheresis products before melphalan, to detect antecedent CH clones at sub-WGS VAF resolution.

**Copy number / SV analysis:** GISTIC applied to de novo AML (n=316 exomes/WGS) and 39 tMN WGS; SV landscape compared between groups. Complex events (chromothripsis, chromoplexy, templated insertions) catalogued. tMN split by chemotherapy-signature positivity for differential CNA/SV analysis (Fisher test; FDR < 0.1).

**Chemotherapy signatures as temporal barcodes:** SNVs present within chromosomal gains (duplicated mutations) are used to time when CNAs occurred relative to chemotherapy — if a chemotherapy signature is in duplicated SNVs, the gain postdates chemotherapy exposure; if absent from duplicated SNVs, the gain predated it. Applied to 8 tMN with large CNAs and 2 post-chemotherapy MM cases.

**Molecular timing of chromosomal gains:** SBS5-based molecular time for MM chromosomal gains cross-validated against the SBS5-barcoding approach in 2 patients with secondary solid tumors and prior MM.

**Functional validation:** SMARCA4 overexpression in Ba/F3 cells tested for IL-3 cytokine independence (growth assay, P < 0.0001).

**Data availability:** New WGS + targeted sequencing uploaded to European Genome Archive EGAS00001006903.

## Key Findings

**Mutational landscape:**
- Only platinum and melphalan induce measurable SBS mutagenesis in tMN; other agents (cytarabine, anthracyclines, 5-FU) do not. SBS burden in melphalan/platinum-exposed tMN is significantly higher than in de novo AML or unexposed tMN (Wilcoxon P = .006 and P = .023 respectively), but tMN without chemo signatures is statistically indistinguishable from de novo AML (P = .492).
- Platinum also induces DBS signatures E-DBS3 and E-DBS9 (present in 8/10 platinum-exposed tMN, absent in unexposed; P < .001) and enrichment of ID8 indels in chemo-mutagenized tMN (P < .001).
- SBS-MM1 (melphalan) was present in only 7/17 (41%) melphalan-exposed cases; its absence in most is explained by the leukapheresis escape model (clones that avoid exposure are reinfused).

**Escape from chemotherapy-induced mutagenesis:**
- All 10 platinum-exposed tMN showed SBS31/SBS35, confirming full penetrance of single-cell expansion after platinum at detectable latencies (up to 25 years; IIQ 3.9–9.0 years).
- Conversely, 5 patients with post-melphalan/ASCT B-ALL lacked SBS-MM1, consistent with an expansion model in an alternate malignancy.
- Sequential platinum-then-melphalan patients showed tumors bearing only platinum signatures, supporting escape via leukapheresis and reinfusion before melphalan.
- Targeted prechemotherapy sequencing of apheresis products detected antecedent CH clones in 8/11 (72%) patients, including 3/4 leukapheresis samples — directly evidencing the clone reservoir available for reinfusion.

**Driver mutation landscape:**
- TP53 was the only driver significantly more mutated in tMN than de novo AML (Fisher P < .001; FDR = 0.009). NPM1 was more frequent in de novo AML (P < .001; FDR = 0.019).
- Platinum signatures contributed only a minor fraction (<1–2%) of nonsynonymous mutations in canonical CH driver genes, supporting the view that driver SNVs are selected, not chemotherapy-caused.
- 10/21 (47.6%) driver mutations in tMN WGS were not detected at prechemotherapy time points; none were in platinum/melphalan trinucleotide contexts, further arguing they were selected, not chemotherapy-introduced.
- Among all chemo-signature-positive tMN with SBS-MM1, 6/6 non-reinfused cases had TP53 disruption vs 2/10 (20%) reinfused cases (Fisher P = .007), indicating TP53 loss may enable survival of direct myeloablative chemotherapy exposure.

**Copy number and structural variation:**
- tMN with chemotherapy-induced mutagenesis showed significantly more complex SVs (chromothripsis, chromoplexy) than tMN without chemo signatures or de novo AML (Wilcoxon P < .001).
- Chromothripsis was the most frequent complex event: 8/39 (20.5%) tMN cases. Notably, chromothripsis involving chr19p13.2 with SMARCA4 focal amplification was found in 5/8 chromothripsis tMN (4/5 in chemo-signature-positive cases).
- SMARCA4 amplification was found in 1/316 de novo AML (Fisher P < .001; FDR < .001) — a striking tMN-specific event. Functional testing confirmed SMARCA4 overexpression confers cytokine-independent growth (P < .0001).
- tMN with chemo signatures held the majority of significant arm-level and focal CNAs vs tMN-no-chemo-sig and de novo AML (7 arm + 1 focal amplification; 7 arm + 11 focal loss regions; FDR < 0.1).

**Chemotherapy signatures as temporal barcodes:**
- In 8 tMN with large CNAs amenable to barcoding, melphalan or platinum signatures were detectable within duplicated clonal mutations in all cases — proving chromosomal gains were acquired post-chemotherapy.
- In 3 patients exposed to both agents, barcoding distinguished platinum vs melphalan timing of individual CNAs.
- Among the 6 non-reinfused SBS-MM1-positive tMN, all had TP53 involvement and post-chemotherapy CNA acquisition, suggesting that TP53 disruption precedes or enables mutagenic therapy survival.
- For 2 post-platinum MM cases, platinum signatures appeared only in subclonal (non-duplicated) mutations, consistent with platinum exposure occurring after the chromosomal gain events that define MM — validating the barcoding logic in the opposite direction.

## Relevance

**Direct relevance to h08 (agnostic covariate→signature-exposure association):**

This paper establishes several positive-control reference points for hypothesis h08's recovery arm (H08a):

1. **Platinum signatures (SBS31/SBS35) have 100% penetrance** in patients with confirmed platinum exposure and sufficient latency for single-cell expansion. This makes them ideal positive controls for H08a's signature-to-exposure recovery: within a cross-study cohort, any study with platinum-treated hematologic patients should yield detectable SBS31/SBS35-to-platinum associations.

2. **SBS-MM1 (melphalan)** shows incomplete penetrance (7/17 cases) due to the leukapheresis escape mechanism. This is a cautionary note for h08: the covariate "melphalan exposure" will be a noisy predictor of SBS-MM1 in any cohort that includes ASCT patients, because ~60% of melphalan-exposed cases will lack the signature. The effect-size ranking in an agnostic scan may therefore underestimate the true melphalan→SBS-MM1 link.

3. **Therapeutic context shapes mutational signature spectrum in AML/tMN.** The dichotomy between chemo-mutagenized and non-mutagenized tMN maps directly onto the h08 framework: a per-sample covariate (treatment history, here melphalan/platinum vs non-mutagenic agents) explains a large fraction of inter-sample variance in SBS exposure. This is precisely the kind of variance the h08 association layer aims to capture — though in this paper it requires curated treatment records, not an agnostic scan.

4. **Structural context matters for signature interpretation.** The finding that driver mutations in tMN are selected (not chemotherapy-induced) while the structural complexity (chromothripsis, CNAs) is chemotherapy-driven illustrates that signature exposures can be mechanistically decoupled from driver selection. For h08, this means signature-exposure associations may reflect mutagenesis without necessarily revealing which clone was selected — a nuance relevant to the reverse-causation guard (R2) in the hypothesis.

**Broader pipeline relevance:**
- This paper is a strong empirical anchor for the **hematologic malignancy arm** of h08's positive controls. The cBioPortal cross-study pipeline likely includes multiple tMN/AML/lymphoma studies where platinum- and melphalan-treated patients appear. If the per-study treatment metadata is available (e.g., via clinical tables), the SBS31/SBS35/SBS-MM1 associations are recoverable in principle.
- The cohort's use of the **single-cell expansion model** (chemotherapy signatures only detectable after clonal dominance of an exposed single cell) is relevant to the cBioPortal pipeline's panel-sequencing limitation (q018): targeted panels will miss sub-clonal signatures, which is why this study required WGS.
- The demonstration that **chromothripsis and complex SVs are enriched in chemo-mutagenized tMN** is relevant to t081/t092 (hypermutator annotation): high structural complexity may co-occur with, but is mechanistically distinct from, hypermutation driven by MMR loss or POLE. The pipeline's hypermutator annotation currently handles TMB/POLE/MSI but not complex SV-based hypermutators; this paper illustrates the gap.

## Project Framework Mapping

| Paper Concept | Project Concept | Notes |
|---|---|---|
| SBS31 / SBS35 (platinum intercalation) | Known positive-control signatures for h08 H08a | Complete penetrance makes these ideal test cases |
| SBS-MM1 (melphalan alkylation) | Positive control with incomplete penetrance | ~41% penetrance in melphalan-exposed; leukapheresis escape dilutes association |
| SBS-HSC / SBS1 (clock-like, hematopoietic) | Clock-like background (SBS1/SBS5 in h08) | tMN baseline; analogous to TCGA MC3 AML background |
| Chemo-mutagenized vs non-mutagenized tMN dichotomy | Hypermutator stratification (t081) | Chemo-mutagenized tMN are hypermutated vs de novo AML; distinct from POLE/MSI hypermutators |
| Single-cell expansion model | Panel vs WGS constraint (q018) | Signature detectable only after clonal dominance; panels miss sub-clonal events |
| Leukapheresis escape | Study-level matched-normal configuration | Matched-normal design affects whether clonal escape events are captured |
| Chemotherapy signatures as temporal barcodes | Mutation timing / clonal evolution | Method independent of clock-based molecular time; validates prior SBS5-based timing |

## Limitations

- Small cohort (39 tMN WGS, 40 samples from 39 patients) limits power for driver-gene frequency comparisons between subgroups. Authors acknowledge this explicitly for the SMARCA4/TP53 associations.
- WGS cost means the study cannot definitively address risk at the individual patient level; prospective cohorts with treatment records are needed to quantify who will develop tMN from a given CH variant.
- The temporal barcoding approach for CNAs cannot time deletions (no duplication logic available for copy-loss events) — a stated limitation.
- tMN without chemotherapy signatures are included but their primary malignancies varied (notably 2 B-ALL among the MM cohort), making the "escape" group heterogeneous.
- Treatment records are curated manually; ascertainment of chemotherapy type may be incomplete for the imported public datasets (21 tMN from dbGaP/EGAD).
- The functional SMARCA4 result uses a Ba/F3 murine cell-line model; whether SMARCA4 amplification is oncogenically sufficient in human AML cells is not established here.

## Follow-up

- Bolton et al. 2020 (Nat. Genet.): the post-platinum CH cohort used for driver-gene signature attribution in Figure 3A — foundational companion for interpreting platinum's mutagenic contribution to CH drivers.
- Maura et al. 2019 (Nat. Commun.): SBS5-based molecular timing in MM; methodological predecessor for the chromosomal gain timing validation.
- Rustad et al. 2020 (Nat. Commun.): timing the initiation of myeloma via SBS5; used here to anchor the MRCA timing.
- Degasperi et al. 2022 (Nat. Cancer): practical framework for mutational signature analysis — the workflow used in this study for signature attribution.
- Sperling et al. 2022 (Blood): lenalidomide promotes tMN development in TP53-mutant CH — directly relevant to the TP53 + non-mutagenic therapy route identified here.

**Questions this raises for the project:**
- Does the cBioPortal cross-study pipeline have access to treatment history (agent type) in clinical tables for AML/MDS/tMN studies? If so, the SBS31/SBS35 positive control could be run within-study on a subset of those studies.
- Are post-ASCT hematologic malignancy studies (e.g., myeloma relapse studies) in the cBioPortal corpus? These would be exactly the cases where SBS-MM1 should appear in WGS-based datasets but not panel-based ones — useful for calibrating the panel adequacy question in q018.
- The leukapheresis escape mechanism means "melphalan-exposed" is a noisy treatment covariate. Does the h08 agnostic scan need to account for treatment-subgroup heterogeneity within a study, or is the between-study variance sufficient?
