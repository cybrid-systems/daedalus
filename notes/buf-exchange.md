# Buffer / Opaque exchange (issue #32)

How matrix/vector data moves between Aura vectors and C++ kernels.

## Ownership

| Object | Owner | Lifetime |
|--------|--------|----------|
| FlatAST / solver `vector` | Aura | Whole solve / mutate / snapshot |
| `c-alloc` scratch (`Opaque`) | Aura wrapper (`lib/buf.aura`) | One native call only |
| `double*` seen by C++ | Borrowed | Until the C function returns |

C++ must not store the pointer. The wrapper always `c-free`s, including on
`rc≠0` and on a partial alloc failure.

## Call sequence

1. `daed:buf-alloc` (`n×n` and/or `n` doubles, 8 bytes each)
2. `daed:buf-copy-in!` — Aura vector → Opaque (`c-struct-set!`)
3. `c-opaque->int` → `daed_dispatch` (op 2 = GE, op 4 = identity copy)
4. On success, `daed:buf-copy-out!` — Opaque → Aura vector
5. `daed:buf-free!` both buffers

## Tracking

`daed:buf-live`, `daed:buf-allocs`, `daed:buf-frees`, `daed:buf-bytes`.
After a soak, `daed:buf-balanced?` means `live=0` and `allocs=frees`.

## Pin-stable path

Not used. Aura `pin-stable-refs` is an AST node-id pin (Hephaestus probe 19),
not a float-buffer pin. A pinned native buffer is a follow-up if the host
exposes one.
