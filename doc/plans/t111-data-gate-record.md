# t111 data-access gate record

- **Task:** t111 — Extract per-tissue normal-tissue 96-trinucleotide reference spectra
- **Gate run date:** 2026-04-19
- **Outcome:** MIXED — Li2021 Branch A (public), Xu2025 Branch B (dbGaP controlled access)

---

## Step 1: Li2021 per-variant calls

**Source verified:** Nature Supplementary Table 3, published with DOI 10.1038/s41586-021-03836-1

**URL:**
```
https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-021-03836-1/MediaObjects/41586_2021_3836_MOESM5_ESM.xlsx
```

**Filename:** `41586_2021_3836_MOESM5_ESM.xlsx` (Springer Nature supplementary MOESM5)

**Retrieval date:** 2026-04-19

**File size for `paper:Li2021` / `task:t111`:** 6.3 MB

**SHA256:** `6276deb0f16ad45871347ca3e705907384a4d66d0eb40833be18b0a853d837a2`

**Content confirmed:**
- Sheet "Sheet1" = "Supplementary Table 3: Somatic mutations detected in exome sequencing (coding regions)"
- Sheet "Sheet2" = additional data (not inspected in detail)
- Row count: 66,191 rows in Sheet1 (including 3 header rows = ~66,188 variant rows)
- **Column schema (row 3 header):** `sampleID, chr, pos, ref, mut, gene, strand, ref_cod, mut_cod, ref3_cod, mut3_cod, aachange, ntchange, codonsub, impact, ref_count, alt_count`
- Sample ID encoding: `PN{donor}{tissue_code}-{layer}-{biopsy}`, e.g. `PN1C-1-1` = donor PN1, Colon, layer 1, biopsy 1
- First data row example: `PN1C-1-1, 15, 102261414, T, C, TARSL2, -1, A, G, CAT, CGT, I161V, A481G, ATC>GTC, Missense, 13, 3`
- Covers 5 donors (PN1, PN2, PN7, PN8, PN9) × 9 organs (bronchus, esophagus, cardia, stomach, duodenum, colon, rectum, liver, pancreas)
- Assembly: GRCh37/hg19 (per Methods)
- **Access status: OPEN — no login or DAC required**

**Notes:**
- The `ref` and `mut` columns map to `ref`/`alt` in MAF/VCF convention (single-base SNVs)
- This is exome coding-region data only; non-coding SNVs used for signature extraction were NOT deposited in the supplement (only available via EGA EGAD00001007859, which is controlled access FASTQ)
- The bioRxiv preprint (PRJCA003552/GSA) deposited raw FASTQs only; the coding-variant table was added to the Nature paper supplement
- Raw sequencing data (WES + WGS FASTQs): EGA EGAD00001007859 — controlled access, DAC approval required (EGAC00001002218)

---

## Step 2: Xu2025 per-variant calls

**Source checked:** bioRxiv supplement for DOI 10.1101/2025.01.07.631808 (PMC11741334)

**Supplementary file URL:**
```
https://www.biorxiv.org/content/biorxiv/early/2025/01/09/2025.01.07.631808/DC1/embed/media-1.docx?download=true
```

**Filename:** `media-1.docx` (`supplements/631808_file08.docx` as listed on bioRxiv)

**Retrieval date:** 2026-04-19

**File size for `paper:Xu2025` / `task:t111`:** 2.3 MB

**SHA256:** `16f8e04d7e082e926d7b9e5df3b497499910f97ab8202bd07bf994505a5aaf38`

**Content confirmed (docx parsed):**
- Table S1: "Information of the 14 GTEx donors studied" — donor metadata only (Donor, Age, Sex, Num Tissues Sequenced, Total Coverage, Num SMs Discovered)
- Table S2: "Mutational signatures detected in our data"
- Supplementary Figures S1–S4: figure legends only
- **NO per-variant mutation call table** (no chrom/pos/ref/alt rows)

**Data availability statement for `paper:Xu2025` / `task:t111` (verbatim from PMC full text):**
> "All protected mapped data of 265 GTEx samples have been deposited at the database of Genotypes and Phenotypes (dbGaP) and are publicly available as of the date of publication. The accession number is listed in the key resources table."

**Key resources table entry:**
> Deposited data: dbGaP: phs000424.v7; https://gtexportal.org/home/protectedDataAccess

**Access status: CONTROLLED — dbGaP phs000424.v7 (GTEx protected access)**
- phs000424.v7 is the existing GTEx v7 protected-access dataset (BAM files)
- Access requires: dbGaP Data Access Request (DAR), institutional sign-off, and GTEx Data Use Agreement
- The per-variant mSOMA calls themselves are NOT separately deposited as open-access supplementary data

---

## Step 3: Branch decision

**Outcome: MIXED**

| Source | Branch | Reason |
|--------|--------|--------|
| Li2021 | **A** | Per-variant coding SNV table (Supp Table 3, MOESM5) is publicly downloadable from Nature Springer CDN with no authentication |
| Xu2025 | **B** | Per-variant calls are not in the supplement; underlying data is dbGaP phs000424.v7 (controlled access, DAR required) |

**Scope implications of Branch B for Xu2025:**
- The design assumed per-variant rows are in the bioRxiv supplement. They are not.
- To use Xu2025 data, options are:
  a. Apply for dbGaP access to phs000424.v7 (GTEx v7 exome BAMs), re-run mSOMA, extract per-variant calls — significant DUA/compute overhead
  b. Request the per-variant call table directly from the authors (Akey Lab, Princeton) — faster but not guaranteed
  c. Reduce t111 scope to Li2021 only for now; add Xu2025 as a follow-up task once access is resolved
  d. Identify an alternative open-access normal-tissue somatic mutation dataset covering ≥10 tissues

**Per the design §Data-access gate: halting. User decision required before proceeding to Task 1.**

---

## Step 4: What is available for Li2021 (Branch A staging notes for Task 16)

The publicly downloadable file to stage to `data/` at Task 16 is:

```
URL:      https://static-content.springer.com/esm/art%3A10.1038%2Fs41586-021-03836-1/MediaObjects/41586_2021_3836_MOESM5_ESM.xlsx
Filename: li2021_supp_table3_somatic_mutations.xlsx  (rename on staging)
SHA256:   6276deb0f16ad45871347ca3e705907384a4d66d0eb40833be18b0a853d837a2
Rows:     ~66,188 variant rows (Sheet1 only; Sheet2 contents not confirmed)
Assembly: GRCh37
Schema:   sampleID, chr, pos, ref, mut, gene, strand, ref_cod, mut_cod,
          ref3_cod, mut3_cod, aachange, ntchange, codonsub, impact,
          ref_count, alt_count
```

**Caveats for t111 pipeline:**
1. This table covers **coding SNVs only** (exome, coding regions). Non-coding SNVs used by the authors for signature extraction via HDP are NOT included. Downstream spectra computed from this table will be exome-coding-only; this is acceptable for SBS96 if the consumer is aware.
2. The `chr` column uses bare integer/X/Y notation (not `chr`-prefixed), consistent with GRCh37 convention.
3. The `mut` column is the alt allele (equivalent to `ALT` in VCF). The design's input contract uses `ref`/`alt`; map `mut` → `alt` at ingest.
4. No `donor_id` column exists; donor is encoded in the first part of `sampleID` (e.g., `PN1` in `PN1C-1-1`). The tissue code is the letter immediately following the donor (C=Colon, E=Esophagus, B=Bronchus, D=Duodenum, R=Rectum, L=Liver, P=Pancreas, S=Stomach, Ca=Cardia — confirm full mapping against Supplementary Table 1).
