import csv
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "resultados" / "resumos" / "resumo.csv"
RAW_INPUT = ROOT / "resultados" / "brutos" / "tempos.csv"
OUTPUT = ROOT / "resultados" / "graficos"
FAMILY_LABELS = {
    "aleatoria": "Aleatória",
    "crescente": "Crescente",
    "inversa": "Inversa",
    "melhor_quick": "Melhor Quick",
    "pior_merge": "Pior Merge",
}
ALGORITHM_LABELS = {"quick": "Quick Sort", "merge": "Merge Sort"}
LANGUAGE_LABELS = {"python": "Python", "c": "C"}
SIZE_ORDER = ("P_1000", "M_4000", "G_16000")
SIZE_LABELS = {"P_1000": "P", "M_4000": "M", "G_16000": "G"}
FAMILY_COLORS = {
    "aleatoria": "#4C78A8",
    "crescente": "#F58518",
    "inversa": "#E45756",
    "melhor_quick": "#54A24B",
    "pior_merge": "#B279A2",
}


def read_rows() -> list[dict[str, str]]:
    with INPUT.open(encoding="ascii", newline="") as file:
        return list(csv.DictReader(file))


def read_raw_rows() -> list[dict[str, str]]:
    with RAW_INPUT.open(encoding="ascii", newline="") as file:
        return list(csv.DictReader(file))


def save_figure(name: str) -> None:
    plt.tight_layout()
    plt.savefig(OUTPUT / name, dpi=180)
    plt.close()


def plot_algorithm_comparisons(rows: list[dict[str, str]]) -> None:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["linguagem"], row["familia"])].append(row)
    for (language, family), values in groups.items():
        plt.figure(figsize=(7, 4.5))
        for algorithm in ("quick", "merge"):
            series = sorted(
                (row for row in values if row["algoritmo"] == algorithm),
                key=lambda row: int(row["n"]),
            )
            n_values = [int(row["n"]) for row in series]
            means = [float(row["tempo_real_medio_vetor_media"]) for row in series]
            deviations = [float(row["tempo_real_medio_vetor_desvio"]) for row in series]
            plt.errorbar(
                n_values,
                means,
                yerr=deviations,
                marker="o",
                capsize=4,
                label=ALGORITHM_LABELS[algorithm],
            )
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Quantidade de elementos (n)")
        plt.ylabel("Tempo real médio por vetor (s)")
        plt.title(f"{LANGUAGE_LABELS[language]} — {FAMILY_LABELS[family]}")
        plt.grid(True, which="both", alpha=0.25)
        plt.legend()
        save_figure(f"algoritmos_{language}_{family}.png")


def theoretical_value(algorithm: str, family: str, n: int) -> float:
    if algorithm == "quick" and family in {"crescente", "inversa"}:
        return float(n * n)
    return n * math.log2(n)


def plot_normalized(rows: list[dict[str, str]]) -> None:
    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["linguagem"], row["algoritmo"])].append(row)
    for (language, algorithm), values in groups.items():
        plt.figure(figsize=(7, 4.5))
        for family in FAMILY_LABELS:
            series = sorted(
                (row for row in values if row["familia"] == family),
                key=lambda row: int(row["n"]),
            )
            n_values = [int(row["n"]) for row in series]
            ratios = [
                float(row["tempo_real_medio_vetor_media"])
                / theoretical_value(algorithm, family, int(row["n"]))
                for row in series
            ]
            plt.plot(n_values, ratios, marker="o", label=FAMILY_LABELS[family])
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Quantidade de elementos (n)")
        plt.ylabel("T(n) / f(n)")
        plt.title(
            f"Normalização — {LANGUAGE_LABELS[language]} — {ALGORITHM_LABELS[algorithm]}"
        )
        plt.grid(True, which="both", alpha=0.25)
        plt.legend()
        save_figure(f"normalizacao_{language}_{algorithm}.png")


def plot_speedup(rows: list[dict[str, str]]) -> None:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            int(row["n"]),
        ): row
        for row in rows
    }
    for algorithm in ALGORITHM_LABELS:
        plt.figure(figsize=(7, 4.5))
        for family in FAMILY_LABELS:
            n_values = sorted(
                {
                    key[3]
                    for key in indexed
                    if key[1] == algorithm and key[2] == family
                }
            )
            speedups = []
            for n in n_values:
                python_time = float(
                    indexed[("python", algorithm, family, n)][
                        "tempo_real_medio_vetor_media"
                    ]
                )
                c_time = float(
                    indexed[("c", algorithm, family, n)]["tempo_real_medio_vetor_media"]
                )
                speedups.append(python_time / c_time)
            plt.plot(n_values, speedups, marker="o", label=FAMILY_LABELS[family])
        plt.xscale("log")
        plt.xlabel("Quantidade de elementos (n)")
        plt.ylabel("Aceleração Python / C")
        plt.title(f"Fator de aceleração — {ALGORITHM_LABELS[algorithm]}")
        plt.grid(True, which="both", alpha=0.25)
        plt.legend()
        save_figure(f"aceleracao_{algorithm}.png")


