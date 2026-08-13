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

**Phase 0–5 landed (P0 slice + educational nonlinear):**
- Scaffolding: scripts, denseness notes, `00-smoke`
- Circuit kernel: `netlist` / `stamp` / `devices` / `solve` / `tran` / `probe` / `mutate-circuit` / `agent` (`daed:min-version=5`)
- Probe `01-voltage-divider` — linear `.op`, \(v_2=10/3\), escapes=0
- Probe `02-rc-lowpass` — `.op` + fixed-step BE `.tran`, analytic RC checks, escapes=0
- Probe `03-mutate-resistor` — safe `daed:mutate!` + dual `daed:snapshot`/`restore!`, escapes=0
- Probe `05-agent-autotune` — O→D→M→V→R auto-tune to \(v_2=2.5\), escapes=0
- Probe `06-viz-bidirectional` — netlist ↔ HTML (issue #1 P0–P2), escapes=0
- Probe `07-diode-op` — Shockley + NR `.op`, escapes=0 (issue #2)
- Probe `08-bjt-ce` — Ebers-Moll switch + CE `.op`, escapes=0 (issue #2)
- Probe `09-diode-clamp-tran` — BE+NR nonlinear `.tran`, escapes=0 (issue #2)
- Probe `10-vision-pipeline` — IR → validate → repair → fixture `from-image`, escapes=0 (issue #6)
- Probe `11-controlled-sources` — E/G/F/H FlatAST + stamp, escapes=0 (issue #12)
- Probe `12-linear-op-suite` — divider / I-network / VCVS vs hand calc + snapshot, escapes=0 (issue #13)
- Probe `13-tran-suite` — RC/RL/RLC BE `.tran` + mutate re-run, escapes=0 (issue #14)
- Probe `14-mutate-rollback` — agent mutate + snapshot-sim + topology reconnect, escapes=0 (issue #15)
- Probe `15-nr-helpers` — NR line-search + previous guess + gmin + diagnostics, escapes=0 (issue #16)
- Probe `16-nl-op-suite` — nonlinear `.op` vs frozen ngspice refs, escapes=0 (issue #17)
- Probe `17-adapt-tran` — LTE adaptive BE `.tran`, escapes=0 (issue #18)
- Probe `18-mosfet` — Level-1 NMOS inverter / CS / adapt `.tran`, escapes=0 (issue #19)
- Probe `19-measure` — `.measure` + CSV waveform export, escapes=0 (issue #20)
- Probe `20-converge-aids` — Gmin / source / ptran fallbacks, escapes=0 (issue #21)
- Probe `21-step-temp` — `.step` + temperature sweep, escapes=0 (issue #22)
- Probe `22-monte-carlo` — Monte Carlo + yield, escapes=0 (issue #23)
- Probe `23-agent-evolve` — spec-driven agent search, escapes=0 (issue #24)
- Probe `24-topo-mutate` — topology add/remove/search, escapes=0 (issue #25)
- Probe `25-spice-export` — FlatAST → SPICE export, escapes=0 (issue #26)
- Probe `26-native-hotswap` — C++ GE hot-swap + fallback (issue #28); default backend stays pure
- Probe `27-ffi-bind` — `c-load` / `c-func` + structured failures (issue #30)
- Native ABI: `extern "C"` + workspace variant + CMake/g++ (`scripts/check-native-abi.sh`, issue #29)
- Solver: native `/`, sci literals; `.tran` via `daed:nsteps-for` / `daed:as-int` (aura#2965)
- Vision: do not trust VLM; fixtures + repair. Live extract is `scripts/extract-ir.py`.
- Roadmap: M0–M4 done (issue #27). M5 #28–#30 landed; #31–#34 remain.

**Post-M4:** M5 C++ hot-swap (metered); optional multi-agent compose, PNP / astable, richer viz.

## When generating or reviewing code

- Compose Aura surfaces (`mutate`, `query`, `ast:snapshot` / restore, …).
- Circuit-specific helpers live in `lib/` (`daed:*` prefix).
- Keep numerical escapes thin and metered (Hephaestus-style).
- Topology integrity after mutation (Hermes-style invariants).
- Prefer `let*` and export-before-require (#2766).

See `README.md`, `notes/span-design.md`, `projects/daedalus-core/SPEC.md`.
