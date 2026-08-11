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
| 01 | voltage-divider | circuit `.op` | planned Phase 1 |
| 02 | rc-lowpass | `.tran` | planned Phase 2 |
| 03 | mutate-resistor | safe mutate + rollback | planned Phase 3 |
| 05 | agent-autotune | O→D→M→V→R | planned Phase 4 |

## Phase map

| Phase | Probes | Focus |
|-------|--------|--------|
| **0** | 00 | Scaffolding: scripts, lib facade, smoke |
| **1** | 01 | Linear MNA `.op` (R, V) |
| **2** | 02 | Fixed-step `.tran` (C, L) |
| **3** | 03+ | Parameter/topology mutate + snapshot |
| **4** | 05 | Agent closed-loop denseness |