def plot_wall_cpu(rows: list[dict[str, str]]) -> None:
    for language in LANGUAGE_LABELS:
        selected = [row for row in rows if row["linguagem"] == language]
        wall = [float(row["tempo_real_bloco_media"]) for row in selected]
        cpu = [float(row["tempo_cpu_bloco_media"]) for row in selected]
        maximum = max([*wall, *cpu])
        plt.figure(figsize=(5.5, 5.5))
        plt.scatter(wall, cpu, alpha=0.75)
        plt.plot([0, maximum], [0, maximum], linestyle="--", color="black")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Tempo real médio do bloco (s)")
        plt.ylabel("Tempo de CPU médio do bloco (s)")
        plt.title(f"Tempo real × CPU — {LANGUAGE_LABELS[language]}")
        plt.grid(True, which="both", alpha=0.25)
        save_figure(f"tempo_real_cpu_{language}.png")


def plot_variability(rows: list[dict[str, str]]) -> None:
    for algorithm in ALGORITHM_LABELS:
        figure, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True)
        for axis, language in zip(axes, LANGUAGE_LABELS, strict=True):
            for family in FAMILY_LABELS:
                series = sorted(
                    (
                        row
                        for row in rows
                        if row["linguagem"] == language
                        and row["algoritmo"] == algorithm
                        and row["familia"] == family
                    ),
                    key=lambda row: int(row["n"]),
                )
                n_values = [int(row["n"]) for row in series]
                coefficients = [
                    float(row["tempo_real_medio_vetor_desvio"])
                    / float(row["tempo_real_medio_vetor_media"])
                    * 100
                    for row in series
                ]
                axis.plot(
                    n_values,
                    coefficients,
                    marker="o",
                    color=FAMILY_COLORS[family],
                    label=FAMILY_LABELS[family],
                )
            axis.axhline(10, color="black", linestyle="--", alpha=0.6)
            axis.set_xscale("log")
            axis.set_yscale("log")
            axis.set_xlabel("Quantidade de elementos (n)")
            axis.set_title(LANGUAGE_LABELS[language])
            axis.grid(True, which="both", alpha=0.25)
        axes[0].set_ylabel("Coeficiente de variação (%)")
        axes[1].legend(fontsize=8)
        figure.suptitle(f"Variabilidade — {ALGORITHM_LABELS[algorithm]}")
        save_figure(f"variabilidade_{algorithm}.png")


def plot_algorithm_ratio(rows: list[dict[str, str]]) -> None:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            int(row["n"]),
        ): row
        for row in rows
    }
    for language in LANGUAGE_LABELS:
        plt.figure(figsize=(7, 4.8))
        for family in FAMILY_LABELS:
            n_values = sorted(
                {
                    key[3]
                    for key in indexed
                    if key[0] == language and key[2] == family
                }
            )
            ratios = [
                float(
                    indexed[(language, "quick", family, n)][
                        "tempo_real_medio_vetor_media"
                    ]
                )
                / float(
                    indexed[(language, "merge", family, n)][
                        "tempo_real_medio_vetor_media"
                    ]
                )
                for n in n_values
            ]
            plt.plot(
                n_values,
                ratios,
                marker="o",
                color=FAMILY_COLORS[family],
                label=FAMILY_LABELS[family],
            )
        plt.axhline(1, color="black", linestyle="--", label="Mesmo tempo")
        plt.xscale("log")
        plt.yscale("log")
        plt.xlabel("Quantidade de elementos (n)")
        plt.ylabel("Tempo Quick / tempo Merge")
        plt.title(f"Quick Sort ÷ Merge Sort — {LANGUAGE_LABELS[language]}")
        plt.grid(True, which="both", alpha=0.25)
        plt.legend(fontsize=8)
        save_figure(f"razao_quick_merge_{language}.png")


def plot_distributions(raw_rows: list[dict[str, str]]) -> None:
    groups: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)
    for row in raw_rows:
        groups[
            (
                row["linguagem"],
                row["algoritmo"],
                row["familia"],
                row["tamanho_categoria"],
            )
        ].append(float(row["tempo_real_medio_vetor"]))
    for language in LANGUAGE_LABELS:
        for algorithm in ALGORITHM_LABELS:
            values = []
            labels = []
            colors = []
            for family in FAMILY_LABELS:
                for size in SIZE_ORDER:
                    values.append(groups[(language, algorithm, family, size)])
                    labels.append(f"{FAMILY_LABELS[family]}\n{SIZE_LABELS[size]}")
                    colors.append(FAMILY_COLORS[family])
            figure, axis = plt.subplots(figsize=(13, 5.5))
            boxes = axis.boxplot(
                values,
                tick_labels=labels,
                patch_artist=True,
                showfliers=True,
            )
            for box, color in zip(boxes["boxes"], colors, strict=True):
                box.set_facecolor(color)
                box.set_alpha(0.7)
            axis.set_yscale("log")
            axis.set_ylabel("Tempo real médio por vetor (s)")
            axis.set_title(
                f"Distribuição das 20 repetições — "
                f"{LANGUAGE_LABELS[language]} — {ALGORITHM_LABELS[algorithm]}"
            )
            axis.grid(True, which="both", axis="y", alpha=0.25)
            axis.tick_params(axis="x", labelrotation=45, labelsize=8)
            figure.subplots_adjust(bottom=0.27)
            save_figure(f"distribuicao_{language}_{algorithm}.png")


