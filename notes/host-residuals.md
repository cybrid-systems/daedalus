# Host Residuals — Daedalus

Issues that are packaging / host / environment related, **not** denseness failures
on \(S_{\mathrm{Daedalus}}\).

| Date | Issue | Upstream | Status | Notes |
|------|-------|----------|--------|-------|
| 2026-08-11 | Float `/` returns `0` after intermediate arithmetic | [aura#2940](https://github.com/cybrid-systems/aura/issues/2940) **P0** | **fixed** | Was blocking dense GE; `daed:safe-div` workaround **removed** (2026-08-12). Solver uses native `/`. |
| 2026-08-11 | No `1e-9` scientific literals | [aura#2941](https://github.com/cybrid-systems/aura/issues/2941) **P2** | **fixed** | `1e3`, `1e-12`, etc. now OK in netlist/probe code. |
| 2026-08-11 | Export-before-require discipline | [aura#2766](https://github.com/cybrid-systems/aura/issues/2766) | fixed (prior) | Still follow export-before-require in span libs. |

## Daedalus workarounds still in force

1. **Form order in span libs**: always `(export …)` before `(require …)` when exports free-ref module cells ([aura#2766](https://github.com/cybrid-systems/aura/issues/2766)).
2. **Prefer `let*`** over internal `define` for dependent values in probes (host internal-define ≈ simultaneous letrec).
3. **Runner**:
   ```bash
   export AURA_BIN   # visible to children if multi-process later
   export AURA_PATH="$AURA_LIB:$DAEDALUS_LIB"
   export AURA_SANDBOX=off
   export AURA_PIPELINE_STRICT=0
   ```
4. Host expects program on **stdin** (`aura < file.aura`), not argv path.
