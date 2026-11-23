#ifndef _WIN32
#define _POSIX_C_SOURCE 200809L
#endif

#include "../c/ordenacao.h"

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#else
#include <time.h>
#endif

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define VECTOR_COUNT 10

typedef struct {
    const char *label;
    size_t length;
} SizeConfig;

static int compare_double(const void *left, const void *right) {
    double a = *(const double *)left;
    double b = *(const double *)right;
    return (a > b) - (a < b);
}

static int read_vector(const char *path, double *values, size_t length) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return 0;
    }
    for (size_t i = 0; i < length; i++) {
        if (fscanf(file, "%lf", &values[i]) != 1) {
            fclose(file);
            return 0;
        }
    }
    double extra;
    int valid = fscanf(file, "%lf", &extra) != 1 && feof(file);
    fclose(file);
    return valid;
}

static void free_block(double **block) {
    if (block == NULL) {
        return;
    }
    for (int i = 0; i < VECTOR_COUNT; i++) {
        free(block[i]);
    }
    free(block);
}

static double **allocate_block(size_t length) {
    double **block = calloc(VECTOR_COUNT, sizeof(*block));
    if (block == NULL) {
        return NULL;
    }
    for (int i = 0; i < VECTOR_COUNT; i++) {
        block[i] = malloc(length * sizeof(**block));
        if (block[i] == NULL) {
            free_block(block);
            return NULL;
        }
    }
    return block;
}

static double **load_block(const char *size, const char *family, size_t length) {
    double **block = allocate_block(length);
    if (block == NULL) {
        return NULL;
    }
    for (int i = 0; i < VECTOR_COUNT; i++) {
        char path[512];
        snprintf(
            path,
            sizeof(path),
            "entradas/%s/%s/vetor_%02d.txt",
            size,
            family,
            i + 1
        );
        if (!read_vector(path, block[i], length)) {
            fprintf(stderr, "Nao foi possivel ler %s.\n", path);
            free_block(block);
            return NULL;
        }
    }
    return block;
}

static double wall_seconds(void) {
#ifdef _WIN32
    LARGE_INTEGER counter;
    LARGE_INTEGER frequency;
    if (!QueryPerformanceFrequency(&frequency) || !QueryPerformanceCounter(&counter)) {
        return -1.0;
    }
    return (double)counter.QuadPart / (double)frequency.QuadPart;
#else
    struct timespec value;
    if (clock_gettime(CLOCK_MONOTONIC, &value) != 0) {
        return -1.0;
    }
    return (double)value.tv_sec + (double)value.tv_nsec / 1000000000.0;
#endif
}

static double process_cpu_seconds(void) {
#ifdef _WIN32
    FILETIME creation;
    FILETIME exit;
    FILETIME kernel;
    FILETIME user;
    if (!GetProcessTimes(GetCurrentProcess(), &creation, &exit, &kernel, &user)) {
        return -1.0;
    }
    ULARGE_INTEGER kernel_value;
    ULARGE_INTEGER user_value;
    kernel_value.LowPart = kernel.dwLowDateTime;
    kernel_value.HighPart = kernel.dwHighDateTime;
    user_value.LowPart = user.dwLowDateTime;
    user_value.HighPart = user.dwHighDateTime;
    return (double)(kernel_value.QuadPart + user_value.QuadPart) / 10000000.0;
#else
    struct timespec value;
    if (clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &value) != 0) {
        return -1.0;
    }
    return (double)value.tv_sec + (double)value.tv_nsec / 1000000000.0;
#endif
}

static int prepare_expected(double **originals, double **expected, size_t length) {
    for (int i = 0; i < VECTOR_COUNT; i++) {
        memcpy(expected[i], originals[i], length * sizeof(**expected));
        qsort(expected[i], length, sizeof(**expected), compare_double);
    }
    return 1;
}

static void restore_block(double **originals, double **working, size_t length) {
    for (int i = 0; i < VECTOR_COUNT; i++) {
        memcpy(working[i], originals[i], length * sizeof(**working));
    }
}

static int sort_block(
    const char *algorithm,
    double **working,
    double **auxiliaries,
    size_t length
) {
    for (int i = 0; i < VECTOR_COUNT; i++) {
        if (strcmp(algorithm, "quick") == 0) {
            if (!quick_sort(working[i], length)) {
                return 0;
            }
        } else {
            merge_sort(working[i], auxiliaries[i], length);
        }
    }
    return 1;
}

