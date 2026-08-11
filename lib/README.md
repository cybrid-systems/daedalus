# lib/ — Daedalus core (pure Aura preferred)

## Landed

| Module | Phase | Role |
|--------|-------|------|
| `daedalus-min.aura` | 0 | Facade: version + baseline metrology (`daed:*`) |

```scheme
(require "daedalus-min" all:)
; daed:min-version => 0  (Phase 0 scaffolding)
```

Host resolution: `scripts/run-aura.sh` sets `AURA_PATH` to `../aura-grok/lib:./lib`.

## Planned (Phase 1+)

| Module | Role |
|--------|------|
| `netlist.aura` | Circuit / Node / Component ADT + construction macros |
| `stamp.aura` | MNA stamp functions (R/C/L/V/I) |
| `solve.aura` | linear / non-linear solve entry points |
| `tran.aura` | transient stepping |
| `probe.aura` | result query and observation points |
| `mutate-circuit.aura` | circuit-specific safe mutation helpers (on top of Aether) |

All modules are `require`-able and remain friendly to `query:*` / `mutate:*`.

## Discipline

- Form order: `(export …)` before `(require …)` when needed (#2766).
- Prefix: `daed:` for public bindings.
- Every critical-path leave from \(V_A\) → `notes/escape-log.md`.
