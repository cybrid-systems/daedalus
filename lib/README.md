# lib/ — Daedalus core (pure Aura preferred)

## Landed

| Module | Phase | Role |
|--------|-------|------|
| `daedalus-min.aura` | 0–1 | Facade: version + metrology + re-exports (`daed:*`) |
| `netlist.aura` | 1 | Circuit / component ADT (`R`, `V`; node 0 = GND) |
| `stamp.aura` | 1 | Linear MNA stamping (dense `A x = b`) |
| `solve.aura` | 1 | Dense GE + `daed:simulate-op` (`.op`) |
| `probe.aura` | 1 | Node voltage query (`daed:v`) |

```scheme
(require "daedalus-min" all:)
; daed:min-version => 1  (Phase 1 linear .op)

(define ckt
  (daed:circuit "divider"
    (list (daed:V "vin" 1 0 5.0)
          (daed:R "r1" 1 2 1e3)
          (daed:R "r2" 2 0 2e3))))

(define res (daed:simulate-op ckt))
(daed:v res 2)  ; ≈ 3.333
```

Host resolution: `scripts/run-aura.sh` sets `AURA_PATH` to `../aura-grok/lib:./lib`.

## Planned (Phase 2+)

| Module | Role |
|--------|------|
| `tran.aura` | Fixed-step transient (C, L companion models) |
| `mutate-circuit.aura` | Circuit-specific safe mutation helpers |

## Discipline

- Form order: `(export …)` before `(require …)` when needed (#2766).
- Prefix: `daed:` for public bindings.
- Solver uses native `/` and scientific literals (post aura#2940 / #2941).
- Every critical-path leave from \(V_A\) → `notes/escape-log.md`.
