# Denseness Report — Daedalus

**Date:** 2026-08-13  
**Status:** **Phase 5 + vision pipeline** — probes **00–03, 05–10** PASS; core \(E=0\). Live VLM extract is an optional logged host escape.  
**Judgment:** **strong on P0 slice + educational nonlinear + fixture vision path** — linear DC/tran, mutate, agent, diode/BJT NR, and IR/repair denseness hold. Live photo accuracy remains a product loop, not a denseness blocker.

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

## Judgment

> On the **P0 Daedalus slice** (linear `.op`, fixed-step `.tran`, parameter mutate, agent auto-tune), \(V_A\) is **practically dense** for the evolvable core (core \(E=0\), probes 00–03 and 05 PASS).  
> Phase 5 extends that claim to **educational nonlinear** circuits (diode + NPN + NR) with core \(E=0\) (probes 07–09 PASS). Remaining growth is product depth (topology search, multi-agent, commercial models) — not a denseness blocker for the stated P0/P1 educational claim.

---

## Next (post-P0 / post-P1)

1. Topology mutate denseness (insert/remove component under Hermes invariants)
2. Optional Aether `orch:*` multi-agent compose
3. PNP / LED defaults / simple astable as further educational coverage
4. Keep [escape-log.md](escape-log.md) / [host-residuals.md](host-residuals.md) current