def plot_empirical_growth(rows: list[dict[str, str]]) -> None:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            row["tamanho_categoria"],
        ): row
        for row in rows
    }
    transitions = tuple(zip(SIZE_ORDER, SIZE_ORDER[1:]))
    transition_labels = [
        f"{SIZE_LABELS[start]} → {SIZE_LABELS[end]}" for start, end in transitions
    ]
    n_log_n_reference = []
    for start, end in transitions:
        start_n = int(indexed[("c", "quick", "aleatoria", start)]["n"])
        end_n = int(indexed[("c", "quick", "aleatoria", end)]["n"])
        n_log_n_reference.append(
            math.log(
                end_n * math.log2(end_n) / (start_n * math.log2(start_n))
            )
            / math.log(end_n / start_n)
        )
    for language in LANGUAGE_LABELS:
        for algorithm in ALGORITHM_LABELS:
            plt.figure(figsize=(7, 4.8))
            for family in FAMILY_LABELS:
                exponents = []
                for start, end in transitions:
                    start_row = indexed[(language, algorithm, family, start)]
                    end_row = indexed[(language, algorithm, family, end)]
                    start_time = float(start_row["tempo_real_medio_vetor_media"])
                    end_time = float(end_row["tempo_real_medio_vetor_media"])
                    start_n = int(start_row["n"])
                    end_n = int(end_row["n"])
                    exponents.append(
                        math.log(end_time / start_time)
                        / math.log(end_n / start_n)
                    )
                plt.plot(
                    transition_labels,
                    exponents,
                    marker="o",
                    color=FAMILY_COLORS[family],
                    label=FAMILY_LABELS[family],
                )
            plt.plot(
                transition_labels,
                n_log_n_reference,
                color="black",
                linestyle="--",
                label="Referência n log₂(n)",
            )
            plt.axhline(2, color="gray", linestyle=":", label="Referência n²")
            plt.ylabel("Expoente empírico p")
            plt.title(
                f"Crescimento empírico — "
                f"{LANGUAGE_LABELS[language]} — {ALGORITHM_LABELS[algorithm]}"
            )
            plt.grid(True, alpha=0.25)
            plt.legend(fontsize=8)
            save_figure(f"crescimento_{language}_{algorithm}.png")


def plot_language_comparison(rows: list[dict[str, str]]) -> None:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            row["tamanho_categoria"],
        ): row
        for row in rows
    }
    labels = [
        f"{FAMILY_LABELS[family]}\n{SIZE_LABELS[size]}"
        for family in FAMILY_LABELS
        for size in SIZE_ORDER
    ]
    positions = list(range(len(labels)))
    width = 0.38
    for algorithm in ALGORITHM_LABELS:
        c_values = [
            float(
                indexed[("c", algorithm, family, size)][
                    "tempo_real_medio_vetor_media"
                ]
            )
            for family in FAMILY_LABELS
            for size in SIZE_ORDER
        ]
        python_values = [
            float(
                indexed[("python", algorithm, family, size)][
                    "tempo_real_medio_vetor_media"
                ]
            )
            for family in FAMILY_LABELS
            for size in SIZE_ORDER
        ]
        figure, axis = plt.subplots(figsize=(13, 5.5))
        axis.bar(
            [position - width / 2 for position in positions],
            c_values,
            width,
            label="C",
        )
        axis.bar(
            [position + width / 2 for position in positions],
            python_values,
            width,
            label="Python",
        )
        axis.set_yscale("log")
        axis.set_xticks(positions, labels, rotation=45, ha="right")
        axis.set_ylabel("Tempo real médio por vetor (s)")
        axis.set_title(
            f"Comparação de tempo entre linguagens — "
            f"{ALGORITHM_LABELS[algorithm]}"
        )
        axis.grid(True, which="both", axis="y", alpha=0.25)
        axis.legend()
        figure.subplots_adjust(bottom=0.27)
        save_figure(f"linguagens_{algorithm}.png")


def main() -> None:
    rows = read_rows()
    raw_rows = read_raw_rows()
    if len(rows) != 60:
        raise ValueError(f"Eram esperadas 60 linhas de resumo; foram encontradas {len(rows)}.")
    if len(raw_rows) != 1200:
        raise ValueError(
            f"Eram esperadas 1.200 medições brutas; foram encontradas {len(raw_rows)}."
        )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    plot_algorithm_comparisons(rows)
    plot_normalized(rows)
    plot_speedup(rows)
    plot_wall_cpu(rows)
    plot_variability(rows)
    plot_algorithm_ratio(rows)
    plot_distributions(raw_rows)
    plot_empirical_growth(rows)
    plot_language_comparison(rows)
    print(f"32 graficos salvos em {OUTPUT}.")


if __name__ == "__main__":
    main()
