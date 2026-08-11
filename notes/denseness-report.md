# Denseness Report — Daedalus

**Date:** 2026-08-12  
**Status:** **Phase 2 fixed-step `.tran`** — probes **00–02** PASS; pure-Aura MNA + BE companions, core \(E=0\).  
**Judgment:** partial — linear DC and fixed-step transient denseness hold; full \(S_{\mathrm{Daedalus}}\) claim still requires mutate + agent loop.

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
| [02](../examples/02-rc-lowpass/) | `.op` + `.tran` | **PASS** | 0 | 0 |
| 03 mutate-resistor | Aether compose | planned | — | — |

### Phase 1 narrative

- `netlist` / `stamp` / `solve` / `probe` implement linear MNA in pure Aura.
- Voltage divider analytic check: \(v_2 = 5 \cdot \frac{2000}{3000} = \frac{10}{3}\).
- Dense GE uses native `/` and sci literals after [aura#2940](https://github.com/cybrid-systems/aura/issues/2940) / [#2941](https://github.com/cybrid-systems/aura/issues/2941).

### Phase 2 narrative

- Components `C`, `L`, `I`; DC treats C as open, L as 0 V short.
- Fixed-step Backward Euler companions for C/L; `daed:simulate-tran` with **integer** `nsteps`.
- RC low-pass: `.op` \(v_2=5\); `.tran` \(v_2(\tau)\) and \(v_2(5\tau)\) within relative tolerance of \(5(1-e^{-t/\tau})\).

---

## Judgment

> On the **linear `.op` + fixed-step `.tran` slice** of \(S_{\mathrm{Daedalus}}\), \(V_A\) is **practically dense** for the evolvable core (core \(E=0\)).  
> Full span claim waits for safe mutation and agent closed-loop probes (≥3 probes already pass: 00–02).

---

## Next

1. Phase 3: parameter mutate + snapshot/rollback + probe **03**
2. Phase 4: agent auto-tune closed loop
3. Keep escapes in [escape-log.md](escape-log.md); host issues in [host-residuals.md](host-residuals.md)
