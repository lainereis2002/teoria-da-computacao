#include "ordenacao.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int read_values(const char *path, double **values, size_t *length) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return 0;
    }
    size_t capacity = 1024;
    size_t count = 0;
    double *result = malloc(capacity * sizeof(*result));
    if (result == NULL) {
        fclose(file);
        return 0;
    }
    double value;
    while (fscanf(file, "%lf", &value) == 1) {
        if (count == capacity) {
            capacity *= 2;
            double *expanded = realloc(result, capacity * sizeof(*expanded));
            if (expanded == NULL) {
                free(result);
                fclose(file);
                return 0;
            }
            result = expanded;
        }
        result[count++] = value;
    }
    if (!feof(file)) {
        free(result);
        fclose(file);
        return 0;
    }
    fclose(file);
    *values = result;
    *length = count;
    return 1;
}

static int write_values(const char *path, const double *values, size_t length) {
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        return 0;
    }
    for (size_t i = 0; i < length; i++) {
        if (fprintf(file, "%.17g\n", values[i]) < 0) {
            fclose(file);
            return 0;
        }
    }
    return fclose(file) == 0;
}

int main(int argument_count, char **arguments) {
    if (argument_count < 3 || argument_count > 4) {
        fprintf(stderr, "Uso: executar.exe <quick|merge> <entrada> [saida]\n");
        return EXIT_FAILURE;
    }
    double *values;
    size_t length;
    if (!read_values(arguments[2], &values, &length)) {
        fprintf(stderr, "Nao foi possivel ler a entrada.\n");
        return EXIT_FAILURE;
    }
    int success;
    if (strcmp(arguments[1], "quick") == 0) {
        success = quick_sort(values, length);
    } else if (strcmp(arguments[1], "merge") == 0) {
        double *auxiliary = malloc(length * sizeof(*auxiliary));
        if (auxiliary == NULL && length > 0) {
            free(values);
            return EXIT_FAILURE;
        }
        merge_sort(values, auxiliary, length);
        free(auxiliary);
        success = 1;
    } else {
        fprintf(stderr, "Algoritmo invalido.\n");
        free(values);
        return EXIT_FAILURE;
    }
    if (!success) {
        fprintf(stderr, "Falha durante a ordenacao.\n");
        free(values);
        return EXIT_FAILURE;
    }
    if (argument_count == 4 && !write_values(arguments[3], values, length)) {
        fprintf(stderr, "Nao foi possivel gravar a saida.\n");
        free(values);
        return EXIT_FAILURE;
    }
    free(values);
    return EXIT_SUCCESS;
}
