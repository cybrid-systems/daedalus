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
