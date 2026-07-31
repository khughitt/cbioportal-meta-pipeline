---
id: t107
project: ''
title: Backport clustering.* defaults to main configs (config-10k-genes.yml, config-full.yml,
  config-pan-cancer.yml) OR make cluster rules opt-out when missing
type: ''
aspects:
- software-development
priority: P2
status: proposed
blocked_by: []
related:
- task:t100
parent: ''
group: pipeline
artifacts: []
findings: []
created: '2026-04-17'
completed: null
---

Surfaced by t100 PoC 2026-04-17: cluster_genes.py and cluster_cancer_types.py require config['clustering']['gene']['k'], ['gene_min_mutations'], ['cancer_min_mutations'], ['random_seed'] (and mirror keys under ['cancer']). No shipped config prior to config-poc.yml contained these keys. This means every run of the main pipeline prior to this PoC would have crashed at the cluster rules if rule all was fully evaluated — the pre-t081 runs presumably did not have cluster rules in their rule all target list. Fix: either (a) backport the default clustering sub-tree from config-poc.yml to the 3 main configs, or (b) make the cluster scripts fall back to sensible defaults when the key is absent (with a warning). Option (a) is more explicit; option (b) is more forgiving.

PARTIAL (backlog review 2026-06-01): `config-full.yml` now carries the `clustering:` block (gene/cancer k, min_mutations, random_seed); `config-10k-genes.yml` and `config-pan-cancer.yml` still lack it, and `cluster_genes.py`/`cluster_cancer_types.py` still hard-require the key (KeyError if absent). Remaining work: backport the block to the two missing configs, or add the script-level fallback.
