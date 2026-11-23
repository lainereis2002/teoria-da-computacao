import csv
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "resultados" / "resumos" / "resumo.csv"
OUTPUT_CSV = ROOT / "resultados" / "resultados_numericos.csv"
OUTPUT_MD = ROOT / "resultados" / "resultados_numericos.md"
OUTPUT_DETAILED = ROOT / "resultados" / "estatisticas_detalhadas.txt"
FAMILY_LABELS = {
    "aleatoria": "Aleatória",
    "crescente": "Crescente",
    "inversa": "Inversa",
    "melhor_quick": "Melhor Quick",
    "pior_merge": "Pior Merge",
}
ALGORITHM_LABELS = {"quick": "Quick", "merge": "Merge"}
LANGUAGE_LABELS = {"python": "Python", "c": "C"}
SIZE_ORDER = {"P_1000": 0, "M_4000": 1, "G_16000": 2}


def theoretical_function(algorithm: str, family: str) -> str:
    if algorithm == "quick" and family in {"crescente", "inversa"}:
        return "n^2"
    return "n*log2(n)"


def theoretical_value(algorithm: str, family: str, n: int) -> float:
    if theoretical_function(algorithm, family) == "n^2":
        return float(n * n)
    return n * math.log2(n)


def read_rows() -> list[dict[str, str]]:
    with INPUT.open(encoding="ascii", newline="") as file:
        rows = list(csv.DictReader(file))
    if len(rows) != 60:
        raise ValueError(f"Eram esperadas 60 linhas; foram encontradas {len(rows)}.")
    return rows


def numeric_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            int(row["n"]),
        ): row
        for row in rows
    }
    results = []
    for row in rows:
        language = row["linguagem"]
        algorithm = row["algoritmo"]
        family = row["familia"]
        n = int(row["n"])
        wall_mean = float(row["tempo_real_medio_vetor_media"])
        wall_deviation = float(row["tempo_real_medio_vetor_desvio"])
        cpu_mean = float(row["tempo_cpu_medio_vetor_media"])
        theory = theoretical_value(algorithm, family, n)
        python_mean = float(
            indexed[("python", algorithm, family, n)]["tempo_real_medio_vetor_media"]
        )
        c_mean = float(indexed[("c", algorithm, family, n)]["tempo_real_medio_vetor_media"])
        quick_mean = float(
            indexed[(language, "quick", family, n)]["tempo_real_medio_vetor_media"]
        )
        merge_mean = float(
            indexed[(language, "merge", family, n)]["tempo_real_medio_vetor_media"]
        )
        results.append(
            {
                "linguagem": language,
                "algoritmo": algorithm,
                "familia": family,
                "tamanho_categoria": row["tamanho_categoria"],
                "n": str(n),
                "observacoes": row["observacoes"],
                "tempo_real_medio_vetor_s": f"{wall_mean:.9f}",
                "desvio_real_medio_vetor_s": f"{wall_deviation:.9f}",
                "coeficiente_variacao_percentual": f"{wall_deviation / wall_mean * 100:.6f}",
                "tempo_cpu_medio_vetor_s": f"{cpu_mean:.9f}",
                "razao_cpu_tempo_real": f"{cpu_mean / wall_mean:.6f}",
                "funcao_teorica": theoretical_function(algorithm, family),
                "valor_funcao_teorica": f"{theory:.9f}",
                "tempo_normalizado": f"{wall_mean / theory:.12e}",
                "aceleracao_python_sobre_c": f"{python_mean / c_mean:.6f}",
                "razao_quick_sobre_merge": f"{quick_mean / merge_mean:.6f}",
            }
        )
    return sorted(
        results,
        key=lambda row: (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            int(row["n"]),
        ),
    )


