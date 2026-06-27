---
type: discussion
title: h08b gate handling after inconclusive H08a and smoking repair
status: active
created: '2026-06-01'
updated: '2026-06-01'
id: discussion:0005-h08b-gate-handling
source_refs:
- task:t199
- task:t200
- task:t204
related:
- task:t205
- task:t182
- task:t204
- hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
- pre-registration:0003-h08-positive-control-agnostic-association-must-recover-known-signature
- pre-registration:0004-h08-smoking-arm-repair-repaired-smoking-covariate-must-recover-sbs4
- method:h08-agnostic-association-model
focus_type: hypothesis
focus_ref: hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and
mode: standard
---

# Discussion: H08b gate handling after H08a

## Focus

This note records how the project treats H08b after the locked H08a positive-control read and the repaired smoking-arm rerun.
The decision is needed because H08a did not pass, but the APOBEC arm was strong enough that exploratory follow-up remains scientifically useful.

Primary evidence is in `doc/interpretations/2026-05-31-t199-h08-association-verdict.md`, `doc/interpretations/2026-06-01-h08-within-tissue-diagnostics.md`, and `doc/interpretations/2026-06-01-h08-smoking-repair.md`.

## Current Position

The locked H08a verdict remains `[?]`.
The t199 positive-control scan passed 1 of 3 registered arms: APOBEC passed, while UV and smoking missed.
The t200 diagnostic attributed the misses to weak environmental proxies and burden/saturation effects, not to a total collapse of the association machinery.
The t204 repaired smoking-arm rerun strengthened the smoking signal directionally, but it still failed the repaired rank gate: `ever_smoker` ranked 5 of 8 against SBS4 in pooled LUAD+LUSC.

Therefore no confirmatory H08b gate is open.
The original pre-registration required at least 2 of 3 H08a arms to pass before H08b discovery could be treated as promoted, confirmatory work.
Neither the diagnostic probe nor the repaired smoking rerun changes that locked condition.

## Critical Analysis

The tempting over-read is to say that because APOBEC passed cleanly, expression-module discovery should proceed as if H08a succeeded.
That would erase the point of the positive-control gate.
H08a was designed to test whether the agnostic association machinery recovers known aetiology links across multiple substrate types, not only a direct molecular-expression substrate.

The opposite over-read is to shut down H08b entirely.
That is also too strong.
The current evidence says the method is substrate-sensitive: it works best where the covariate is a direct molecular measurement, and it is weaker where the covariate is a noisy clinical proxy for lifetime environmental exposure.
That pattern is directly relevant to H08b, whose flagship target is expression-module association with SBS40/SBS5.
It licenses exploratory prototyping, not hypothesis promotion.

## Decision

H08b may proceed only as **exploratory/prototype** work until a future gate is explicitly pre-registered and passes.

The practical rules are:

- Do not describe H08b output as confirmatory evidence for `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and`.
- Do not use H08b results to update H08a.
- Do not treat a discovered SBS40/SBS5 expression-module hit as upstream causal evidence without the causal-direction guard from `question:0025`.
- Label `task:t182` outputs as exploratory discovery prototypes.
- Require a separate pre-registration before any H08b result is used for hypothesis promotion.

This is not a bypass of the H08a gate.
It is a scoped continuation under lower evidential weight.

## Evidence Needed

To promote H08b beyond exploratory status, the project needs one of two evidence routes.

First, a new repaired positive-control gate could be pre-registered and passed.
That gate would need to address both the current UV proxy failure and the lung SBS4 burden-dominance problem rather than repairing smoking alone.

Second, an H08b-specific pre-registration could define a lower evidential claim that does not depend on H08a promotion.
That would need explicit negative controls, age and tissue conditioning, reverse-causation guards, and a replication requirement before any upstream-cause language.

Neither condition is met today.

## Prioritized Follow-Ups

| Priority | Action | Why now |
|---|---|---|
| P2 | Keep `task:t182` exploratory if run next | It tests feasibility without weakening the H08a gate. |
| P2 | Preserve the locked H08a and repaired smoking verdicts as `[?]` | The repaired signal is positive but not top-3. |
| P3 | Defer a repaired gate until a better UV substrate is available | Smoking-only repair did not produce a sufficient positive-control pass. |

## Implications

The next defensible H08b action is a small t182 prototype focused on whether the existing substrate can separate SBS40 from SBS5 after age and tissue conditioning.
The expected deliverable is a feasibility/triage note, not a promotion verdict.

UV repair remains deferred unless a better UV exposure substrate appears.
A future repaired positive-control gate would need to address both the UV proxy problem and the lung SBS4 burden-dominance problem before it could unlock confirmatory H08b.

## Synthesis

The `hypothesis:0007-agnostic-covariate-association-recovers-known-signature-aetiologies-and` program remains useful but not promoted.
The current evidence supports a disciplined exploratory path: learn whether the expression-module machinery can produce coherent SBS40/SBS5 candidates, while keeping the hypothesis-promotion boundary intact.
This preserves the value of the APOBEC success without letting a single strong arm override the failed positive-control gate.
