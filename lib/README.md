# lib/ — Daedalus core (pure Aura preferred)

## Landed

| Module | Phase | Role |
|--------|-------|------|
| `daedalus-min.aura` | 0–4 | Facade: version + metrology + re-exports (`daed:*`) |
| `netlist.aura` | 1–2 | Circuit ADT (`R`/`C`/`L`/`V`/`I`; node 0 = GND) |
| `stamp.aura` | 1–2 | MNA stamp: DC + BE companions for `.tran` |
| `solve.aura` | 1 | Dense GE + `daed:simulate-op` |
| `tran.aura` | 2 | Fixed-step Backward Euler `.tran` |
| `probe.aura` | 1–2 | Node voltage / series query |
| `mutate-circuit.aura` | 3 | Safe parameter mutate + circuit snapshot |
| `agent.aura` | 4 | O→D→M→V→R loop + auto-tune |

```scheme
(require "daedalus-min" all:)
; daed:min-version => 4

(define ckt
  (daed:circuit "divider"
    (list (daed:V "vin" 1 0 5.0)
          (daed:R "r1" 1 2 1e3)
          (daed:R "r2" 2 0 2e3))))

;; Agent: tune R2 so v2 → 2.5 V
(define tune
  (daed:autotune! ckt 2 2.5 0.05 "r2" 20 "scale" "r1" 5.0))
(daed:tune-reached? tune)
```

Host resolution: `scripts/run-aura.sh` sets `AURA_PATH` to `../aura-grok/lib:./lib`.

## Discipline

- Form order: `(export …)` before `(require …)` when needed (#2766).
- Prefer **flat** control flow in large multi-export modules (deep `if`/`let` nests have bitten host export/paren paths).
- Prefix: `daed:` for public bindings.
- Dual rollback: `daed:snapshot` / `daed:restore!` (circuit + stats); agent step uses circuit-only restore.
- Host `ast:snapshot` best-effort (often `-1` — aura#2966).
- Every critical-path leave from \(V_A\) → `notes/escape-log.md`.
