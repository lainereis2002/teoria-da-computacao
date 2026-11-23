#include "../c/ordenacao.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int compare_double(const void *left, const void *right) {
    double a = *(const double *)left;
    double b = *(const double *)right;
    return (a > b) - (a < b);
}

static int run_case(const double *input, size_t length) {
    if (length == 0) {
        return quick_sort(NULL, 0);
    }
    size_t bytes = length * sizeof(*input);
    double *expected = malloc(bytes);
    double *quick_values = malloc(bytes);
    double *merge_values = malloc(bytes);
    double *auxiliary = malloc(bytes);
    if (expected == NULL || quick_values == NULL || merge_values == NULL || auxiliary == NULL) {
        free(expected);
        free(quick_values);
        free(merge_values);
        free(auxiliary);
        return 0;
    }
    memcpy(expected, input, bytes);
    memcpy(quick_values, input, bytes);
    memcpy(merge_values, input, bytes);
    qsort(expected, length, sizeof(*expected), compare_double);
    int success = quick_sort(quick_values, length);
    merge_sort(merge_values, auxiliary, length);
    for (size_t i = 0; i < length && success; i++) {
        success = quick_values[i] == expected[i] && merge_values[i] == expected[i];
    }
    free(expected);
    free(quick_values);
    free(merge_values);
    free(auxiliary);
    return success;
}

int main(void) {
    const double one[] = {1.0};
    const double ordered[] = {1.0, 2.0, 3.0, 4.0};
    const double inverse[] = {4.0, 3.0, 2.0, 1.0};
    const double repeated[] = {3.5, -1.25, 3.5, 0.0, -9.75};
    if (
        !run_case(NULL, 0) ||
        !run_case(one, sizeof(one) / sizeof(one[0])) ||
        !run_case(ordered, sizeof(ordered) / sizeof(ordered[0])) ||
        !run_case(inverse, sizeof(inverse) / sizeof(inverse[0])) ||
        !run_case(repeated, sizeof(repeated) / sizeof(repeated[0]))
    ) {
        fprintf(stderr, "Teste de ordenacao em C falhou.\n");
        return EXIT_FAILURE;
    }
    unsigned int state = 42;
    for (size_t length = 2; length <= 200; length++) {
        double *values = malloc(length * sizeof(*values));
        if (values == NULL) {
            return EXIT_FAILURE;
        }
        for (size_t i = 0; i < length; i++) {
            state = state * 1664525U + 1013904223U;
            values[i] = (double)(state % 10000U) / 100.0 - 50.0;
        }
        int success = run_case(values, length);
        free(values);
        if (!success) {
            fprintf(stderr, "Teste aleatorio em C falhou para n=%zu.\n", length);
            return EXIT_FAILURE;
        }
    }
    printf("Testes de ordenacao em C passaram.\n");
    return EXIT_SUCCESS;
}
