# SPEC — daedalus-core

## Goal

Implement a **minimally complete, agent-evolvable SPICE-style circuit simulation core** on Aura, serving as the concrete denseness probe for the Daedalus span.

## P0 Requirements

### Netlist
- Nodes identified by integer or symbol (0 = GND)
- Components: at least `R`, `C`, `L`, independent `V` / `I`, controlled `E`/`G`/`F`/`H`
- Representation is a FlatAST-friendly structure that supports `mutate:rebind`, `mutate:splice`, `mutate:replace-subtree`
- Topological integrity must be preserved across mutations (no dangling nodes)

### Analyses
- `.op` — DC operating point (required)
- `.tran` — fixed-step transient (required)
- Results returned as queryable structures (node voltages, time series)

### Solver (Hephaestus-style)
- Modified Nodal Analysis (MNA) stamping
- Newton-Raphson for nonlinear systems (linear first is acceptable)
- Critical numerical paths may use metered escapes; all such escapes must appear in the escape log

### Agent Loop (Aether-style)
```
load → simulate → observe (voltages, residual, convergence)
     → decide → safe-mutate → re-simulate → verify → rollback-if-needed
```
Must use `ast:snapshot` / `ast:restore`.

### Denseness Metrics
- escape rate
- rollback success rate
- post-mutation correctness
- pure-Aura fraction of the hot path

## Success Criteria (Phase 1)
1. Voltage divider and RC low-pass produce correct `.op` / `.tran` results
2. Agent mutation of a resistor value yields the expected new voltages
3. ≥ 3 denseness probes pass
4. No unlogged critical escapes

## Non-Goals (P0)
Full device models (BSIM etc.), commercial sparse solvers, schematic UI, mixed-signal.

## Interface Sketch
```scheme
(define ckt
  (circuit "divider"
    (V "vin" 1 0 5.0)
    (R "r1" 1 2 1e3)
    (R "r2" 2 0 2e3)))

(define res (simulate ckt '(.op)))
;; → (hash 'v1 5.0 'v2 ≈3.333)

(ast:snapshot "pre")
;; mutate parameter or topology
(simulate ckt '(.op))
```

## Status
- [x] SPEC frozen (Phase 0 scaffolding; interface sketch accepted for P0)
- [x] Repo scaffolding (scripts, `daedalus-min`, probe 00-smoke)
- [x] Netlist ADT + stamp skeleton (`netlist.aura`, `stamp.aura`)
- [x] Linear `.op` (`solve.aura`, `probe.aura`, denseness probe 01)
- [x] Fixed-step `.tran` (C/L BE companions, `tran.aura`, denseness probe 02)
- [x] Safe parameter mutate + dual snapshot/rollback (`mutate-circuit.aura`, probe 03)
- [x] Agent closed-loop auto-tune (`agent.aura`, probe 05)
- [x] Nonlinear devices + Newton-Raphson (Shockley D, Ebers-Moll Q, probes 07–09; issue #2)
- [x] denseness probe 01
- [x] denseness probe 02
- [x] denseness probe 03
- [x] denseness probe 05
- [x] denseness probe 07 (diode `.op`)
- [x] denseness probe 08 (BJT switch + CE `.op`)
- [x] denseness probe 09 (diode clamp + BJT switch `.tran`)
- [x] Vision → IR → repair → simulate (`ir`/`validate`/`repair`/`vision`, probe 10; issue #6)
- [x] Controlled sources E/G/F/H + query (issue #12, probe 11)
- [x] Linear `.op` suite + branch currents + snapshot (issue #13, probe 12)
- [x] Fixed-step `.tran` RC/RL/RLC + mutate re-run (issue #14, probe 13)
- [x] Agent mutate + snapshot (circuit/metrics/.op) + topology reconnect (issue #15, probe 14)
