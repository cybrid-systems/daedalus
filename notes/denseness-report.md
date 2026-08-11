# Denseness Report — Daedalus

**Date:** 2026-08-11  
**Status:** **Phase 1 linear `.op`** — probes **00–01** PASS; pure-Aura MNA path, core \(E=0\).  
**Judgment:** partial — circuit description + linear DC solve denseness holds for the divider probe; full \(S_{\mathrm{Daedalus}}\) claim still requires `.tran`, mutate, and agent loop.

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
| ≥3 denseness probes | Full multi-agent orch product |

---

## Constructive evidence

| Probe | Axes | Result | Core \(E\) | Edge \(E\) |
|-------|------|--------|------------|------------|
| [00](../examples/00-smoke/) | scaffolding | **PASS** | 0 | 0 |
| [01](../examples/01-voltage-divider/) | circuit `.op` | **PASS** | 0 | 0 |
| 02 rc-lowpass | `.tran` | planned | — | — |
| 03 mutate-resistor | Aether compose | planned | — | — |

### Phase 1 narrative

- `netlist` / `stamp` / `solve` / `probe` implement linear MNA in pure Aura.
- Voltage divider analytic check: \(v_2 = 5 \cdot \frac{2000}{3000} = \frac{10}{3}\).
- Solver uses `daed:safe-div` (host residual workaround, still pure Aura — not an escape).

---

## Judgment

> On the **linear `.op` slice** of \(S_{\mathrm{Daedalus}}\), \(V_A\) is **practically dense** for the evolvable core (core \(E=0\)).  
> Full span claim waits for transient, safe mutation, and agent closed-loop probes.

---

## Next

1. Phase 2: `C`/`L` + fixed-step `.tran` + probe **02-rc-lowpass**
2. Phase 3: parameter mutate + snapshot/rollback
3. Keep escapes in [escape-log.md](escape-log.md); host issues in [host-residuals.md](host-residuals.md)
