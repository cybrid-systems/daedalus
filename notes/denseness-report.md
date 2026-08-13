# Denseness Report — Daedalus

**Date:** 2026-08-13  
**Status:** **Phase 5 + M0–M4** — probes **00–03, 05–25** PASS; core \(E=0\). Live VLM extract and live ngspice are optional host oracles.  
**Judgment:** **strong on P0 slice + educational nonlinear + fixture vision path** — linear DC/tran, mutate, agent, diode/BJT NR, IR/repair, and matched-T ngspice compare hold. Live photo accuracy remains a product loop, not a denseness blocker.

**Theory:** [span-design.md](span-design.md) · repo [README.md](../README.md)  
**Prior spans:** Aether / Hephaestus / Hermes / Prometheus denseness reports (siblings)

---

## Claim (target)

\[
P \approx A \oplus E,\quad A \in V_A
\]

On \(S_{\mathrm{Daedalus}}\) the evolvable core  
(description → simulate → observe → decide → safe-mutate → verify → rollback)  
should remain predominantly pure Aura. Escapes are rare, metered, and logged.

| In scope (P0 target) | Out of scope (P0) |
|----------------------|-------------------|
| Netlist FlatAST (R, C, L, V, I) | Full BSIM / commercial models |
| Linear `.op`, fixed-step `.tran` | Schematic UI, mixed-signal |
| Safe mutate + snapshot/rollback | Production sparse solvers |
| Agent closed loop on parameters | Full multi-agent orch product |
| ≥3 denseness probes | |

---

## Constructive evidence

