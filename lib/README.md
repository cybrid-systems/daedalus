# lib/ — Daedalus core (pure Aura preferred)

## Landed

| Module | Phase | Role |
|--------|-------|------|
| `daedalus-min.aura` | 0–2 | Facade: version + metrology + re-exports (`daed:*`) |
| `netlist.aura` | 1–2 | Circuit ADT (`R`/`C`/`L`/`V`/`I`; node 0 = GND) |
| `stamp.aura` | 1–2 | MNA stamp: DC + BE companions for `.tran` |
| `solve.aura` | 1 | Dense GE + `daed:simulate-op` |
| `tran.aura` | 2 | Fixed-step Backward Euler `.tran` |
| `probe.aura` | 1–2 | Node voltage / series query |

```scheme
(require "daedalus-min" all:)
; daed:min-version => 2

(define ckt
  (daed:circuit "rc-lp"
    (list (daed:V "vin" 1 0 5.0)
          (daed:R "r1" 1 2 1e3)
          (daed:C "c1" 2 0 1e-6))))

(define op (daed:simulate-op ckt))
(daed:v op 2)  ; DC: 5.0 (C open)

;; Fixed-step .tran: integer nsteps (make-vector needs int length)
(define tr (daed:simulate-tran ckt 1e-5 500))
(daed:tran-v-at tr 2 100)  ; ≈ v(τ)
```

Host resolution: `scripts/run-aura.sh` sets `AURA_PATH` to `../aura-grok/lib:./lib`.

## Planned (Phase 3+)

| Module | Role |
|--------|------|
| `mutate-circuit.aura` | Circuit-specific safe mutation helpers |

## Discipline

- Form order: `(export …)` before `(require …)` when needed (#2766).
- Prefix: `daed:` for public bindings.
- Solver uses native `/` and scientific literals (post aura#2940 / #2941).
- `.tran` takes **integer** `nsteps` — host `make-vector` rejects float lengths.
- Every critical-path leave from \(V_A\) → `notes/escape-log.md`.
