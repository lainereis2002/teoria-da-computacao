#include "ordenacao.h"

#include <limits.h>
#include <stdlib.h>

typedef struct {
    size_t low;
    size_t high;
} Range;

static void swap(double *left, double *right) {
    double temporary = *left;
    *left = *right;
    *right = temporary;
}

static size_t partition_lomuto(double *values, size_t low, size_t high) {
    double pivot = values[high];
    size_t position = low;
    for (size_t index = low; index < high; index++) {
        if (values[index] <= pivot) {
            swap(&values[position], &values[index]);
            position++;
        }
    }
    swap(&values[position], &values[high]);
    return position;
}

int quick_sort(double *values, size_t length) {
    if (length < 2) {
        return 1;
    }
    size_t capacity = sizeof(size_t) * CHAR_BIT + 1;
    Range *stack = malloc(capacity * sizeof(*stack));
    if (stack == NULL) {
        return 0;
    }
    size_t top = 0;
    stack[top++] = (Range){0, length - 1};
    while (top > 0) {
        Range current = stack[--top];
        size_t low = current.low;
        size_t high = current.high;
        while (low < high) {
            size_t pivot = partition_lomuto(values, low, high);
            size_t left_size = pivot - low;
            size_t right_size = high - pivot;
            if (left_size < right_size) {
                if (right_size > 1) {
                    if (top == capacity) {
                        free(stack);
                        return 0;
                    }
                    stack[top++] = (Range){pivot + 1, high};
                }
                if (left_size > 1) {
                    high = pivot - 1;
                } else {
                    break;
                }
            } else {
                if (left_size > 1) {
                    if (top == capacity) {
                        free(stack);
                        return 0;
                    }
                    stack[top++] = (Range){low, pivot - 1};
                }
                if (right_size > 1) {
                    low = pivot + 1;
                } else {
                    break;
                }
            }
        }
    }
    free(stack);
    return 1;
}

static void merge(
    double *values,
    double *auxiliary,
    size_t left,
    size_t middle,
    size_t right
) {
    size_t left_index = left;
    size_t right_index = middle;
    size_t output_index = left;
    while (left_index < middle && right_index < right) {
        if (values[left_index] <= values[right_index]) {
            auxiliary[output_index++] = values[left_index++];
        } else {
            auxiliary[output_index++] = values[right_index++];
        }
    }
    while (left_index < middle) {
        auxiliary[output_index++] = values[left_index++];
    }
    while (right_index < right) {
        auxiliary[output_index++] = values[right_index++];
    }
    for (size_t index = left; index < right; index++) {
        values[index] = auxiliary[index];
    }
}

static void merge_sort_range(
    double *values,
    double *auxiliary,
    size_t left,
    size_t right
) {
    if (right - left < 2) {
        return;
    }
    size_t middle = left + (right - left) / 2;
    merge_sort_range(values, auxiliary, left, middle);
    merge_sort_range(values, auxiliary, middle, right);
    merge(values, auxiliary, left, middle, right);
}

void merge_sort(double *values, double *auxiliary, size_t length) {
    merge_sort_range(values, auxiliary, 0, length);
}
