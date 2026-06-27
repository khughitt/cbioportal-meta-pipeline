# Variant annotation — best-practices guide

*As-of: 2026-04-13*

This guide codifies the audit checklist for code that **annotates somatic variants** with
functional / clinical / hotspot information — primarily via OncoKB, Cancer Gene Census, Cancer
Hotspots, and the upstream annotation pipelines (Genome Nexus, VEP, Oncotator). For driver-gene-
level overlay see `driver-detection.md`.

The interpretive backbone is `topic:variant-interpretation-oncokb-vus`.

## Sources

**Foundational papers:**

- Chakravarty D, et al. 2017. "OncoKB: A Precision Oncology Knowledge Base." *JCO Precis Oncol*
  2017:PO.17.00011. PMID 28890946.
  → OncoKB structure: variant-level oncogenicity calls + tumor-type-specific therapy tiers.
- Suehnholz SP, et al. 2024. "Quantifying the Expanding Landscape of Clinical Actionability for
  Patients with Cancer." *Cancer Discov*. PMID 37849038.
  → OncoKB version-drift quantification: Level 1/2 actionability 8.9% (2017) → 31.6% (2022) on
  the *same* MSK-IMPACT cohort. Mandates version-stamping.
- Tate JG, et al. 2019. "COSMIC: the Catalogue Of Somatic Mutations In Cancer." *Nucleic Acids
  Res* 47:941-947. PMID 30371878. → Cancer Gene Census Tier 1 + Tier 2.
- Cerami E, et al. 2012. "The cBio cancer genomics portal." *Cancer Discov* 2:401–404. PMID
  22588877. → cBioPortal's annotation conventions, including Oncotator canonical-isoform
  filtering applied to all incoming MAFs.

**Tooling:**
- OncoKB API + CSV downloads at `oncokb.org` (free for academia; account required; monthly
  versioned releases).
- COSMIC CGC at `cancer.sanger.ac.uk/cosmic/download` (free for academia; account required).
- Cancer Hotspots at `github.com/taylor-lab/hotspots`.
- 3D Hotspots at `3dhotspots.org`.
- Genome Nexus at `genomenexus.org` — MSK-curated annotation aggregator (VEP + custom).

## Audit checklist

| ID | Item | Applicability | Settled? | Evidence expected |
|---|---|---|---|---|
| annot.01 | OncoKB / CGC / Bailey catalog version stamped on annotated outputs | any annotated output | settled | catalog version (snapshot date, release tag, file checksum) recorded per annotation column |
| annot.02 | OncoKB tier interpretation is tumor-type-aware | per-(variant, cancer) annotation | settled | OncoKB tier assignment uses the patient's specific cancer type; pooled "Level 1 across all cancers" not reported |
| annot.03 | "Functional" / "actionable" % carries explicit catalog-version qualifier | any "% functional" / "% actionable" output | settled | output text or column metadata names the catalog snapshot used |
| annot.04 | Absence-from-OncoKB is not interpreted as benignity | any per-variant filter or annotation | settled | scripts handling VUS-equivalent variants document this explicitly; no implicit "not in OncoKB → benign" filter |
| annot.05 | Oncotator canonical-isoform filter (applied upstream by cBioPortal) is documented as a known restriction | any aggregation that depends on per-variant calls | settled | script header notes that non-canonical-isoform-only mutations are silently excluded from cBioPortal-fed summaries (per Cerami 2012 [@Cerami2012] / Gao 2013 [@Gao2013]) |
| annot.06 | Hotspot annotations from both 1D (Chang 2016 [@Chang2016]) and 3D (Gao 2017 [@Gao2017]) catalogs applied | per-mutation outputs | contested | both `is_1d_hotspot` and `is_3d_cluster_residue` columns; the two are largely disjoint (~3% overlap per Gao 2017 [@Gao2017]) and both add value |
| annot.07 | Catalog refresh cadence documented | any pipeline using a versioned catalog | settled | per-catalog refresh cadence (OncoKB monthly; CGC per-release; Bailey 2018 [@Bailey2018] static; Hotspots static) noted in pipeline docs |
| annot.08 | Pre-annotated cBioPortal MAFs are version-tracked | any ingestion of cBioPortal data | settled | cBioPortal study version / data-release tag noted; substantial re-annotation events flagged |
| annot.09 | OncoKB API rate-limit / authentication handled | any pipeline making OncoKB API calls | settled | API key + rate-limit handling in script; offline batch annotation preferred where possible |
| annot.10 | Two-source consensus annotations preferred over single-source | any "is X a driver / known cancer gene / functional variant" annotation | contested | Bailey ∧ CGC consensus, OncoKB ∧ Hotspots consensus, etc. — single-source annotations flagged as exploratory |

## Common pitfalls

- **Treating OncoKB-Level-1 as time-invariant.** Per Suehnholz 2024 [@Suehnholz2024], the Level 1 fraction of a
  fixed cohort tripled in 5 years. Always pin the OncoKB version.
- **"Not in OncoKB" interpreted as "not functional."** OncoKB is curated, not exhaustive. A
  variant absent from OncoKB may be: uncurated, recently curated and not yet in the local
  annotation snapshot, or genuinely VUS. Don't infer benignity.
- **Pooling OncoKB tier across cancers.** A KRAS G12C mutation is OncoKB Level 1 in NSCLC
  (sotorasib) but Level 3B in CRC. Pan-cancer "% Level 1" hides this.
- **Re-annotating per-variant against current OncoKB API without version-stamping.** Outputs
  become non-reproducible: re-running tomorrow gives different numbers if OncoKB updated. Pin to
  a snapshot.
- **Inheriting Oncotator's canonical-isoform filter without realizing it.** cBioPortal-fed MAFs
  silently exclude non-canonical-isoform-only mutations. If your downstream analysis cares about
  alternative isoforms, this is invisible to you unless you note it.
