import argparse
from pathlib import Path

from algoritmos import merge_sort, quick_sort


def read_values(path: Path) -> list[float]:
    with path.open(encoding="ascii") as file:
        return [float(line) for line in file if line.strip()]


def write_values(path: Path, values: list[float]) -> None:
    with path.open("w", encoding="ascii", newline="\n") as file:
        for value in values:
            file.write(f"{value:.17g}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("algoritmo", choices=("quick", "merge"))
    parser.add_argument("entrada", type=Path)
    parser.add_argument("saida", type=Path, nargs="?")
    arguments = parser.parse_args()
    values = read_values(arguments.entrada)
    if arguments.algoritmo == "quick":
        quick_sort(values)
    else:
        merge_sort(values)
    if arguments.saida is not None:
        write_values(arguments.saida, values)


if __name__ == "__main__":
    main()
