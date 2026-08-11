# Host Residuals — Daedalus

Issues that are packaging / host / environment related, **not** denseness failures
on \(S_{\mathrm{Daedalus}}\).

| Date | Issue | Upstream | Notes |
|------|-------|----------|-------|
| 2026-08-11 | *(none observed in Phase 0)* | — | Smoke used export-before-require discipline from #2766 |

## Daedalus workarounds (inherited from sibling spans)

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
