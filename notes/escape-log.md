# Escape Log — Daedalus

Every leave from pure Aura (\(V_A\)) on a circuit-critical path must be recorded here.

| Date | Location | Reason | Mechanism | Impact | Mitigation / Plan |
|------|----------|--------|-----------|--------|-------------------|
| — | — | *(none yet — Phase 0 pure scaffolding)* | — | — | — |

## Phase 0

No leave from \(V_A\). Scaffolding and metrology helpers are pure Aura.

## Phase 1

No leave from \(V_A\). Linear MNA stamp + dense GE (`.op`) are pure Aura.
(Historical: temporary `daed:safe-div` for aura#2940 was pure Aura, not an escape; removed after host fix.)

## Phase 2

No leave from \(V_A\). Fixed-step Backward Euler companions (C/L), current sources, and
`.tran` time-stepping are pure Aura.

## Phase 3

No leave from \(V_A\). Parameter mutate, topology guards, and dual snapshot/rollback
(circuit clone + denseness metrics) are pure Aura. Host `ast:snapshot` is best-effort
only (often returns `-1` offline); circuit-domain rollback does not depend on it.

## Phase 4

No leave from \(V_A\). Agent O→D→M→V→R (`loop-once` / `autotune!`) uses pure-Aura
observe, propose, mutate, and circuit-only rollback. Aether is composed as a **pattern**,
not as a required host rebind path.

## Issue #1 (viz)

No leave from \(V_A\). `circuit->html` / `apply-viz-edits!` are pure Aura string build +
safe mutate. Browser edit-back uses exported JSON/form; live HTTP/postMessage transport
is optional product glue, not denseness core.

## Phase 5 / issue #2 (nonlinear)

No leave from \(V_A\). Shockley diode, Ebers-Moll NPN, dense Newton-Raphson (with
`pnjlim` + gmin), and BE+NR `.tran` are pure Aura on the existing dense GE kernel.

## Issue #6 (vision pipeline)

Core path (`ir` / `validate` / `repair` / `from-ir` / fixture `from-image`) stays
in \(V_A\). The optional live extractor `scripts/extract-ir.py` is a **metered
host escape** (xAI or MiniMax multimodal). Probes use fixtures only (`E=0`).

| Date | Location | Reason | Mechanism | Impact | Mitigation / Plan |
|------|----------|--------|-----------|--------|-------------------|
| 2026-08-13 | `scripts/extract-ir.py` | Schematic photo → IR | HTTP VLM (xAI default; MiniMax optional) | Offline probes do not call it | Fixture `from-image`; log every live call |

## Issue #12 (controlled sources)

No leave from \(V_A\). VCVS/VCCS/CCCS/CCVS stamps are pure Aura on the dense MNA kernel.

## Issue #13 (linear .op suite)

No leave from \(V_A\). Branch-current extract reads the existing MNA unknown
vector; comparison is hand calculation (optional ngspice decks are documentation).

## Issue #14 (fixed-step .tran suite)

No leave from \(V_A\). BE companions for C/L, inductor current series, and
mutate + re-`.tran` stay on the existing pure-Aura path.

## Issue #15 (mutate + snapshot/rollback)

No leave from \(V_A\). Value/topology mutate, solver-state snapshot, mutation
log, and dual rollback remain pure Aura. Host `ast:snapshot` is still best-effort.

## Issue #16 (NR convergence helpers)

No leave from \(V_A\). Line-search, previous-guess restart, Gmin ramp, and
residual / fail-node diagnostics stay on the existing dense NR + GE path.

## Issue #17 (nonlinear .op vs ngspice)

No leave from \(V_A\) on the probe path. Frozen ngspice numbers live in
`examples/16-nl-op-suite/ref/ngspice.tsv`. Live `ngspice -b` is an optional
host oracle (`scripts/compare-ngspice.sh`), same class as the #13 decks.

## Issue #18 (LTE adaptive .tran)

No leave from \(V_A\). Adaptive BE uses the existing companion stamp + dense
GE / NR. Fixed-step `simulate-tran` is unchanged.

## Issue #19 (Level-1 MOSFET)

No leave from \(V_A\). Shichman-Hodges stamp and Jacobian stay on the dense
NR + BE path. Parameters are ordinary FlatAST hash fields.

## Convention

- Prefer pure Aura on the evolvable circuit core (netlist, stamp, agent loop).
- Escapes on core paths are evidence *against* denseness until justified and isolated.
- Critical numerical escapes (e.g. sparse solvers later) must be thin, metered, and logged.
- Host / packaging residuals go to `host-residuals.md`, not here.
