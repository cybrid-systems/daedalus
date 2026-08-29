# Roadmap — M0 → M6

Living copy of [issue #27](https://github.com/cybrid-systems/daedalus/issues/27)
plus [issue #35](https://github.com/cybrid-systems/daedalus/issues/35) (M6).
**Date:** 2026-08-29

Daedalus is a living laboratory: mutable FlatAST circuits, snapshot/rollback,
agent loops. Production accuracy stays with ngspice / LTspice via export (#26).
A thin C++ kernel escape is M5, not a replacement for the semantic layer.
M6 is the denseness claim Git+file agents cannot match: rebind the Jacobian
assembler mid-`.tran` without restarting or dropping `v`.

**Suite:** 35/35 (32 probes + ngspice-compare + export-roundtrip + check-native-abi), core \(E=0\) on the default pure backend.

| Milestone | Scope | Status |
|-----------|--------|--------|
| **M0** | P0 completion | **done** (#12–#15) |
| **M1** | Nonlinear DC | **done** (#2–#5, #16–#17) |
| **M2** | Transient + devices | **done** (#18–#20) |
| **M3** | Convergence & analysis | **done** (#21–#23) |
| **M4** | Agent-driven evolution | **done** (#24–#26) |
| **M5** | Native kernel escape | **done** (#28–#34, probes 26–31) |
| **M6** | Live kernel hot-swap during `.tran` | **done** (#35–#43, probe 32) |

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

## Milestone 5 – Native Kernel Escape — done (issues #28–#34)

Parent: **[#28](https://github.com/cybrid-systems/daedalus/issues/28)** — probe 26.

The #28 success criteria are met (ABI, `c-load`, rebind-safe pattern, Opaque
copy, divider demo, optional dispatch). #29–#31 record ABI, FFI, and the
Hephaestus rebind-safe wrapper, Opaque exchange, and the end-to-end
hot-swap demo, and optional native `.op` / Newton.

- [x] [#28](https://github.com/cybrid-systems/daedalus/issues/28) Parent success criteria — probe 26
- [x] [#29](https://github.com/cybrid-systems/daedalus/issues/29) ABI + build conventions
- [x] [#30](https://github.com/cybrid-systems/daedalus/issues/30) Aura FFI (`c-load` / `c-func`) — probe 27
- [x] [#31](https://github.com/cybrid-systems/daedalus/issues/31) Hephaestus wrapper + escape metering — probe 28
- [x] [#32](https://github.com/cybrid-systems/daedalus/issues/32) Buffer / Opaque exchange — probe 29
- [x] [#33](https://github.com/cybrid-systems/daedalus/issues/33) Pure → C++ hot-swap → rollback demo — probe 30
- [x] [#34](https://github.com/cybrid-systems/daedalus/issues/34) Optional native `.op` / Newton backend — probe 31

Semantic layer stays pure Aura. Native calls are metered and rollback-safe.

## Milestone 6 – Live kernel hot-swap during `.tran` — done (issues #35–#43)

Parent: **[#35](https://github.com/cybrid-systems/daedalus/issues/35)** — probe 32.

While a transient is already running, an agent rebinds the solver kernel
(not the netlist). The next BE+NR step uses the new bindings. If Newton
diverges, rollback restores **only the kernel**. Simulation time `t` and
the voltage vector `v` stay at the last accepted point. Audit answers
which `assemble-jacobian` was live at `t = 1.20 ms`.

Work lands in `lib/kernel.aura` + `examples/32-live-kernel-tran/`
(issue text said “example 26”; 26–31 were already M5).

- [x] [#36](https://github.com/cybrid-systems/daedalus/issues/36) Freeze PoC netlist + split world/kernel snapshot keys
- [x] [#37](https://github.com/cybrid-systems/daedalus/issues/37) Expose K1–K4 as stable live defines
- [x] [#38](https://github.com/cybrid-systems/daedalus/issues/38) BE+NR stepper: next-step uses new kernel; nr-diverge rolls back kernel only
- [x] [#39](https://github.com/cybrid-systems/daedalus/issues/39) Step audit log + time-travel query at t = 1.20 ms
- [x] [#40](https://github.com/cybrid-systems/daedalus/issues/40) Example `32-live-kernel-tran` + scripted mid-run perturbations
- [x] [#41](https://github.com/cybrid-systems/daedalus/issues/41) Bench gates: no-restart, id stability, ngspice RMSE ruler
- [x] [#42](https://github.com/cybrid-systems/daedalus/issues/42) Aether loop on example 32 (recorded policy)
- [x] [#43](https://github.com/cybrid-systems/daedalus/issues/43) File-agent contrast B + demo notes

Do not reopen #27. Contrast vs #15 / #18 / #24 / #33: see
`examples/32-live-kernel-tran/NOTES.md`.

## Strategy

Explore in Daedalus; sign off in ngspice/LTspice (#26). Speed, if needed, is a
metered C++ escape (M5), not a second circuit language.
