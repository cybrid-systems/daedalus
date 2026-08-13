/* native/daed_solve.cpp — dense GE kernel (issue #28 / #29)
 *
 * Educational dense solver, same shape as daed:dense-solve-pure!.
 * Build: ./scripts/build-native.sh   or   cmake -S native -B native/build
 */
#include "daed_abi.h"

#include <cmath>
#include <cstddef>

static int64_t g_fail = 0;

int64_t daed_abi_version(void) {
    return DAED_ABI_VERSION;
}

int64_t daed_set_fail(int64_t on) {
    g_fail = on;
    return DAED_OK;
}

static double at(const double* A, int64_t n, int64_t i, int64_t j) {
    return A[i * n + j];
}

static void set_at(double* A, int64_t n, int64_t i, int64_t j, double v) {
    A[i * n + j] = v;
}

static void swap_rows(double* A, double* b, int64_t n, int64_t r1, int64_t r2) {
    if (r1 == r2) {
        return;
    }
    for (int64_t j = 0; j < n; ++j) {
        double t = at(A, n, r1, j);
        set_at(A, n, r1, j, at(A, n, r2, j));
        set_at(A, n, r2, j, t);
    }
    double tb = b[r1];
    b[r1] = b[r2];
    b[r2] = tb;
}

static int64_t solve_inplace(double* A, double* b, int64_t n) {
    for (int64_t col = 0; col < n; ++col) {
        int64_t piv = col;
        double best = std::fabs(at(A, n, col, col));
        for (int64_t r = col + 1; r < n; ++r) {
            double av = std::fabs(at(A, n, r, col));
            if (av > best) {
                best = av;
                piv = r;
            }
        }
        if (best < DAED_GE_EPS) {
            return DAED_ERR_SINGULAR;
        }
        swap_rows(A, b, n, col, piv);
        double diag = at(A, n, col, col);
        for (int64_t i = col + 1; i < n; ++i) {
            double factor = at(A, n, i, col) / diag;
            set_at(A, n, i, col, 0.0);
            for (int64_t j = col + 1; j < n; ++j) {
                set_at(A, n, i, j, at(A, n, i, j) - factor * at(A, n, col, j));
            }
            b[i] = b[i] - factor * b[col];
        }
    }
    for (int64_t i = n - 1; i >= 0; --i) {
        double s = b[i];
        for (int64_t j = i + 1; j < n; ++j) {
            s -= at(A, n, i, j) * b[j];
        }
        double diag = at(A, n, i, i);
        if (std::fabs(diag) < DAED_GE_EPS) {
            return DAED_ERR_SINGULAR;
        }
        b[i] = s / diag;
    }
    return DAED_OK;
}

int64_t daed_dispatch(int64_t op, int64_t a, int64_t b, int64_t c) {
    if (op == 0) {
        return daed_abi_version();
    }
    if (op == 1) {
        return daed_set_fail(a);
    }
    if (op == 2) {
        return daed_solve_dense(reinterpret_cast<double*>(a),
                                reinterpret_cast<double*>(b), c);
    }
    if (op == 3) {
        return daed_solve_dense_work_n(a);
    }
    return DAED_ERR_OP;
}

int64_t daed_solve_dense(double* A, double* b, int64_t n) {
    if (g_fail) {
        return DAED_ERR_POISON;
    }
    if (A == nullptr || b == nullptr || n <= 0) {
        return DAED_ERR_ARG;
    }
    return solve_inplace(A, b, n);
}

int64_t daed_solve_dense_work_n(int64_t n) {
    if (n <= 0) {
        return 0;
    }
    return n * n;
}

int64_t daed_solve_dense_ws(double* A, double* b, int64_t n, double* work) {
    if (g_fail) {
        return DAED_ERR_POISON;
    }
    if (A == nullptr || b == nullptr || n <= 0) {
        return DAED_ERR_ARG;
    }
    if (work == nullptr) {
        return DAED_ERR_WORK;
    }
    int64_t nn = n * n;
    for (int64_t i = 0; i < nn; ++i) {
        work[i] = A[i];
    }
    return solve_inplace(work, b, n);
}
