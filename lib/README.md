# lib/ — Daedalus core (pure Aura preferred)

## Landed

| Module | Phase | Role |
|--------|-------|------|
| `daedalus-min.aura` | 0–5 | Facade: version + metrology + re-exports (`daed:*`) |
| `netlist.aura` | 1–5 / M0 | Circuit ADT (`R`/`C`/`L`/`V`/`I`/`D`/`Q`/`E`/`G`/`F`/`H`) |
| `stamp.aura` | 1–2 / M0 | MNA stamp: DC + BE + controlled sources |
| `devices.aura` | 5 | Shockley diode + Ebers-Moll NPN + NR residual/Jacobian |
| `solve.aura` | 1 / 5 / M0 / M1 | Dense GE + linear `.op` + NR (line-search, hist, gmin) |
| `tran.aura` | 2 / 5 / M0 / M2 | Fixed-step BE `.tran` + LTE adaptive step control |
| `probe.aura` | 1–2 | Node voltage / series query |
| `mutate-circuit.aura` | 3–5 / M0 | Value + topology mutate; circuit snapshot (incl. D/Q / E–H) |
| `agent.aura` | 4 | O→D→M→V→R loop + auto-tune |
| `viz.aura` | issue #1 | Netlist → self-contained HTML/SVG + edit-back apply |
| `ir.aura` | issue #6 | `daedalus-ir/1` + unit parse + `IR → circuit` |
| `validate.aura` | issue #6 | Static topology / semantic issues |
| `repair.aura` | issue #6 | Snapshot-guarded repair operators + loop |
| `vision.aura` | issue #6 | `from-ir` / `from-image` (fixture; VLM is an escape) |

```scheme
(require "daedalus-min" all:)
; daed:min-version => 5

(define ckt
  (daed:circuit "divider"
    (list (daed:V "vin" 1 0 5.0)
          (daed:R "r1" 1 2 1e3)
          (daed:R "r2" 2 0 2e3))))

;; Agent: tune R2 so v2 → 2.5 V
(define tune
  (daed:autotune! ckt 2 2.5 0.05 "r2" 20 "scale" "r1" 5.0))
(daed:tune-reached? tune)

;; Visualization (issue #1)
(define op (daed:simulate-op ckt))
(write-file "out.html" (daed:circuit->html ckt op))
(daed:apply-viz-edits! ckt (list (list "r2" 1e3)))

;; Phase 5: Shockley diode + Ebers-Moll NPN (Newton-Raphson .op)
(define dckt
  (daed:circuit "diode"
    (list (daed:V "vin" 1 0 5.0)
          (daed:R "r1" 1 2 1e3)
          (daed:D "d1" 2 0))))
(define dop (daed:simulate-op dckt))
(daed:v dop 2)   ; ≈ 0.7 V
(daed:op-iters dop)

;; Issue #6: IR → repair → simulate (no live VLM)
(define pipe (daed:from-ir (daed:ir-ex-divider) 8))
(daed:pipe-ok? pipe)
(daed:from-image "fixtures/divider.svg")
```

Host resolution: `scripts/run-aura.sh` sets `AURA_PATH` to `../aura-grok/lib:./lib`.

## Discipline

- Form order: `(export …)` before `(require …)` when needed (#2766).
- Prefer **flat** control flow in large multi-export modules (deep `if`/`let` nests have bitten host export/paren paths).
- Prefix: `daed:` for public bindings.
- Dual rollback: `daed:snapshot` / `daed:restore!` (circuit + stats); agent step uses circuit-only restore.
- Host `ast:snapshot` best-effort (often `-1` — aura#2966).
- Every critical-path leave from \(V_A\) → `notes/escape-log.md`.
