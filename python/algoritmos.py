from collections.abc import MutableSequence


def _partition_lomuto(values: MutableSequence[float], low: int, high: int) -> int:
    pivot = values[high]
    position = low
    for index in range(low, high):
        if values[index] <= pivot:
            values[position], values[index] = values[index], values[position]
            position += 1
    values[position], values[high] = values[high], values[position]
    return position


def quick_sort(values: MutableSequence[float]) -> None:
    if len(values) < 2:
        return
    stack = [(0, len(values) - 1)]
    while stack:
        low, high = stack.pop()
        while low < high:
            pivot = _partition_lomuto(values, low, high)
            left_size = pivot - low
            right_size = high - pivot
            if left_size < right_size:
                if right_size > 1:
                    stack.append((pivot + 1, high))
                if left_size > 1:
                    high = pivot - 1
                else:
                    break
            else:
                if left_size > 1:
                    stack.append((low, pivot - 1))
                if right_size > 1:
                    low = pivot + 1
                else:
                    break


def _merge(
    values: MutableSequence[float],
    auxiliary: MutableSequence[float],
    left: int,
    middle: int,
    right: int,
) -> None:
    left_index = left
    right_index = middle
    output_index = left
    while left_index < middle and right_index < right:
        if values[left_index] <= values[right_index]:
            auxiliary[output_index] = values[left_index]
            left_index += 1
        else:
            auxiliary[output_index] = values[right_index]
            right_index += 1
        output_index += 1
    while left_index < middle:
        auxiliary[output_index] = values[left_index]
        left_index += 1
        output_index += 1
    while right_index < right:
        auxiliary[output_index] = values[right_index]
        right_index += 1
        output_index += 1
    for index in range(left, right):
        values[index] = auxiliary[index]


def _merge_sort(
    values: MutableSequence[float],
    auxiliary: MutableSequence[float],
    left: int,
    right: int,
) -> None:
    if right - left < 2:
        return
    middle = left + (right - left) // 2
    _merge_sort(values, auxiliary, left, middle)
    _merge_sort(values, auxiliary, middle, right)
    _merge(values, auxiliary, left, middle, right)


def merge_sort(
    values: MutableSequence[float],
    auxiliary: MutableSequence[float] | None = None,
) -> None:
    if auxiliary is None:
        auxiliary = [0.0] * len(values)
    elif len(auxiliary) < len(values):
        raise ValueError("O vetor auxiliar e menor que o vetor de entrada.")
    _merge_sort(values, auxiliary, 0, len(values))
