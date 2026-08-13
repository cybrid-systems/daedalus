# 17-adapt-tran

**Milestone 2 / issue #18** — LTE adaptive Backward-Euler `.tran`.

| Case | What happens |
|------|----------------|
| RC vs analytic | Adaptive `v(τ)` / `v(5τ)` within 5 % / 3 % of \(5(1-e^{-t/τ})\) |
| vs fine fixed | Same points within 3 % of `dt=τ/200` fixed-step |
| Step size | `dt` at the rising edge is < ½ of `dt` in the flat tail (`t>2τ`) |
| Fast RC | `τ=1 µs`, `tstop=50 µs` finishes; `v_end≈Vin`; no dt collapse |
| Clamp | Nonlinear diode+RC adaptive `.tran` settles near 0.7 V |

Fixed-step `daed:simulate-tran` is unchanged (probes 02 / 09 / 13). Adaptive is `daed:simulate-tran-adapt`. Query a time with `daed:tran-v-at-t`. Diagnostics: `tran-accepted`, `tran-rejected`, `tran-dthist`, `tran-lte`.

## Run

```bash
./scripts/run-aura.sh examples/17-adapt-tran/main.aura
```
