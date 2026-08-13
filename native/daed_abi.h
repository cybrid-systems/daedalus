/* native/daed_abi.h — Daedalus C ABI for dense kernels (issue #29)
 *
 * Export rules (extern "C"):
 *   - Every public symbol is wrapped in extern "C" (no C++ mangling).
 *   - Types: int64_t, double*, void. No STL, bool, references, or overloads.
 *   - Caller owns every buffer. A is row-major n×n doubles.
 *   - Return 0 on success, a positive DAED_ERR_* on failure.
 *   - Bump DAED_ABI_VERSION only for breaking changes; additive symbols
 *     keep the same version. Aura binds daed_dispatch only (one c-func).
 */
#ifndef DAED_ABI_H
#define DAED_ABI_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define DAED_ABI_VERSION 1
#define DAED_GE_EPS 1e-12

#define DAED_OK            0
#define DAED_ERR_ARG       1  /* null pointer or n <= 0 */
#define DAED_ERR_POISON    2  /* daed_set_fail(1) armed */
#define DAED_ERR_SINGULAR  3  /* pivot below DAED_GE_EPS */
#define DAED_ERR_OP        4  /* unknown daed_dispatch op */
#define DAED_ERR_WORK      5  /* workspace missing */

int64_t daed_abi_version(void);

/* In-place GE + partial pivot. A is n*n row-major. b becomes x. */
int64_t daed_solve_dense(double* A, double* b, int64_t n);

/* Doubles required in `work` for daed_solve_dense_ws (n*n; 0 if n<=0). */
int64_t daed_solve_dense_work_n(int64_t n);

/* Same GE, but factors a copy of A in `work`. A is not mutated.
 * work must hold at least daed_solve_dense_work_n(n) doubles.
 */
int64_t daed_solve_dense_ws(double* A, double* b, int64_t n, double* work);

/* 0 = normal, non-zero = next solve returns DAED_ERR_POISON (probe). */
int64_t daed_set_fail(int64_t on);

/* Identity / exchange kernel: dst[i] = src[i] for i in [0,n). */
int64_t daed_copy_f64(double* dst, const double* src, int64_t n);

/*
 * Single Aura c-func entry (host c-func steals cid 0..N-1).
 * op 0: version
 * op 1: set_fail(a)
 * op 2: solve((double*)a, (double*)b, c)
 * op 3: work_n(a)
 * op 4: copy_f64((double*)a dst, (double*)b src, c)
 * Workspace solve is C-only (needs a 4th pointer).
 */
int64_t daed_dispatch(int64_t op, int64_t a, int64_t b, int64_t c);

#ifdef __cplusplus
}
#endif

#endif
