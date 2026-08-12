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

**Phase 0–4 landed (P0 denseness slice):**
- Scaffolding: scripts, denseness notes, `00-smoke`
- Circuit kernel: `netlist` / `stamp` / `solve` / `tran` / `probe` / `mutate-circuit` / `agent` (`daed:min-version=4`)
- Probe `01-voltage-divider` — linear `.op`, \(v_2=10/3\), escapes=0
- Probe `02-rc-lowpass` — `.op` + fixed-step BE `.tran`, analytic RC checks, escapes=0
- Probe `03-mutate-resistor` — safe `daed:mutate!` + dual `daed:snapshot`/`restore!`, escapes=0
- Probe `05-agent-autotune` — O→D→M→V→R auto-tune to \(v_2=2.5\), escapes=0
- Solver: native `/`, sci literals; `.tran` via `daed:nsteps-for` / `daed:as-int` (aura#2965)

**Post-P0:** topology mutate, multi-agent compose, nonlinear devices (as needed).

## When generating or reviewing code

- Compose Aura surfaces (`mutate`, `query`, `ast:snapshot` / restore, …).
- Circuit-specific helpers live in `lib/` (`daed:*` prefix).
- Keep numerical escapes thin and metered (Hephaestus-style).
- Topology integrity after mutation (Hermes-style invariants).
- Prefer `let*` and export-before-require (#2766).

See `README.md`, `notes/span-design.md`, `projects/daedalus-core/SPEC.md`.
