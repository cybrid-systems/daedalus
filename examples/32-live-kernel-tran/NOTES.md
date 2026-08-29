# M6 live-kernel `.tran` — demo notes and file-agent contrast

Parent: [issue #35](https://github.com/cybrid-systems/daedalus/issues/35).
Probe: `examples/32-live-kernel-tran/` (issue text said “example 26”; 26–31
are M5 native probes).

## Why this is not #15 plus Copilot

| | #15 mutate-rollback | #18 adaptive `.tran` | #24 agent-evolve | #33 native `.op` swap | **#35 this probe** |
|---|---|---|---|---|---|
| What moves | A resistor / topology | Step size `h` | Spec search on **R** | Linear GE backend | **K1–K4 solver bindings** |
| When | Between full `.op` runs | Inside one `.tran` | Between full sims | Before / during `.op` | **While `.tran` is already running** |
| On failure | Restore circuit | Shrink `h` | Restore circuit | Restore backend | Restore **kernel only** |
| `t`, `v` | Re-sim from scratch | Advance | Re-sim from scratch | No transient cursor | **Stay at last accepted point** |
| Process | New `simulate-op` | One `simulate-tran-adapt` | New sim each try | Optional `.so` load | **One PID, no reload** |

#15 changes the netlist and re-solves. #18 adapts `h` inside a closed
integrator. #33 hot-swaps a linear `.op` kernel and may restart the solve.
This probe forbids killing the process, forbids `t = 0` replay, and forbids
treating a resistor edit as the demo.

## Contrast protocol

**A (allowed to cheat):** the same model edits a `.cir` / `.py` file, restarts
the process, integrates from `t = 0`. Expected: can match waveforms.
**Invalid** as an Aura substitute — it dropped `v` and the live Jacobian
identity.

**B (fair):** the same model, **forbidden** to kill the process or replay from
`t = 0`. It may only edit files on disk. Expected: cannot swap the Jacobian
assembler without dropping `v`, or must admit failure.

A file-diff agent has no handle on the in-process `assemble-jacobian` node
id. After a restart the audit row `t=1.20ms k1=` is gone.

## Six milestone gates

1. `hot-rebind-count >= 3` at `t > 0`; the next NR iteration uses the new binding.
2. After `nr-diverge` → kernel rollback: `t` unchanged and `||v - v_before||_∞ = 0`.
3. K1–K4 ids survive ≥30 mutate/rollback cycles (`id-drift` fails).
4. Query at `t = 1.20 ms` returns the K1 id + source digest that was live then.
5. One process / one PID; reload-netlist or exec is an automatic fail.
6. File-agent contrast B cannot complete the same script.

## Demo shot list

- Left: primitive stream (`query:binding` / `mutate:rebind` / `rollback`)
- Center: `v_out(t)` keeps moving; one red flash on `nr-diverge`
- Bottom: `t=1.20ms  k1=`
- No “reload netlist” line anywhere

## What M6 does **not** claim

- SPICE replacement or accuracy trophy vs ngspice (the RMSE is a ruler, bound
  5 % of pulse amplitude)
- FlashAttention-class / sparse / KLU kernels
- The M5 C++ `.so` as the protagonist (optional metered escape only)
- MOSFET/BSIM, topology search, or swapping BE→trapezoidal as the main demo

## Snapshot keys

| Key | Holds | On kernel rollback |
|---|---|---|
| `world:tran-cursor` | `t`, `v`, `v_prev`, accepted probes | **untouched** |
| `kernel:nr-be` | K1–K4 bindings | restored |

Host `ast:snapshot` is still often `-1` offline (aura#2966). The live kernel
slots are the circuit-domain analog of `query:binding` / `mutate:rebind`.

## ngspice ruler

Deck: `spice/clamp.cir`. Frozen samples: `ref/ngspice.tsv`.
Educational Shockley `IS=1e-14 N=1`, `T=TNOM=27`. Probe RMSE must stay
below 0.25 V (5 % of the 5 V pulse) against those samples.