def write_csv(rows: list[dict[str, str]]) -> None:
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, str]]) -> None:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            int(row["n"]),
        ): row
        for row in rows
    }
    lines = [
        "# Resultados numéricos",
        "",
        "## Quick Sort dividido por Merge Sort",
        "",
        "| Linguagem | Família | n | Quick (s) | Merge (s) | Quick/Merge |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for language in ("python", "c"):
        for family in FAMILY_LABELS:
            for n in (1000, 4000, 16000):
                quick = indexed[(language, "quick", family, n)]
                merge = indexed[(language, "merge", family, n)]
                lines.append(
                    f"| {LANGUAGE_LABELS[language]} | {FAMILY_LABELS[family]} | {n} "
                    f"| {float(quick['tempo_real_medio_vetor_s']):.9f} "
                    f"| {float(merge['tempo_real_medio_vetor_s']):.9f} "
                    f"| {float(quick['razao_quick_sobre_merge']):.3f}× |"
                )
    lines.extend(
        [
            "",
            "## Aceleração de C em relação a Python",
            "",
            "| Algoritmo | Família | n | Python/C |",
            "|---|---|---:|---:|",
        ]
    )
    for algorithm in ("quick", "merge"):
        for family in FAMILY_LABELS:
            for n in (1000, 4000, 16000):
                row = indexed[("python", algorithm, family, n)]
                lines.append(
                    f"| {ALGORITHM_LABELS[algorithm]} | {FAMILY_LABELS[family]} | {n} "
                    f"| {float(row['aceleracao_python_sobre_c']):.3f}× |"
                )
    lines.extend(
        [
            "",
            "## Valores normalizados usados nos gráficos",
            "",
            "| Linguagem | Algoritmo | Família | n | Média (s) | Desvio (s) | f(n) | T(n)/f(n) | CPU/real |",
            "|---|---|---|---:|---:|---:|---|---:|---:|",
        ]
    )
    for row in rows:
        lines.append(
            f"| {LANGUAGE_LABELS[row['linguagem']]} "
            f"| {ALGORITHM_LABELS[row['algoritmo']]} "
            f"| {FAMILY_LABELS[row['familia']]} "
            f"| {row['n']} "
            f"| {float(row['tempo_real_medio_vetor_s']):.9f} "
            f"| {float(row['desvio_real_medio_vetor_s']):.9f} "
            f"| {row['funcao_teorica']} "
            f"| {float(row['tempo_normalizado']):.6e} "
            f"| {float(row['razao_cpu_tempo_real']):.4f} |"
        )
    OUTPUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_detailed_statistics(rows: list[dict[str, str]]) -> None:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            row["tamanho_categoria"],
        ): row
        for row in rows
    }
    separator = "=" * 80
    subsection = "-" * 80
    lines = [
        separator,
        "RELATÓRIO DE ESTATÍSTICAS DETALHADAS",
        "Análise de Complexidade - Quick Sort × Merge Sort",
        separator,
        "",
        "Cada observação representa a ordenação de um bloco com dez vetores.",
        "As estatísticas por vetor correspondem ao tempo do bloco dividido por dez.",
        "",
    ]
    for language in ("c", "python"):
        lines.extend(
            [
                separator,
                f"LINGUAGEM: {LANGUAGE_LABELS[language].upper()}",
                separator,
                "",
            ]
        )
        for algorithm in ("quick", "merge"):
            lines.extend(
                [
                    f"ALGORITMO: {ALGORITHM_LABELS[algorithm].upper()} SORT",
                    subsection,
                    "",
                ]
            )
            for family in FAMILY_LABELS:
                for size in SIZE_ORDER:
                    row = indexed[(language, algorithm, family, size)]
                    observations = int(row["observacoes"])
                    n = int(row["n"])
                    real_mean = float(row["tempo_real_medio_vetor_media"])
                    real_deviation = float(row["tempo_real_medio_vetor_desvio"])
                    cpu_mean = float(row["tempo_cpu_medio_vetor_media"])
                    cpu_deviation = float(row["tempo_cpu_medio_vetor_desvio"])
                    real_cv = real_deviation / real_mean * 100
                    cpu_cv = cpu_deviation / cpu_mean * 100
                    lines.extend(
                        [
                            (
                                f"{FAMILY_LABELS[family].upper()} - {size} "
                                f"(n = {n:,}):"
                            ).replace(",", "."),
                            subsection,
                            f"  Observações: {observations}",
                            "  Função teórica de referência: "
                            f"{theoretical_function(algorithm, family)}",
                            "",
                            "  TEMPO REAL POR VETOR:",
                            "    Média:                    "
                            f"{real_mean:.9f} segundos ({real_mean * 1000:.6f} ms)",
                            "    Desvio-padrão amostral:   "
                            f"{real_deviation:.9f} segundos "
                            f"({real_deviation * 1000:.6f} ms)",
                            f"    Coeficiente de variação:  {real_cv:.2f}%",
                            "    IC95% da média:           "
                            f"[{float(row['tempo_real_medio_vetor_ic95_inferior']):.9f}, "
                            f"{float(row['tempo_real_medio_vetor_ic95_superior']):.9f}] "
                            "segundos",
                            "    Mediana:                  "
                            f"{float(row['tempo_real_medio_vetor_mediana']):.9f} "
                            "segundos",
                            "    Primeiro quartil (Q1):    "
                            f"{float(row['tempo_real_medio_vetor_q1']):.9f} segundos",
                            "    Terceiro quartil (Q3):    "
                            f"{float(row['tempo_real_medio_vetor_q3']):.9f} segundos",
                            "    Intervalo interquartil:   "
                            f"{float(row['tempo_real_medio_vetor_iqr']):.9f} segundos",
                            "    Mínimo:                   "
                            f"{float(row['tempo_real_medio_vetor_minimo']):.9f} "
                            "segundos",
                            "    Máximo:                   "
                            f"{float(row['tempo_real_medio_vetor_maximo']):.9f} "
                            "segundos",
                            "",
                            "  TEMPO DE CPU POR VETOR:",
                            "    Média:                    "
                            f"{cpu_mean:.9f} segundos ({cpu_mean * 1000:.6f} ms)",
                            "    Desvio-padrão amostral:   "
                            f"{cpu_deviation:.9f} segundos "
                            f"({cpu_deviation * 1000:.6f} ms)",
                            f"    Coeficiente de variação:  {cpu_cv:.2f}%",
                            "    IC95% da média:           "
                            f"[{float(row['tempo_cpu_medio_vetor_ic95_inferior']):.9f}, "
                            f"{float(row['tempo_cpu_medio_vetor_ic95_superior']):.9f}] "
                            "segundos",
                            "    Mediana:                  "
                            f"{float(row['tempo_cpu_medio_vetor_mediana']):.9f} "
                            "segundos",
                            "    Primeiro quartil (Q1):    "
                            f"{float(row['tempo_cpu_medio_vetor_q1']):.9f} segundos",
                            "    Terceiro quartil (Q3):    "
                            f"{float(row['tempo_cpu_medio_vetor_q3']):.9f} segundos",
                            "    Intervalo interquartil:   "
                            f"{float(row['tempo_cpu_medio_vetor_iqr']):.9f} segundos",
                            "    Mínimo:                   "
                            f"{float(row['tempo_cpu_medio_vetor_minimo']):.9f} segundos",
                            "    Máximo:                   "
                            f"{float(row['tempo_cpu_medio_vetor_maximo']):.9f} segundos",
                            "",
                            "  TEMPO REAL DO BLOCO DE DEZ VETORES:",
                            "    Média:                    "
                            f"{float(row['tempo_real_bloco_media']):.9f} segundos",
                            "    Desvio-padrão amostral:   "
                            f"{float(row['tempo_real_bloco_desvio']):.9f} segundos",
                            "    Mediana:                  "
                            f"{float(row['tempo_real_bloco_mediana']):.9f} segundos",
                            "    Mínimo:                   "
                            f"{float(row['tempo_real_bloco_minimo']):.9f} segundos",
                            "    Máximo:                   "
                            f"{float(row['tempo_real_bloco_maximo']):.9f} segundos",
                            "",
                            f"  Razão CPU/tempo real:       {cpu_mean / real_mean:.6f}",
                            "",
                        ]
                    )
    lines.extend([separator, "FIM DO RELATÓRIO", separator])
    OUTPUT_DETAILED.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_main_results(rows: list[dict[str, str]]) -> None:
    indexed = {
        (
            row["linguagem"],
            row["algoritmo"],
            row["familia"],
            int(row["n"]),
        ): row
        for row in rows
    }
    print("QUICK / MERGE")
    print("linguagem;familia;n;quick_s;merge_s;quick_div_merge")
    for language in ("python", "c"):
        for family in FAMILY_LABELS:
            for n in (1000, 4000, 16000):
                quick = indexed[(language, "quick", family, n)]
                merge = indexed[(language, "merge", family, n)]
                print(
                    f"{language};{family};{n};"
                    f"{quick['tempo_real_medio_vetor_s']};"
                    f"{merge['tempo_real_medio_vetor_s']};"
                    f"{quick['razao_quick_sobre_merge']}"
                )
    print()
    print("PYTHON / C")
    print("algoritmo;familia;n;aceleracao_python_div_c")
    for algorithm in ("quick", "merge"):
        for family in FAMILY_LABELS:
            for n in (1000, 4000, 16000):
                row = indexed[("python", algorithm, family, n)]
                print(
                    f"{algorithm};{family};{n};"
                    f"{row['aceleracao_python_sobre_c']}"
                )


def main() -> None:
    summary_rows = read_rows()
    rows = numeric_rows(summary_rows)
    write_csv(rows)
    write_markdown(rows)
    write_detailed_statistics(summary_rows)
    print_main_results(rows)
    print()
    print(f"CSV numerico: {OUTPUT_CSV}")
    print(f"Relatorio numerico: {OUTPUT_MD}")
    print(f"Estatisticas detalhadas: {OUTPUT_DETAILED}")


if __name__ == "__main__":
    main()
