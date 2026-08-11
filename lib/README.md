# lib/ — Daedalus core (pure Aura preferred)

Planned modules:

- `netlist.aura`          — Circuit / Node / Component ADT + construction macros
- `stamp.aura`            — MNA stamp functions (R/C/L/V/I)
- `solve.aura`            — linear / non-linear solve entry points
- `tran.aura`             — transient stepping
- `probe.aura`            — result query and observation points
- `mutate-circuit.aura`   — circuit-specific safe mutation helpers (on top of Aether)

All modules are `require`-able and remain friendly to `query:*` / `mutate:*`.
