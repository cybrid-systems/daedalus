# Roadmap — M0 → M5

Living copy of [issue #27](https://github.com/cybrid-systems/daedalus/issues/27).
**Date:** 2026-08-14

Daedalus is a living laboratory: mutable FlatAST circuits, snapshot/rollback,
agent loops. Production accuracy stays with ngspice / LTspice via export (#26).
A thin C++ kernel escape is M5, not a replacement for the semantic layer.

**Suite:** 27/27 (25 probes + ngspice-compare + export-roundtrip), core \(E=0\).

| Milestone | Scope | Status |
|-----------|--------|--------|
| **M0** | P0 completion | **done** (#12–#15) |
| **M1** | Nonlinear DC | **done** (#2–#5, #16–#17) |
| **M2** | Transient + devices | **done** (#18–#20) |
| **M3** | Convergence & analysis | **done** (#21–#23) |
| **M4** | Agent-driven evolution | **done** (#24–#26) |
| **M5** | Native kernel escape | **slice landed** (parent #28, probe 26) |

## Milestone 0 – P0 Completion — done

- [x] [#12](https://github.com/cybrid-systems/daedalus/issues/12) FlatAST netlist R/C/L/V/I + E/G/F/H — probe 11
- [x] [#13](https://github.com/cybrid-systems/daedalus/issues/13) Linear `.op` suite — probe 12
- [x] [#14](https://github.com/cybrid-systems/daedalus/issues/14) Fixed-step `.tran` RC/RL/RLC — probe 13
- [x] [#15](https://github.com/cybrid-systems/daedalus/issues/15) Mutate + snapshot/rollback — probe 14

## Milestone 1 – Nonlinear DC Foundation — done

Related: #2 (Phase 5), #3 diode, #4 BJT, #5 Newton-Raphson.

- [x] [#16](https://github.com/cybrid-systems/daedalus/issues/16) NR helpers (line-search, guess, gmin) — probe 15
- [x] [#17](https://github.com/cybrid-systems/daedalus/issues/17) Nonlinear `.op` vs ngspice — probe 16

## Milestone 2 – Practical Transient + Devices — done

- [x] [#18](https://github.com/cybrid-systems/daedalus/issues/18) LTE adaptive `.tran` — probe 17
- [x] [#19](https://github.com/cybrid-systems/daedalus/issues/19) Level-1 NMOS — probe 18
- [x] [#20](https://github.com/cybrid-systems/daedalus/issues/20) `.measure` + CSV — probe 19

## Milestone 3 – Convergence & Analysis Tools — done

- [x] [#21](https://github.com/cybrid-systems/daedalus/issues/21) Gmin / source / ptran — probe 20
- [x] [#22](https://github.com/cybrid-systems/daedalus/issues/22) `.step` + temperature — probe 21
- [x] [#23](https://github.com/cybrid-systems/daedalus/issues/23) Monte Carlo + yield — probe 22

## Milestone 4 – Agent-Driven Circuit Evolution — done

- [x] [#24](https://github.com/cybrid-systems/daedalus/issues/24) Spec-driven agent search — probe 23
- [x] [#25](https://github.com/cybrid-systems/daedalus/issues/25) Topology mutation surface — probe 24
- [x] [#26](https://github.com/cybrid-systems/daedalus/issues/26) SPICE export for sign-off — probe 25

## Milestone 5 – Native Kernel Escape — slice landed (issue #28)

Parent: **[#28](https://github.com/cybrid-systems/daedalus/issues/28)** — probe 26.

The #28 success criteria are met (ABI, `c-load`, rebind-safe pattern, Opaque
copy, divider demo, optional dispatch). Sub-issues #29–#34 remain for
follow-up polish unless closed separately.

- [x] [#28](https://github.com/cybrid-systems/daedalus/issues/28) Parent success criteria — probe 26
- [ ] [#29](https://github.com/cybrid-systems/daedalus/issues/29) ABI + build conventions
- [ ] [#30](https://github.com/cybrid-systems/daedalus/issues/30) Aura FFI (`c-load` / `c-func`)
- [ ] [#31](https://github.com/cybrid-systems/daedalus/issues/31) Hephaestus wrapper + escape metering
- [ ] [#32](https://github.com/cybrid-systems/daedalus/issues/32) Buffer / Opaque exchange
- [ ] [#33](https://github.com/cybrid-systems/daedalus/issues/33) Pure → C++ hot-swap → rollback demo
- [ ] [#34](https://github.com/cybrid-systems/daedalus/issues/34) Optional native `.op` / Newton backend

Semantic layer stays pure Aura. Native calls are metered and rollback-safe.

## Strategy

Explore in Daedalus; sign off in ngspice/LTspice (#26). Speed, if needed, is a
metered C++ escape (M5), not a second circuit language.
