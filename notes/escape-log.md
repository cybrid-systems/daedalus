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

## Convention

- Prefer pure Aura on the evolvable circuit core (netlist, stamp, agent loop).
- Escapes on core paths are evidence *against* denseness until justified and isolated.
- Critical numerical escapes (e.g. sparse solvers later) must be thin, metered, and logged.
- Host / packaging residuals go to `host-residuals.md`, not here.