static int validate_block(double **working, double **expected, size_t length) {
    for (int i = 0; i < VECTOR_COUNT; i++) {
        if (memcmp(working[i], expected[i], length * sizeof(**working)) != 0) {
            fprintf(stderr, "Resultado incorreto no vetor %d.\n", i + 1);
            return 0;
        }
    }
    return 1;
}

static int find_size(const char *label, SizeConfig *result) {
    const SizeConfig sizes[] = {
        {"P_1000", 1000},
        {"M_4000", 4000},
        {"G_16000", 16000}
    };
    for (size_t i = 0; i < sizeof(sizes) / sizeof(sizes[0]); i++) {
        if (strcmp(label, sizes[i].label) == 0) {
            *result = sizes[i];
            return 1;
        }
    }
    return 0;
}

int main(int argument_count, char **arguments) {
    if (argument_count != 7) {
        fprintf(
            stderr,
            "Uso: medir_c.exe <quick|merge> <familia> <tamanho> <repeticoes> "
            "<aquecimentos> <saida.csv>\n"
        );
        return EXIT_FAILURE;
    }
    const char *algorithm = arguments[1];
    const char *family = arguments[2];
    SizeConfig size;
    int repetitions = atoi(arguments[4]);
    int warmups = atoi(arguments[5]);
    if (
        (strcmp(algorithm, "quick") != 0 && strcmp(algorithm, "merge") != 0) ||
        !find_size(arguments[3], &size) ||
        repetitions < 1 ||
        warmups < 0
    ) {
        fprintf(stderr, "Argumentos invalidos.\n");
        return EXIT_FAILURE;
    }
    double **originals = load_block(size.label, family, size.length);
    double **working = allocate_block(size.length);
    double **expected = allocate_block(size.length);
    double **auxiliaries =
        strcmp(algorithm, "merge") == 0 ? allocate_block(size.length) : NULL;
    if (
        originals == NULL ||
        working == NULL ||
        expected == NULL ||
        (strcmp(algorithm, "merge") == 0 && auxiliaries == NULL)
    ) {
        free_block(originals);
        free_block(working);
        free_block(expected);
        free_block(auxiliaries);
        return EXIT_FAILURE;
    }
    prepare_expected(originals, expected, size.length);
    for (int warmup = 0; warmup < warmups; warmup++) {
        restore_block(originals, working, size.length);
        if (
            !sort_block(algorithm, working, auxiliaries, size.length) ||
            !validate_block(working, expected, size.length)
        ) {
            free_block(originals);
            free_block(working);
            free_block(expected);
            free_block(auxiliaries);
            return EXIT_FAILURE;
        }
    }
    FILE *output = fopen(arguments[6], "w");
    if (output == NULL) {
        fprintf(stderr, "Nao foi possivel criar %s.\n", arguments[6]);
        free_block(originals);
        free_block(working);
        free_block(expected);
        free_block(auxiliaries);
        return EXIT_FAILURE;
    }
    fprintf(
        output,
        "linguagem,algoritmo,familia,tamanho_categoria,n,repeticao,"
        "quantidade_vetores,tempo_real_bloco,tempo_cpu_bloco,"
        "tempo_real_medio_vetor,tempo_cpu_medio_vetor,semente\n"
    );
    for (int repetition = 1; repetition <= repetitions; repetition++) {
        restore_block(originals, working, size.length);
        double wall_start = wall_seconds();
        double cpu_start = process_cpu_seconds();
        int success = sort_block(algorithm, working, auxiliaries, size.length);
        double cpu_end = process_cpu_seconds();
        double wall_end = wall_seconds();
        if (
            !success ||
            wall_start < 0.0 ||
            wall_end < 0.0 ||
            cpu_start < 0.0 ||
            cpu_end < 0.0 ||
            !validate_block(working, expected, size.length)
        ) {
            fclose(output);
            free_block(originals);
            free_block(working);
            free_block(expected);
            free_block(auxiliaries);
            return EXIT_FAILURE;
        }
        double wall = wall_end - wall_start;
        double cpu = cpu_end - cpu_start;
        fprintf(
            output,
            "c,%s,%s,%s,%zu,%d,%d,%.9f,%.9f,%.9f,%.9f,42\n",
            algorithm,
            family,
            size.label,
            size.length,
            repetition,
            VECTOR_COUNT,
            wall,
            cpu,
            wall / VECTOR_COUNT,
            cpu / VECTOR_COUNT
        );
    }
    fclose(output);
    free_block(originals);
    free_block(working);
    free_block(expected);
    free_block(auxiliaries);
    return EXIT_SUCCESS;
}
