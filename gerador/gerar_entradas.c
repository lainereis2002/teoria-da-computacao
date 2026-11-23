#include <errno.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <direct.h>
#define CREATE_DIRECTORY(path) _mkdir(path)
#else
#include <sys/stat.h>
#define CREATE_DIRECTORY(path) mkdir(path, 0777)
#endif

#define SEED 42ULL
#define VALUE_LIMIT 100000001U
#define VECTOR_COUNT 10

typedef struct {
    const char *label;
    size_t length;
} SizeConfig;

static uint64_t rng_state = SEED;

static uint32_t next_random(void) {
    uint64_t value = rng_state;
    value ^= value >> 12;
    value ^= value << 25;
    value ^= value >> 27;
    rng_state = value;
    return (uint32_t)((value * 2685821657736338717ULL) >> 32);
}

static int compare_uint32(const void *left, const void *right) {
    uint32_t a = *(const uint32_t *)left;
    uint32_t b = *(const uint32_t *)right;
    return (a > b) - (a < b);
}

static int ensure_directory(const char *path) {
    if (CREATE_DIRECTORY(path) == 0 || errno == EEXIST) {
        return 1;
    }
    fprintf(stderr, "Nao foi possivel criar o diretorio %s.\n", path);
    return 0;
}

static size_t next_power_of_two(size_t value) {
    size_t result = 1;
    while (result < value) {
        result <<= 1;
    }
    return result;
}

static int generate_unique_values(uint32_t *values, size_t length) {
    size_t capacity = next_power_of_two(length * 2);
    uint32_t *table = malloc(capacity * sizeof(*table));
    if (table == NULL) {
        return 0;
    }
    for (size_t i = 0; i < capacity; i++) {
        table[i] = UINT32_MAX;
    }
    for (size_t i = 0; i < length;) {
        uint32_t candidate = next_random() % VALUE_LIMIT;
        size_t position = ((size_t)candidate * 2654435761U) & (capacity - 1);
        while (table[position] != UINT32_MAX && table[position] != candidate) {
            position = (position + 1) & (capacity - 1);
        }
        if (table[position] == candidate) {
            continue;
        }
        table[position] = candidate;
        values[i++] = candidate;
    }
    free(table);
    return 1;
}

static void build_quick_best(const uint32_t *sorted, size_t length, uint32_t *output) {
    if (length == 0) {
        return;
    }
    size_t left_length = (length - 1) / 2;
    size_t right_length = length - left_length - 1;
    build_quick_best(sorted, left_length, output);
    build_quick_best(sorted + left_length + 1, right_length, output + left_length);
    if (right_length > 1) {
        uint32_t last = output[left_length + right_length - 1];
        memmove(
            output + left_length + 1,
            output + left_length,
            (right_length - 1) * sizeof(*output)
        );
        output[left_length] = last;
    }
    output[length - 1] = sorted[left_length];
}

static int build_merge_worst(const uint32_t *sorted, size_t length, uint32_t *output) {
    if (length <= 1) {
        if (length == 1) {
            output[0] = sorted[0];
        }
        return 1;
    }
    size_t left_length = length / 2;
    size_t right_length = length - left_length;
    uint32_t *left = malloc(left_length * sizeof(*left));
    uint32_t *right = malloc(right_length * sizeof(*right));
    if (left == NULL || right == NULL) {
        free(left);
        free(right);
        return 0;
    }
    size_t left_index = 0;
    size_t right_index = 0;
    for (size_t i = 0; i < length; i++) {
        int goes_left = length % 2 == 0 ? i % 2 == 0 : i % 2 == 1;
        if (goes_left) {
            left[left_index++] = sorted[i];
        } else {
            right[right_index++] = sorted[i];
        }
    }
    int success =
        build_merge_worst(left, left_length, output) &&
        build_merge_worst(right, right_length, output + left_length);
    free(left);
    free(right);
    return success;
}

static int write_values(const char *path, const uint32_t *values, size_t length) {
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        fprintf(stderr, "Nao foi possivel criar o arquivo %s.\n", path);
        return 0;
    }
    for (size_t i = 0; i < length; i++) {
        uint32_t integer = values[i] / 1000000U;
        uint32_t fraction = values[i] % 1000000U;
        if (fprintf(file, "%u.%06u\n", integer, fraction) < 0) {
            fclose(file);
            return 0;
        }
    }
    return fclose(file) == 0;
}

static int write_family(
    FILE *manifest,
    const char *size_label,
    const char *family,
    int vector_number,
    const uint32_t *values,
    size_t length
) {
    char path[512];
    int written = snprintf(
        path,
        sizeof(path),
        "entradas/%s/%s/vetor_%02d.txt",
        size_label,
        family,
        vector_number
    );
    if (written < 0 || (size_t)written >= sizeof(path) || !write_values(path, values, length)) {
        return 0;
    }
    return fprintf(
        manifest,
        "%s,%zu,%s,%02d,%s\n",
        size_label,
        length,
        family,
        vector_number,
        path
    ) > 0;
}

