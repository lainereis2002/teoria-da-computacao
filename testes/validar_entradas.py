import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "entradas" / "manifesto.csv"
EXPECTED_LENGTHS = {"P_1000": 1000, "M_4000": 4000, "G_16000": 16000}
FAMILIES = {"aleatoria", "crescente", "inversa", "melhor_quick", "pior_merge"}


def read_values(path: Path) -> list[float]:
    with path.open(encoding="ascii") as file:
        return [float(line) for line in file if line.strip()]


def quick_partition_balance(values: list[float]) -> int:
    working = values.copy()
    stack = [(0, len(working) - 1)]
    comparisons = 0
    while stack:
        low, high = stack.pop()
        if low >= high:
            continue
        pivot_value = working[high]
        position = low
        for index in range(low, high):
            comparisons += 1
            if working[index] <= pivot_value:
                working[position], working[index] = working[index], working[position]
                position += 1
        working[position], working[high] = working[high], working[position]
        left_length = position - low
        right_length = high - position
        if abs(left_length - right_length) > 1:
            raise ValueError(
                f"Particao desbalanceada no melhor Quick: {left_length} e {right_length}."
            )
        stack.append((low, position - 1))
        stack.append((position + 1, high))
    return comparisons


def merge_comparisons(values: list[float]) -> int:
    auxiliary = [0.0] * len(values)

    def sort_range(left: int, right: int) -> int:
        if right - left < 2:
            return 0
        middle = left + (right - left) // 2
        comparisons = sort_range(left, middle) + sort_range(middle, right)
        left_index = left
        right_index = middle
        output_index = left
        while left_index < middle and right_index < right:
            comparisons += 1
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
        values[left:right] = auxiliary[left:right]
        return comparisons

    return sort_range(0, len(values))


def maximum_merge_comparisons(length: int) -> int:
    if length < 2:
        return 0
    left_length = length // 2
    right_length = length - left_length
    return (
        maximum_merge_comparisons(left_length)
        + maximum_merge_comparisons(right_length)
        + length
        - 1
    )


def main() -> None:
    if not MANIFEST.exists():
        raise FileNotFoundError("Execute o gerador antes de validar as entradas.")
    records: dict[tuple[str, str], dict[str, list[float]]] = {}
    with MANIFEST.open(encoding="ascii", newline="") as file:
        rows = list(csv.DictReader(file))
    if len(rows) != 150:
        raise ValueError(f"O manifesto possui {len(rows)} entradas; eram esperadas 150.")
    for row in rows:
        size = row["tamanho"]
        family = row["familia"]
        vector = row["vetor"]
        if size not in EXPECTED_LENGTHS or family not in FAMILIES:
            raise ValueError(f"Registro inesperado no manifesto: {row}.")
        path = ROOT / Path(row["arquivo"])
        values = read_values(path)
        if len(values) != EXPECTED_LENGTHS[size]:
            raise ValueError(f"Quantidade incorreta de valores em {path}.")
        if len(set(values)) != len(values):
            raise ValueError(f"Existem valores repetidos em {path}.")
        records.setdefault((size, vector), {})[family] = values
    for key, families in records.items():
        if set(families) != FAMILIES:
            raise ValueError(f"Familias incompletas para {key}.")
        reference = sorted(families["aleatoria"])
        for family, values in families.items():
            if sorted(values) != reference:
                raise ValueError(f"Conjunto de valores divergente em {key}, {family}.")
        if families["crescente"] != reference:
            raise ValueError(f"Entrada crescente invalida em {key}.")
        if families["inversa"] != list(reversed(reference)):
            raise ValueError(f"Entrada inversa invalida em {key}.")
        quick_partition_balance(families["melhor_quick"])
        actual = merge_comparisons(families["pior_merge"].copy())
        expected = maximum_merge_comparisons(len(reference))
        if actual != expected:
            raise ValueError(
                f"Pior Merge invalido em {key}: {actual} comparacoes, esperadas {expected}."
            )
    print("As 150 entradas e os casos construidos foram validados.")


if __name__ == "__main__":
    main()
