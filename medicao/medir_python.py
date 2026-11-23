import argparse
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from python.algoritmos import merge_sort, quick_sort

SIZE_LENGTHS = {"P_1000": 1000, "M_4000": 4000, "G_16000": 16000}
FAMILIES = ("aleatoria", "crescente", "inversa", "melhor_quick", "pior_merge")
VECTOR_COUNT = 10
FIELDS = (
    "linguagem",
    "algoritmo",
    "familia",
    "tamanho_categoria",
    "n",
    "repeticao",
    "quantidade_vetores",
    "tempo_real_bloco",
    "tempo_cpu_bloco",
    "tempo_real_medio_vetor",
    "tempo_cpu_medio_vetor",
    "semente",
)


def read_block(size: str, family: str) -> list[list[float]]:
    directory = ROOT / "entradas" / size / family
    block = []
    for number in range(1, VECTOR_COUNT + 1):
        path = directory / f"vetor_{number:02d}.txt"
        with path.open(encoding="ascii") as file:
            values = [float(line) for line in file if line.strip()]
        if len(values) != SIZE_LENGTHS[size]:
            raise ValueError(f"Quantidade incorreta de valores em {path}.")
        block.append(values)
    return block


def sort_block(
    algorithm: str,
    working: list[list[float]],
    auxiliaries: list[list[float]] | None,
) -> None:
    if algorithm == "quick":
        for values in working:
            quick_sort(values)
    else:
        if auxiliaries is None:
            raise ValueError("Vetores auxiliares ausentes.")
        for values, auxiliary in zip(working, auxiliaries, strict=True):
            merge_sort(values, auxiliary)


def prepare_working(
    originals: list[list[float]],
    algorithm: str,
) -> tuple[list[list[float]], list[list[float]] | None]:
    working = [values.copy() for values in originals]
    auxiliaries = (
        [[0.0] * len(values) for values in originals] if algorithm == "merge" else None
    )
    return working, auxiliaries


def validate_block(working: list[list[float]], expected: list[list[float]]) -> None:
    for index, (actual, reference) in enumerate(zip(working, expected, strict=True), 1):
        if actual != reference:
            raise ValueError(f"Resultado incorreto no vetor {index}.")


def measure(
    algorithm: str,
    family: str,
    size: str,
    repetitions: int,
    warmups: int,
) -> list[dict[str, str | int | float]]:
    originals = read_block(size, family)
    expected = [sorted(values) for values in originals]
    for _ in range(warmups):
        working, auxiliaries = prepare_working(originals, algorithm)
        sort_block(algorithm, working, auxiliaries)
        validate_block(working, expected)
    rows = []
    for repetition in range(1, repetitions + 1):
        working, auxiliaries = prepare_working(originals, algorithm)
        wall_start = time.perf_counter()
        cpu_start = time.process_time()
        sort_block(algorithm, working, auxiliaries)
        cpu_seconds = time.process_time() - cpu_start
        wall_seconds = time.perf_counter() - wall_start
        validate_block(working, expected)
        rows.append(
            {
                "linguagem": "python",
                "algoritmo": algorithm,
                "familia": family,
                "tamanho_categoria": size,
                "n": SIZE_LENGTHS[size],
                "repeticao": repetition,
                "quantidade_vetores": VECTOR_COUNT,
                "tempo_real_bloco": f"{wall_seconds:.9f}",
                "tempo_cpu_bloco": f"{cpu_seconds:.9f}",
                "tempo_real_medio_vetor": f"{wall_seconds / VECTOR_COUNT:.9f}",
                "tempo_cpu_medio_vetor": f"{cpu_seconds / VECTOR_COUNT:.9f}",
                "semente": 42,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("algoritmo", choices=("quick", "merge"))
    parser.add_argument("familia", choices=FAMILIES)
    parser.add_argument("tamanho", choices=tuple(SIZE_LENGTHS))
    parser.add_argument("saida", type=Path)
    parser.add_argument("--repeticoes", type=int, default=20)
    parser.add_argument("--aquecimentos", type=int, default=2)
    arguments = parser.parse_args()
    if arguments.repeticoes < 1 or arguments.aquecimentos < 0:
        parser.error("Repeticoes deve ser positiva e aquecimentos nao pode ser negativo.")
    rows = measure(
        arguments.algoritmo,
        arguments.familia,
        arguments.tamanho,
        arguments.repeticoes,
        arguments.aquecimentos,
    )
    arguments.saida.parent.mkdir(parents=True, exist_ok=True)
    with arguments.saida.open("w", encoding="ascii", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
