/* native/daed_abi.h — Daedalus C ABI for dense solve (issue #28 / #29)
 *
 * extern "C", no mangling. Row-major n×n A, rhs/solution in b.
 * Return 0 on success, non-zero on failure.
 */
#ifndef DAED_ABI_H
#define DAED_ABI_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#define DAED_ABI_VERSION 1
#define DAED_GE_EPS 1e-12

int64_t daed_abi_version(void);

/* In-place GE + partial pivot. A is n*n row-major. b becomes x. */
int64_t daed_solve_dense(double* A, double* b, int64_t n);

/* 0 = normal, non-zero = next daed_solve_dense returns 2 (probe poison). */
int64_t daed_set_fail(int64_t on);

/*
 * Single Aura c-func entry (host c-func steals cid 0..N-1).
 * op 0: version  op 1: set_fail(a)  op 2: solve((double*)a,(double*)b,c)
 */
int64_t daed_dispatch(int64_t op, int64_t a, int64_t b, int64_t c);

#ifdef __cplusplus
}
#endif

#endif
