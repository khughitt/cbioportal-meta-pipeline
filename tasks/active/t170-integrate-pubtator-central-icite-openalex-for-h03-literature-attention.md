---
id: t170
project: ''
title: Integrate PubTator Central + iCite + OpenAlex for h03 literature-attention
  regression
type: ''
aspects:
- computational-analysis
priority: P1
status: proposed
blocked_by: []
related:
- hypothesis:0003-gene-length-confounds-literature-attention
- question:0011-gene-length-as-literature-attention-confounder
- task:t129
- task:t130
- topic:mutation-rate-normalization
parent: ''
group: dataset-acquisition
artifacts: []
findings: []
created: '2026-04-28'
completed: null
---

t129 (the partial-slope regression for beta_length) and the broader h03 framing both depend on a robust literature-attention metric. PubMed mention count alone has known issues: it conflates primary research with reviews, treats every paper as equally weighted, and cannot disentangle gene-as-subject from gene-as-mention. Three sources together give a triangulated attention signal. (1) PubTator Central: NCBI's BioConcept-tagged corpus, gene-resolved at the entity level (resolves the gene-as-subject problem; provides per-gene primary-research vs review counts). (2) iCite (NIH OPA): per-paper citation counts and the Relative Citation Ratio, lets us weight mentions by paper-level impact and citation-window stability. (3) OpenAlex: independent corpus with author-affiliation and topic metadata, useful as an orthogonal validation of PubTator counts (does the PubTator-derived beta_length replicate against an independently-built corpus?). All three are free public APIs / bulk downloads. Pipeline integration scope: a code/scripts/build_gene_attention_features.py that joins gene HGNC symbol -> NCBI Entrez -> PubTator counts, OpenAlex topic counts, iCite RCR-weighted mentions, and emits gene_attention_features.feather. Acceptance: gene_attention_features.feather exists for all protein-coding genes with: pubtator_mention_count, pubtator_research_only, openalex_mention_count, icite_rcr_weighted_mentions, time-window subsets (pre-2010 / post-2010). t129 regression runs against this feather. PubTator-vs-OpenAlex correlation panel reported as a sanity check.
