import csv
import math
import statistics
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "resultados" / "brutos" / "tempos.csv"
OUTPUT = ROOT / "resultados" / "resumos" / "resumo.csv"
KEY_FIELDS = ("linguagem", "algoritmo", "familia", "tamanho_categoria", "n")
METRICS = (
    "tempo_real_bloco",
    "tempo_cpu_bloco",
    "tempo_real_medio_vetor",
    "tempo_cpu_medio_vetor",
)
T_CRITICAL_95_DF_19 = 2.093024054


def main() -> None:
    groups: dict[tuple[str, ...], dict[str, list[float]]] = defaultdict(
        lambda: {metric: [] for metric in METRICS}
    )
    with INPUT.open(encoding="ascii", newline="") as file:
        for row in csv.DictReader(file):
            key = tuple(row[field] for field in KEY_FIELDS)
            for metric in METRICS:
                groups[key][metric].append(float(row[metric]))
    if not groups:
        raise ValueError("O arquivo de tempos nao possui observacoes.")
    fieldnames = [*KEY_FIELDS, "observacoes"]
    for metric in METRICS:
        fieldnames.extend(
            (
                f"{metric}_media",
                f"{metric}_desvio",
                f"{metric}_mediana",
                f"{metric}_minimo",
                f"{metric}_maximo",
                f"{metric}_q1",
                f"{metric}_q3",
                f"{metric}_iqr",
                f"{metric}_erro_padrao",
                f"{metric}_ic95_inferior",
                f"{metric}_ic95_superior",
            )
        )
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="ascii", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted(groups, key=lambda item: (item[0], item[1], item[2], int(item[4]))):
            values_by_metric = groups[key]
            counts = {len(values) for values in values_by_metric.values()}
            if len(counts) != 1:
                raise ValueError(f"Metricas incompletas para {key}.")
            count = counts.pop()
            row: dict[str, str | int] = dict(zip(KEY_FIELDS, key, strict=True))
            row["observacoes"] = count
            for metric, values in values_by_metric.items():
                deviation = statistics.stdev(values) if len(values) > 1 else 0.0
                q1, _, q3 = statistics.quantiles(values, n=4, method="inclusive")
                standard_error = deviation / math.sqrt(len(values))
                confidence_margin = T_CRITICAL_95_DF_19 * standard_error
                mean = statistics.fmean(values)
                row[f"{metric}_media"] = f"{statistics.fmean(values):.9f}"
                row[f"{metric}_desvio"] = f"{deviation:.9f}"
                row[f"{metric}_mediana"] = f"{statistics.median(values):.9f}"
                row[f"{metric}_minimo"] = f"{min(values):.9f}"
                row[f"{metric}_maximo"] = f"{max(values):.9f}"
                row[f"{metric}_q1"] = f"{q1:.9f}"
                row[f"{metric}_q3"] = f"{q3:.9f}"
                row[f"{metric}_iqr"] = f"{q3 - q1:.9f}"
                row[f"{metric}_erro_padrao"] = f"{standard_error:.9f}"
                row[f"{metric}_ic95_inferior"] = (
                    f"{max(0.0, mean - confidence_margin):.9f}"
                )
                row[f"{metric}_ic95_superior"] = f"{mean + confidence_margin:.9f}"
            writer.writerow(row)
    print(f"Resumo de {len(groups)} combinacoes salvo em {OUTPUT}.")


if __name__ == "__main__":
    main()
