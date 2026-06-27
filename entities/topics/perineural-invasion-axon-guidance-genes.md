---
type: topic
title: "Perineural invasion, peripheral nerve\u2013tumor interaction, and large axon-guidance/adhesion\
  \ genes"
status: active
created: '2026-06-06'
updated: '2026-06-06'
id: topic:perineural-invasion-axon-guidance-genes
ontology_terms:
- perineural invasion
- axon guidance
- cell adhesion molecule
- peripheral nervous system
- gene length
- Schwann cell
source_refs:
- paper:Lu2026
- paper:Fan2024
- paper:Cortese2020
- paper:Xiong2023
- paper:Zhang2025
related:
- hypothesis:0012-neural-gene-enrichment-length-histology-artifact
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0032-neural-gene-length-null
- question:0033-neural-enrichment-cns-exclusion
- synthesis:0015-cancer-neuroscience-literature-batch-21-papers-does-it-explain-a-neural
---

# Perineural invasion, peripheral nerve–tumor interaction, and large axon-guidance/adhesion genes

## Scope

Perineural invasion (PNI) and how peripheral (non-CNS) tumors recruit/co-opt nerves. Focused
review: `paper:Lu2026` (PNI mechanisms); per-cancer-type peripheral nerve dependence:
`paper:Fan2024`; PNS-immune interface: `paper:Cortese2020`; brain→peripheral-tumor circuit:
`paper:Xiong2023`.

## Why this topic is the most directly relevant to the candidate-gene question

The PNI / axon-guidance machinery includes the **large IgCAM / adhesion / guidance genes** that
structurally resemble the project's candidate list:

- PNI actors named in the literature: **L1CAM, NCAM1, SLIT2, ROBO1/2, SEMA3A/3D, PLXNB1/D1,
  GDNF/RET, NGF/NTRK1, GAP43** — all large genes.
- The project's candidates **LSAMP** and **OPCML** are GPI-anchored IgCAMs in the *same family*
  as L1CAM/NCAM1, but `paper:Lu2026` does **not** cite them as PNI actors — they are brain-
  expressed and recurrent in glioma. Their appearance is, per the Lu2026 reviewer, "expected
  under length-proportional background mutation without any selection."

This makes PNI the sharpest setting to disentangle **H1 (selection on guidance genes)** from
**H5 (length)** and **H4 (CNS)**: PNI is cancer-type-structured (PDAC ~100%, prostate 25–90%,
HNSCC, CRC), so a *genuine* PNI-driven mutation signal would track PNI-prevalent cancer types,
whereas a length artifact would be flat across types and a CNS artifact would localize to glioma.

**SLIT2 is the cautionary example (`paper:Zhang2025`, Cell 2025):** in HNSCC, the axon-guidance
ligand SLIT2 drives an immune-escape circuit — but through **ATF4-dependent secretion
(expression)**, not somatic mutation. A long axon-guidance gene can be mechanistically central to
neuro-oncology while contributing *nothing* to a somatic-mutation ranking except length-scaled
passengers. This is exactly the dissociation `hypothesis:0012` predicts.

## Tests this topic feeds

- Gene-length null on candidate adhesion/guidance genes (`question:0032`).
- Cancer-type structure: do candidate-gene mutations co-vary with PNI-prevalent cancers vs
  flat/CNS? (`question:0033` and the plan's §3).
- Label-free PNS-vs-CNS partition of the neural score (`question:0035`) — Cortese2020's point
  that our candidates are CNS-structural, not PNS.

## External data lead

`paper:Lu2026` points to a pan-cancer PNI transcriptomic classifier (2,029 patients, 12 cancer
types) and a single-cell + spatial pancreatic neural-invasion dataset (Chen et al. 2025 Cancer
Cell) as label-free sources for a tumor-nerve-interface gene signature.

## Summary

This topic note is currently a concise project-facing record; the existing sections above carry the substantive synthesis until a fuller rewrite is warranted.

## Key Concepts

The key concepts are defined in the existing prose above and in the linked project entities; this section is present to keep the topic aligned with the current Science topic template.

## Current State of Knowledge

The current project-facing state of knowledge is summarized in the existing prose above. No additional confidence upgrade is made by this structural section.

## Relevance to This Project

This topic is relevant through the linked questions, hypotheses, datasets, and source references in the frontmatter and in the note above.

## Key References

Key references are listed in `source_refs` and cited in the note above.
