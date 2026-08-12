# Denseness Report — Daedalus

**Date:** 2026-08-12  
**Status:** **Phase 4 agent closed loop** — probes **00–03, 05** PASS; pure-Aura MNA + BE + mutate + O→D→M→V→R, core \(E=0\).  
**Judgment:** **partial → strong on P0 slice** — linear DC, fixed-step transient, parameter mutate, and agent auto-tune denseness hold on the evolvable core. Full multi-agent / topology-search product claim remains out of P0.

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

### Phase 1–2 narrative

- Linear MNA `.op` + fixed-step BE `.tran` in pure Aura (native `/`, sci literals post #2940/#2941; `nsteps` via `as-int` post #2965).

### Phase 3 narrative

- `mutate-circuit` + dual `daed:snapshot` / `restore!` (circuit clone + denseness metrics).
- Host `ast:snapshot` often `-1` offline ([aura#2966](https://github.com/cybrid-systems/aura/issues/2966)); circuit-domain rollback is pure Aura.

### Phase 4 narrative

- `agent.aura`: `daed:loop-once` / `daed:autotune!` — observe → decide → circuit snapshot → mutate → re-sim → verify → rollback.
- Compose **pattern** with Aether (O→D→M→V→R); circuit-domain data, not workspace `mutate:rebind`.
- Probe 05: refuse `R≤0`; rollback worsen; iterative scale to \(v_2\approx 2.5\); analytic one-shot \(R_2=R_1\); skip when within tol; escapes=0.

---

## Judgment

> On the **P0 Daedalus slice** (linear `.op`, fixed-step `.tran`, parameter mutate, agent auto-tune), \(V_A\) is **practically dense** for the evolvable core (core \(E=0\), probes 00–03 and 05 PASS).  
> Remaining growth is product depth (topology search, multi-agent, nonlinear devices) — not a denseness blocker for the stated P0 claim.

---

## Next (post-P0)

1. Topology mutate denseness (insert/remove component under Hermes invariants)
2. Optional Aether `orch:*` multi-agent compose
3. Nonlinear devices / Newton (metered escapes if needed)
4. Keep [escape-log.md](escape-log.md) / [host-residuals.md](host-residuals.md) current