static int prepare_directories(const SizeConfig *sizes, size_t size_count) {
    const char *families[] = {
        "aleatoria",
        "crescente",
        "inversa",
        "melhor_quick",
        "pior_merge"
    };
    if (!ensure_directory("entradas")) {
        return 0;
    }
    for (size_t i = 0; i < size_count; i++) {
        char size_path[256];
        snprintf(size_path, sizeof(size_path), "entradas/%s", sizes[i].label);
        if (!ensure_directory(size_path)) {
            return 0;
        }
        for (size_t j = 0; j < sizeof(families) / sizeof(families[0]); j++) {
            char family_path[512];
            int written = snprintf(
                family_path,
                sizeof(family_path),
                "%s/%s",
                size_path,
                families[j]
            );
            if (
                written < 0 ||
                (size_t)written >= sizeof(family_path) ||
                !ensure_directory(family_path)
            ) {
                return 0;
            }
        }
    }
    return 1;
}

int main(void) {
    const SizeConfig sizes[] = {
        {"P_1000", 1000},
        {"M_4000", 4000},
        {"G_16000", 16000}
    };
    size_t size_count = sizeof(sizes) / sizeof(sizes[0]);
    if (!prepare_directories(sizes, size_count)) {
        return EXIT_FAILURE;
    }
    FILE *manifest = fopen("entradas/manifesto.csv", "w");
    if (manifest == NULL) {
        fprintf(stderr, "Nao foi possivel criar o manifesto.\n");
        return EXIT_FAILURE;
    }
    fprintf(manifest, "tamanho,n,familia,vetor,arquivo\n");
    for (size_t size_index = 0; size_index < size_count; size_index++) {
        size_t length = sizes[size_index].length;
        uint32_t *random_values = malloc(length * sizeof(*random_values));
        uint32_t *sorted = malloc(length * sizeof(*sorted));
        uint32_t *inverse = malloc(length * sizeof(*inverse));
        uint32_t *quick_best = malloc(length * sizeof(*quick_best));
        uint32_t *merge_worst = malloc(length * sizeof(*merge_worst));
        if (
            random_values == NULL ||
            sorted == NULL ||
            inverse == NULL ||
            quick_best == NULL ||
            merge_worst == NULL
        ) {
            fprintf(stderr, "Memoria insuficiente para o tamanho %s.\n", sizes[size_index].label);
            free(random_values);
            free(sorted);
            free(inverse);
            free(quick_best);
            free(merge_worst);
            fclose(manifest);
            return EXIT_FAILURE;
        }
        for (int vector_number = 1; vector_number <= VECTOR_COUNT; vector_number++) {
            if (!generate_unique_values(random_values, length)) {
                fprintf(stderr, "Falha ao gerar valores unicos.\n");
                fclose(manifest);
                return EXIT_FAILURE;
            }
            memcpy(sorted, random_values, length * sizeof(*sorted));
            qsort(sorted, length, sizeof(*sorted), compare_uint32);
            for (size_t i = 0; i < length; i++) {
                inverse[i] = sorted[length - i - 1];
            }
            build_quick_best(sorted, length, quick_best);
            if (!build_merge_worst(sorted, length, merge_worst)) {
                fprintf(stderr, "Falha ao construir o pior caso do Merge Sort.\n");
                fclose(manifest);
                return EXIT_FAILURE;
            }
            int success =
                write_family(
                    manifest,
                    sizes[size_index].label,
                    "aleatoria",
                    vector_number,
                    random_values,
                    length
                ) &&
                write_family(
                    manifest,
                    sizes[size_index].label,
                    "crescente",
                    vector_number,
                    sorted,
                    length
                ) &&
                write_family(
                    manifest,
                    sizes[size_index].label,
                    "inversa",
                    vector_number,
                    inverse,
                    length
                ) &&
                write_family(
                    manifest,
                    sizes[size_index].label,
                    "melhor_quick",
                    vector_number,
                    quick_best,
                    length
                ) &&
                write_family(
                    manifest,
                    sizes[size_index].label,
                    "pior_merge",
                    vector_number,
                    merge_worst,
                    length
                );
            if (!success) {
                fclose(manifest);
                return EXIT_FAILURE;
            }
        }
        free(random_values);
        free(sorted);
        free(inverse);
        free(quick_best);
        free(merge_worst);
    }
    if (fclose(manifest) != 0) {
        return EXIT_FAILURE;
    }
    printf("150 arquivos de entrada gerados com a semente 42.\n");
    return EXIT_SUCCESS;
}