| Probe | Axes | Result | Core \(E\) | Edge \(E\) |
|-------|------|--------|------------|------------|
| [00](../examples/00-smoke/) | scaffolding | **PASS** | 0 | 0 |
| [01](../examples/01-voltage-divider/) | circuit `.op` | **PASS** | 0 | 0 |
| [02](../examples/02-rc-lowpass/) | `.op` + `.tran` | **PASS** | 0 | 0 |
| [03](../examples/03-mutate-resistor/) | mutate + dual rollback | **PASS** | 0 | 0 |
| [05](../examples/05-agent-autotune/) | O→D→M→V→R | **PASS** | 0 | 0 |
| [06](../examples/06-viz-bidirectional/) | netlist ↔ HTML (issue #1) | **PASS** | 0 | 0 |
| [07](../examples/07-diode-op/) | Shockley + NR `.op` | **PASS** | 0 | 0 |
| [08](../examples/08-bjt-ce/) | Ebers-Moll CE / switch | **PASS** | 0 | 0 |
| [09](../examples/09-diode-clamp-tran/) | BE+NR nonlinear `.tran` | **PASS** | 0 | 0 |
| [10](../examples/10-vision-pipeline/) | IR → repair → simulate (issue #6) | **PASS** | 0 | 0 |
| [11](../examples/11-controlled-sources/) | E/G/F/H stamp (issue #12) | **PASS** | 0 | 0 |
| [12](../examples/12-linear-op-suite/) | linear `.op` vs hand calc (issue #13) | **PASS** | 0 | 0 |
| [13](../examples/13-tran-suite/) | RC/RL/RLC `.tran` (issue #14) | **PASS** | 0 | 0 |
| [14](../examples/14-mutate-rollback/) | mutate + snapshot/rollback (issue #15) | **PASS** | 0 | 0 |
| [15](../examples/15-nr-helpers/) | NR helpers (issue #16) | **PASS** | 0 | 0 |
| [16](../examples/16-nl-op-suite/) | nonlinear `.op` vs ngspice (issue #17) | **PASS** | 0 | 0 |
| [17](../examples/17-adapt-tran/) | LTE adaptive `.tran` (issue #18) | **PASS** | 0 | 0 |
| [18](../examples/18-mosfet/) | Level-1 NMOS (issue #19) | **PASS** | 0 | 0 |
| [19](../examples/19-measure/) | `.measure` + CSV (issue #20) | **PASS** | 0 | 0 |
| [20](../examples/20-converge-aids/) | Gmin / source / ptran (issue #21) | **PASS** | 0 | 0 |
| [21](../examples/21-step-temp/) | `.step` + temperature (issue #22) | **PASS** | 0 | 0 |
| [22](../examples/22-monte-carlo/) | Monte Carlo + yield (issue #23) | **PASS** | 0 | 0 |
| [23](../examples/23-agent-evolve/) | spec-driven agent search (issue #24) | **PASS** | 0 | 0 |
| [24](../examples/24-topo-mutate/) | topology mutate + family search (issue #25) | **PASS** | 0 | 0 |
| [25](../examples/25-spice-export/) | FlatAST → SPICE export (issue #26) | **PASS** | 0 | 0 |

### Phase 1–2 narrative

- Linear MNA `.op` + fixed-step BE `.tran` in pure Aura (native `/`, sci literals post #2940/#2941; `nsteps` via `as-int` post #2965).

### Phase 3 narrative

- `mutate-circuit` + dual `daed:snapshot` / `restore!` (circuit clone + denseness metrics).
- Host `ast:snapshot` often `-1` offline ([aura#2966](https://github.com/cybrid-systems/aura/issues/2966)); circuit-domain rollback is pure Aura.

### Phase 4 narrative

- `agent.aura`: `daed:loop-once` / `daed:autotune!` — observe → decide → circuit snapshot → mutate → re-sim → verify → rollback.
- Compose **pattern** with Aether (O→D→M→V→R); circuit-domain data, not workspace `mutate:rebind`.
- Probe 05: refuse `R≤0`; rollback worsen; iterative scale to \(v_2\approx 2.5\); analytic one-shot \(R_2=R_1\); skip when within tol; escapes=0.

### Phase 5 narrative (issue #2)

- `devices.aura`: Shockley diode + Ebers-Moll NPN with `pnjlim` voltage limiting and gmin.
- Dense Newton-Raphson on the existing GE kernel; linear circuits keep the one-shot path (probes 01/02 unchanged).
- Probe 07: forward \(V_d \approx 0.7\,\mathrm{V}\), reverse \(I \approx 0\), mutate \(I_s\) + rollback.
- Probe 08: NPN switch on/off, CE mid-rail bias, inverting small-signal polarity, mutate \(\beta_F\).
- Probe 09: RC + shunt diode clamps a step; BJT inverter `.tran` settles into saturation.

### Issue #6 narrative (vision pipeline)

- `daedalus-ir/1` + `ir->circuit` / `circuit->ir`; static validator; rule-based repair with snapshot/rollback.
- `from-image` is fixture-first. Live VLM (`scripts/extract-ir.py`) is a logged host escape, not on the probe path.
- Probe 10: 5 clean IRs simulate; ≥10 broken IRs diagnosed; ≥7/10 seeded repairs recover; fixture `from-image`; escapes=0.

---

### Issue #16 narrative (NR helpers)

- Line-search damps the Newton step when residual would increase (\(\lambda=1,1/2,1/4,1/8\)).
- Initial guesses: zero (default), previous solution (`simulate-op-from`), Gmin ramp fallback (`simulate-op-gmin`).
- Failures report residual history, iteration count, failed node, and a reason string — not silent NaN.
- Probe 15: diode + rectifier cold-start `.op`, previous-guess fewer iters, gap-circuit diagnostics; probes 07–09 unchanged.

### Issue #17 narrative (nonlinear vs ngspice)

- Probe 16: diode bias, series D+R, rectifier DC, BJT CE vs frozen ngspice 45.2
  numbers at matched \(T\) (\(V_t \approx 26\,\mathrm{mV}\)).
- Bounds: 2 mV / 50 µA (CE 5 mV). Typical \|Δ\| is tens of µV.
- Default 27 °C ngspice shift is a **model** difference (frozen \(V_t\)), documented
  in [nl-op-compare.md](nl-op-compare.md). Live ngspice is optional
  (`scripts/compare-ngspice.sh`), not on the Aura path.

### Issue #18 narrative (adaptive .tran)

- `daed:simulate-tran-adapt`: Backward-Euler LTE, grow/shrink with reject, min/max dt.
- First step skips LTE (no \(\dot x\)); later `err = (h/2)|\dot x_n-\dot x_{n-1}| / (\mathrm{reltol}|x|+\mathrm{abstol})`.
- Probe 17: RC `dt` at the edge is ≪ flat-tail `dt`; `v(τ)` / `v(5τ)` match analytic and a fine fixed-step; fast RC and diode clamp finish. Fixed-step path unchanged.

### Issue #19 narrative (Level-1 MOSFET)

- `daed:M` / `daed:M*`: Shichman-Hodges NMOS (cutoff / linear / sat), bulk=source.
- Jacobian `gm`/`gds` on the existing NR kernel; optional constant `Cgs`/`Cgd` on `.tran`.
- `Kp`, `W`, `L`, `Vto`, `λ` are mutable. Probe 18: inverter off/on vs hand calc, CS mid-rail, Vto mutate+restore, adaptive switched-load `.tran`.

### Issue #20 narrative (`.measure` + CSV)

- `measure.aura`: MAX / MIN / AVG / RMS (trapezoidal), WHEN rising-cross, TRIG/TARG delay and 10–90 % rise.
- `daed:tran->csv` / `write-tran-csv!` for plotters; `daed:measure-summary` for agents.
- Probe 19: RC final / WHEN 2.5 V / rise time vs analytic; CSV header `t,v1,v2`.

### Issue #21 narrative (convergence aids)

- `daed:simulate-op-aid` tries `none → gmin-step → source-step → gmin-dev → ptran`.
- Gmin-to-ground stepping repairs empty DC rows (floating C / MOSFET gate).
- Source stepping ramps V/I 0.2→1; ptran adds grounded C then a final DC NR.
- `daed:op-aid` / `aid-steps` / `aid-tried` are queryable. Cold `simulate-op` unchanged.

### Issue #22 narrative (`.step` + temperature)

- `step-lin` / `step-log` / `step-list`; `sweep-op`, `sweep-tran`, `sweep-op-2`, `sweep-temp-op`.
- `daed:set-temp!` scales D/Q `Is` (SPICE XTI=3, EG=1.11) and `Vt=kT/q`; MOSFET `Vto` at −2 mV/°C. At `T=Tnom` scale=1.
- Agent: `daed:sweep-best` picks the step closest to a target voltage.

### Issue #23 narrative (Monte Carlo)

- `mc.aura`: seeded Park-Miller `u01` / polar gauss; `dist-uniform` / `dist-gauss` / `dist-rel`.
- `mc-op` / `mc-tran` run N trials, snap+restore, keep per-trial records + mean/std/min/max.
- `.tran` path collects a `.measure` metric (`final` / `max` / `min` / `avg` / `rms`).
- Agent: `mc-yield` and `mc-robust?` decide whether a spec window is hit often enough.

### Issue #24 narrative (agent evolve)

- `evolve.aura`: `spec-v` / `spec-when` / `spec-risetime` / `spec-final` plus `eval-spec`.
- `evolve!` is O→D→M→V→R: hill-climb or scale-toward-target; each commit is a good snapshot.
- Agent: `evo-restore-good!` rewinds to any intermediate good; `evo-replay!` reproduces the log.
- Probe 23: CE `Vc=2.5 V ± 2 %`; RC `WHEN 2.5 V ≈ τ ln 2`.

### Issue #25 narrative (topology mutate)

- `topo.aura`: add/remove, series-R insert/undo, parallel C/R, tap, compensation C.
- `topology-ok?` rejects invalid graphs (dup name, `R≤0`, F/H dangling ctrl); snap+restore on fail.
- `restore-circuit!` now replaces the component list so add/remove rolls back.
- `topo-search!` tries a family of ops from the origin snapshot and keeps the best spec.

### Issue #26 narrative (SPICE export)

- `spice.aura`: `circuit->spice` / `circuit->spice-tran` emit a deterministic ngspice deck.
- Models carry `IS`/`N`/`BF`/`VTO`/`KP`. `T=Tnom` maps to `tnom=temp=28.555` (Vt match).
- Probe 25: divider + agent-tuned R2 + D/Q/M models + write `out/*.cir`.
- Live `scripts/roundtrip-spice.sh` is an optional host oracle (same class as #17).

## Judgment

> On the **P0 Daedalus slice** (linear `.op`, fixed-step `.tran`, parameter mutate, agent auto-tune), \(V_A\) is **practically dense** for the evolvable core (core \(E=0\), probes 00–03 and 05 PASS).  
> Phase 5 extends that claim to **educational nonlinear** circuits (diode + NPN + NR) with core \(E=0\) (probes 07–09 PASS). Remaining growth is product depth (topology search, multi-agent, commercial models) — not a denseness blocker for the stated P0/P1 educational claim.

---

## Next (post-M4)

1. Milestone 5 — native C++ kernel escape ([#28](https://github.com/cybrid-systems/daedalus/issues/28)–#34); see [roadmap.md](roadmap.md)
2. Optional Aether `orch:*` multi-agent compose
3. PNP / LED defaults / simple astable as further educational coverage
4. Keep [escape-log.md](escape-log.md) / [host-residuals.md](host-residuals.md) current
