# GROK.md — Living Prompt for Daedalus

You are assisting the Daedalus denseness probe for Aura Unify.

## Core Mission

Daedalus tests whether Aura’s native space \(V_A\) is practically dense on the
**circuit simulation + evolvable netlist** composition subspace:

\[
S_{\mathrm{Daedalus}} = \text{compose}(S_{\mathrm{Aether}}, S_{\mathrm{Hephaestus}}, S_{\mathrm{Prometheus}}, S_{\mathrm{Hermes}})
\]

projected onto analog circuit domain (SPICE-class).

Primary objects under test:
- Hierarchical, mutable netlists and device models (FlatAST)
- Numerical kernels (MNA stamp, solve, transient integration)
- Closed-loop agent evolution of topology / parameters / models
- Topological correctness and probe insertion
- Snapshot / rollback of circuit + denseness metrics

## Discipline (non-negotiable)

1. Prefer pure Aura on the evolvable circuit core.
2. Every leave from \(V_A\) on a critical path → record in `notes/escape-log.md`.
3. Probes must be runnable and regressable (`RESULT pass` / `RESULT fail`).
4. Dual rollback: semantic circuit state **and** denseness metrics.
5. **Compose** sibling spans; do not re-prove Aether / Hephaestus / Prometheus / Hermes.
6. P0 non-goals: full BSIM, commercial sparse solvers, schematic UI, mixed-signal.

## Current Status

**Phase 0 scaffolding landed:**
- `scripts/run-aura.sh`, `run-all.sh`, `check-structure.sh`
- `lib/daedalus-min.aura` (version 0 + metrology helpers)
- Probe `00-smoke` — host + lib load, escapes=0

**Next (Phase 1):** `netlist` / `stamp` / `solve` + `01-voltage-divider` linear `.op`.

## When generating or reviewing code

- Compose Aura surfaces (`mutate`, `query`, `ast:snapshot` / restore, …).
- Circuit-specific helpers live in `lib/` (`daed:*` prefix).
- Keep numerical escapes thin and metered (Hephaestus-style).
- Topology integrity after mutation (Hermes-style invariants).
- Prefer `let*` and export-before-require (#2766).

See `README.md`, `notes/span-design.md`, `projects/daedalus-core/SPEC.md`.
