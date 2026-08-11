# Host Residuals — Daedalus

Issues that are packaging / host / environment related, **not** denseness failures
on \(S_{\mathrm{Daedalus}}\).

| Date | Issue | Upstream | Notes |
|------|-------|----------|-------|
| 2026-08-11 | Float `/` returns `0` for legitimate small operands after intermediate arithmetic | aura host (TBD issue) | Repro: GE on divider MNA; `a21=-0.001`, `a11=0.0015`, `(= a21 -0.001)` → `#t` but `(/ a21 a11)` → `0`. `(/ a21 d)` fails for `\|d\|<1`. Workaround: `daed:safe-div` scales so `\|den·scale\|≥1` before `/`. Still pure Aura — **not** a denseness escape. |
| 2026-08-11 | No `1e-9` scientific literals | aura parser | Write `0.000000001` or `(/ 1.0 1e9)`-style decimals; `e-9` parses as identifier. |
| 2026-08-11 | Phase 0 smoke | — | Export-before-require discipline from #2766 |

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
