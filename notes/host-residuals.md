# Host Residuals — Daedalus

Issues that are packaging / host / environment related, **not** denseness failures
on \(S_{\mathrm{Daedalus}}\).

| Date | Issue | Upstream | Status | Notes |
|------|-------|----------|--------|-------|
| 2026-08-11 | Float `/` returns `0` after intermediate arithmetic | [aura#2940](https://github.com/cybrid-systems/aura/issues/2940) **P0** | **fixed** | Was blocking dense GE; `daed:safe-div` workaround **removed** (2026-08-12). Solver uses native `/`. |
| 2026-08-11 | No `1e-9` scientific literals | [aura#2941](https://github.com/cybrid-systems/aura/issues/2941) **P2** | **fixed** | `1e3`, `1e-12`, etc. now OK in netlist/probe code. |
| 2026-08-11 | Export-before-require discipline | [aura#2766](https://github.com/cybrid-systems/aura/issues/2766) | fixed (prior) | Still follow export-before-require in span libs. |
| 2026-08-12 | `make-vector` rejects float length (incl. `floor` result); misleading `max_size()` error | [aura#2965](https://github.com/cybrid-systems/aura/issues/2965) **P1** | **fixed** | Host coerces integer-valued float lengths for `make-vector`. `vector-ref` / `vector-set!` still need true integers. Daedalus: `daed:as-int` / `daed:nsteps-for` = `inexact->exact` ∘ `round`. |
| 2026-08-12 | `ast:snapshot` returns silent `-1` without `set-code` workspace (stdin denseness) | [aura#2966](https://github.com/cybrid-systems/aura/issues/2966) **P1** | open | Related #2918 (wrong `current-source`). Dual rollback: pure-Aura `daed:snapshot` (comps + stats); host `ast_id` best-effort. Aether works via `set-code` bootstrap. |
| 2026-08-14 | `c-func` closures collide with low Aura cids (`cid < n_ffi` treated as FFI) | host FFI apply | open | Binding 3 symbols stole `daed:V`/`daed:circuit` and SIGSEGV'd. Workaround: one `daed_dispatch` trampoline + `c-opaque->int`. |

## Daedalus workarounds still in force

1. **Form order in span libs**: always `(export …)` before `(require …)` when exports free-ref module cells ([aura#2766](https://github.com/cybrid-systems/aura/issues/2766)).
2. **Prefer `let*`** over internal `define` for dependent values in probes (host internal-define ≈ simultaneous letrec).
3. **`.tran` step counts / vector indices**: use `daed:nsteps-for` / `daed:as-int` (not bare `floor` — FP under-shoots; not raw float for `vector-ref`).
4. **Runner**:
   ```bash
   export AURA_BIN   # visible to children if multi-process later
   export AURA_PATH="$AURA_LIB:$DAEDALUS_LIB"
   export AURA_SANDBOX=off
   export AURA_PIPELINE_STRICT=0
   ```
5. Host expects program on **stdin** (`aura < file.aura`), not argv path.
