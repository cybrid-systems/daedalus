/* native/example_dense.c — ABI smoke via dlopen/dlsym (issue #29).
 *
 * No Aura required. Confirms unmangled symbols and a 2×2 GE.
 *
 *   ./scripts/check-native-abi.sh
 *   cc -O2 -o /tmp/daed_example native/example_dense.c -ldl
 *   /tmp/daed_example native/libdaed_solve.so
 */
#include <dlfcn.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static int close_enough(double a, double b) {
    double d = a - b;
    if (d < 0.0) {
        d = -d;
    }
    return d < 1e-9;
}

int main(int argc, char** argv) {
    const char* path = (argc > 1) ? argv[1] : "native/libdaed_solve.so";
    void* h = dlopen(path, RTLD_NOW);
    if (!h) {
        fprintf(stderr, "dlopen %s: %s\n", path, dlerror());
        printf("RESULT fail\n");
        return 1;
    }

    int64_t (*ver)(void) = (int64_t (*)(void))dlsym(h, "daed_abi_version");
    int64_t (*solve)(double*, double*, int64_t) =
        (int64_t (*)(double*, double*, int64_t))dlsym(h, "daed_solve_dense");
    int64_t (*workn)(int64_t) =
        (int64_t (*)(int64_t))dlsym(h, "daed_solve_dense_work_n");
    int64_t (*ws)(double*, double*, int64_t, double*) =
        (int64_t (*)(double*, double*, int64_t, double*))dlsym(h, "daed_solve_dense_ws");
    int64_t (*disp)(int64_t, int64_t, int64_t, int64_t) =
        (int64_t (*)(int64_t, int64_t, int64_t, int64_t))dlsym(h, "daed_dispatch");

    int ok = 1;
    if (!ver || !solve || !workn || !ws || !disp) {
        fprintf(stderr, "dlsym missing (unmangled names required)\n");
        ok = 0;
    } else {
        if (ver() != 1) {
            fprintf(stderr, "abi version %lld\n", (long long)ver());
            ok = 0;
        }
        if (disp(0, 0, 0, 0) != 1) {
            fprintf(stderr, "dispatch version failed\n");
            ok = 0;
        }
        if (workn(2) != 4) {
            fprintf(stderr, "work_n(2)=%lld\n", (long long)workn(2));
            ok = 0;
        }

        /* 2x + y = 5; x + 2y = 4 → x=2, y=1 */
        double A[] = {2.0, 1.0, 1.0, 2.0};
        double b[] = {5.0, 4.0};
        int64_t rc = solve(A, b, 2);
        if (rc != 0 || !close_enough(b[0], 2.0) || !close_enough(b[1], 1.0)) {
            fprintf(stderr, "solve rc=%lld x=%g %g\n", (long long)rc, b[0], b[1]);
            ok = 0;
        }

        double A2[] = {2.0, 1.0, 1.0, 2.0};
        double b2[] = {5.0, 4.0};
        double work[4];
        rc = ws(A2, b2, 2, work);
        if (rc != 0 || !close_enough(b2[0], 2.0) || !close_enough(b2[1], 1.0)) {
            fprintf(stderr, "ws rc=%lld x=%g %g\n", (long long)rc, b2[0], b2[1]);
            ok = 0;
        }
        if (!close_enough(A2[0], 2.0) || !close_enough(A2[1], 1.0)
            || !close_enough(A2[2], 1.0) || !close_enough(A2[3], 2.0)) {
            fprintf(stderr, "ws mutated A\n");
            ok = 0;
        }
        if (ws(A2, b2, 2, NULL) != 5) {
            fprintf(stderr, "ws null work expected DAED_ERR_WORK=5\n");
            ok = 0;
        }
    }

    dlclose(h);
    printf("RESULT %s\n", ok ? "pass" : "fail");
    return ok ? 0 : 1;
}
