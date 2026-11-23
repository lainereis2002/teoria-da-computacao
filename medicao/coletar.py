import argparse
import csv
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / "resultados" / "brutos" / "partes"
RAW_OUTPUT = ROOT / "resultados" / "brutos" / "tempos.csv"
ALGORITHMS = ("quick", "merge")
FAMILIES = ("aleatoria", "crescente", "inversa", "melhor_quick", "pior_merge")
SIZES = ("P_1000", "M_4000", "G_16000")
LANGUAGES = ("python", "c")


def configuration_path(language: str, algorithm: str, family: str, size: str) -> Path:
    return PARTS / f"{language}_{algorithm}_{family}_{size}.csv"


def part_is_complete(path: Path, repetitions: int) -> bool:
    if not path.exists():
        return False
    try:
        with path.open(encoding="ascii", newline="") as file:
            rows = list(csv.DictReader(file))
    except (OSError, csv.Error):
        return False
    return len(rows) == repetitions and [
        int(row["repeticao"]) for row in rows
    ] == list(range(1, repetitions + 1))


def run_configuration(
    language: str,
    algorithm: str,
    family: str,
    size: str,
    repetitions: int,
    warmups: int,
) -> None:
    output = configuration_path(language, algorithm, family, size)
    if language == "python":
        command = [
            sys.executable,
            str(ROOT / "medicao" / "medir_python.py"),
            algorithm,
            family,
            size,
            str(output),
            "--repeticoes",
            str(repetitions),
            "--aquecimentos",
            str(warmups),
        ]
    else:
        command = [
            str(ROOT / "medicao" / "medir_c.exe"),
            algorithm,
            family,
            size,
            str(repetitions),
            str(warmups),
            str(output),
        ]
    subprocess.run(command, cwd=ROOT, check=True)


def combine_results(configurations: list[tuple[str, str, str, str]]) -> None:
    rows = []
    fieldnames = None
    for configuration in configurations:
        path = configuration_path(*configuration)
        with path.open(encoding="ascii", newline="") as file:
            reader = csv.DictReader(file)
            if fieldnames is None:
                fieldnames = reader.fieldnames
            rows.extend(reader)
    if fieldnames is None:
        raise ValueError("Nenhum resultado foi produzido.")
    RAW_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with RAW_OUTPUT.open("w", encoding="ascii", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repeticoes", type=int, default=20)
    parser.add_argument("--aquecimentos", type=int, default=2)
    parser.add_argument("--refazer", action="store_true")
    arguments = parser.parse_args()
    if arguments.repeticoes < 1 or arguments.aquecimentos < 0:
        parser.error("Repeticoes deve ser positiva e aquecimentos nao pode ser negativo.")
    executable = ROOT / "medicao" / "medir_c.exe"
    if not executable.exists():
        raise FileNotFoundError("Compile medicao/medir_c.exe antes da coleta.")
    configurations = [
        (language, algorithm, family, size)
        for language in LANGUAGES
        for algorithm in ALGORITHMS
        for family in FAMILIES
        for size in SIZES
    ]
    random.Random(42).shuffle(configurations)
    PARTS.mkdir(parents=True, exist_ok=True)
    for index, configuration in enumerate(configurations, 1):
        output = configuration_path(*configuration)
        if arguments.refazer or not part_is_complete(output, arguments.repeticoes):
            print(f"[{index:02d}/{len(configurations)}] {'/'.join(configuration)}", flush=True)
            run_configuration(
                *configuration,
                repetitions=arguments.repeticoes,
                warmups=arguments.aquecimentos,
            )
    combine_results(configurations)
    print(f"Coleta consolidada em {RAW_OUTPUT}.")


if __name__ == "__main__":
    main()
