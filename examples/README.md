# Daedalus Probes

Each probe is a self-contained denseness experiment on \(S_{\mathrm{Daedalus}}\).

## Conventions

- Directory: `examples/NN-short-name/` with `main.aura` + short `README.md`
- Run one: `./scripts/run-aura.sh examples/NN-short-name/main.aura`
- Full suite: `./scripts/run-all.sh`
- Structure only: `./scripts/check-structure.sh`
- Probes print `RESULT pass` / `RESULT fail` for `run-all.sh` grepping

## Probe index

| # | Name | Axes | Status |
|---|------|------|--------|
| 00 | [smoke](00-smoke/) | scaffolding | **PASS** (Phase 0) |
| 01 | [voltage-divider](01-voltage-divider/) | circuit `.op` | **PASS** (Phase 1) |
| 02 | [rc-lowpass](02-rc-lowpass/) | `.op` + `.tran` | **PASS** (Phase 2) |
| 03 | [mutate-resistor](03-mutate-resistor/) | safe mutate + dual rollback | **PASS** (Phase 3) |
| 05 | [agent-autotune](05-agent-autotune/) | O→D→M→V→R | **PASS** (Phase 4) |
| 06 | [viz-bidirectional](06-viz-bidirectional/) | netlist ↔ HTML | **PASS** (issue #1) |
| 07 | [diode-op](07-diode-op/) | Shockley + NR `.op` | **PASS** (Phase 5 / issue #2) |
| 08 | [bjt-ce](08-bjt-ce/) | Ebers-Moll CE / switch `.op` | **PASS** (Phase 5 / issue #2) |
| 09 | [diode-clamp-tran](09-diode-clamp-tran/) | BE+NR nonlinear `.tran` | **PASS** (Phase 5 / issue #2) |
| 10 | [vision-pipeline](10-vision-pipeline/) | IR → repair → simulate | **PASS** (issue #6) |
| 11 | [controlled-sources](11-controlled-sources/) | E/G/F/H stamp + query | **PASS** (issue #12 / M0) |
| 12 | [linear-op-suite](12-linear-op-suite/) | `.op` vs hand calc + snapshot | **PASS** (issue #13 / M0) |
| 13 | [tran-suite](13-tran-suite/) | RC / RL / RLC `.tran` | **PASS** (issue #14 / M0) |
| 14 | [mutate-rollback](14-mutate-rollback/) | mutate + snapshot/rollback | **PASS** (issue #15 / M0) |
| 15 | [nr-helpers](15-nr-helpers/) | NR line-search + guess + diagnostics | **PASS** (issue #16 / M1) |
| 16 | [nl-op-suite](16-nl-op-suite/) | nonlinear `.op` vs ngspice refs | **PASS** (issue #17 / M1) |
| 17 | [adapt-tran](17-adapt-tran/) | LTE adaptive `.tran` | **PASS** (issue #18 / M2) |
| 18 | [mosfet](18-mosfet/) | Level-1 NMOS `.op` + adapt `.tran` | **PASS** (issue #19 / M2) |
| 19 | [measure](19-measure/) | `.measure` + CSV export | **PASS** (issue #20 / M2) |
| 20 | [converge-aids](20-converge-aids/) | Gmin / source / ptran | **PASS** (issue #21 / M3) |
| 21 | [step-temp](21-step-temp/) | `.step` + temperature | **PASS** (issue #22 / M3) |
| 22 | [monte-carlo](22-monte-carlo/) | Monte Carlo + yield | **PASS** (issue #23 / M3) |
| 23 | [agent-evolve](23-agent-evolve/) | spec-driven agent search | **PASS** (issue #24 / M4) |

## Phase map

| Phase | Probes | Focus |
|-------|--------|--------|
| **0** | 00 | Scaffolding: scripts, lib facade, smoke |
| **1** | 01 | Linear MNA `.op` (R, V) |
| **2** | 02 | Fixed-step BE `.tran` (C, L, I) |
| **3** | 03 | Parameter mutate + dual snapshot/rollback |
| **4** | 05 | Agent closed-loop denseness |
| **viz** | 06 | Bidirectional netlist ↔ HTML (issue #1) |
| **5** | 07–09 | Shockley diode, Ebers-Moll NPN, Newton-Raphson (issue #2) |
| **viz-in** | 10 | Image/IR → validate → repair → simulate (issue #6) |
| **M0** | 11–14 | Netlist, `.op`, `.tran`, mutate/rollback (issues #12–#15) |
| **M1** | 15–16 | NR helpers + nonlinear `.op` vs ngspice (issues #16–#17) |
| **M2** | 17–19 | Adaptive `.tran`, MOSFET, `.measure` (issues #18–#20) |
| **M3** | 20–22 | Convergence aids + `.step` / temperature + Monte Carlo (issues #21–#23) |
| **M4** | 23 | Spec-driven agent parameter search (issue #24) |
