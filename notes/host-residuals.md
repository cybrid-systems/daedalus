# Host Residuals — Daedalus

Issues that are packaging / host / environment related, **not** denseness failures
on \(S_{\mathrm{Daedalus}}\).

| Date | Issue | Upstream | Status | Notes |
|------|-------|----------|--------|-------|
| 2026-08-11 | Float `/` returns `0` after intermediate arithmetic | [aura#2940](https://github.com/cybrid-systems/aura/issues/2940) **P0** | **fixed** | Was blocking dense GE; `daed:safe-div` workaround **removed** (2026-08-12). Solver uses native `/`. |
| 2026-08-11 | No `1e-9` scientific literals | [aura#2941](https://github.com/cybrid-systems/aura/issues/2941) **P2** | **fixed** | `1e3`, `1e-12`, etc. now OK in netlist/probe code. |
| 2026-08-11 | Export-before-require discipline | [aura#2766](https://github.com/cybrid-systems/aura/issues/2766) | fixed (prior) | Still follow export-before-require in span libs. |
| 2026-08-12 | `make-vector` rejects float length (incl. `floor` result); misleading `max_size()` error | [aura#2965](https://github.com/cybrid-systems/aura/issues/2965) **P1** | open | `floor(n)` is not `integer?`; `make-vector 5.0` / `(floor 10.0)` fail. **Workaround:** integer `nsteps` literals in `daed:simulate-tran`. |

## Daedalus workarounds still in force

1. **Form order in span libs**: always `(export …)` before `(require …)` when exports free-ref module cells ([aura#2766](https://github.com/cybrid-systems/aura/issues/2766)).
2. **Prefer `let*`** over internal `define` for dependent values in probes (host internal-define ≈ simultaneous letrec).
3. **Integer vector lengths**: do not pass `floor`/`/` results to `make-vector`; use integer literals (`.tran` API takes `nsteps` int).
4. **Runner**:
   ```bash
   export AURA_BIN   # visible to children if multi-process later
   export AURA_PATH="$AURA_LIB:$DAEDALUS_LIB"
   export AURA_SANDBOX=off
   export AURA_PIPELINE_STRICT=0
   ```
5. Host expects program on **stdin** (`aura < file.aura`), not argv path.
