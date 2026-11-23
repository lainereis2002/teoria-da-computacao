# 📊 Análise de Complexidade: Quick Sort × Merge Sort

## 📋 Descrição do projeto

Este projeto de Teoria da Computação compara o comportamento teórico e experimental dos algoritmos **Quick Sort** e **Merge Sort**, implementados em **C** e **Python**.

A análise considera:

- duas linguagens de programação;
- dois algoritmos de ordenação;
- três tamanhos de entrada;
- cinco famílias de entrada;
- tempo real e tempo de CPU;
- estatísticas descritivas e crescimento assintótico.

### 🎯 Características principais

- **Quick Sort iterativo**, com partição de Lomuto e pivô no último elemento;
- **Merge Sort top-down estável**;
- Python com `float` e C com `double`;
- mesmos 150 arquivos usados nas quatro implementações;
- dez vetores por tamanho e família;
- vinte repetições de cada bloco;
- geração determinística com semente fixa 42;
- testes automatizados, relatórios numéricos e gráficos.

---

## 🏗️ Arquitetura do projeto

```text
teoria-da-computacao/
│
├── gerador/                    # Gerador determinístico das entradas
├── entradas/                   # 150 vetores persistidos e compartilhados
├── python/                     # Implementações e executor em Python
├── c/                          # Implementações e executor em C
├── medicao/                    # Medidores e controlador da coleta
├── testes/                     # Testes de corretude e validação
├── analise/                    # Resumo estatístico e gráficos
├── resultados/
│   ├── brutos/                 # Medições consolidadas
│   ├── resumos/                # Estatísticas das configurações
│   ├── graficos/               # Imagens produzidas pela análise
│   ├── estatisticas_detalhadas.txt
│   └── resultados_numericos.md
│
├── requirements.txt
├── plano-de-implementação.md
└── README.md
```

| Diretório | Responsabilidade |
|---|---|
| `gerador/` | Cria os valores-base e organiza as famílias de entrada. |
| `python/` e `c/` | Contêm os algoritmos e executores equivalentes. |
| `medicao/` | Mede tempo real e CPU e coordena as 60 configurações. |
| `testes/` | Verifica os algoritmos e as propriedades das entradas. |
| `analise/` | Calcula estatísticas e produz os gráficos. |
| `resultados/` | Reúne medições, relatório estatístico e imagens. |

---

## ⚙️ Configuração experimental

| Categoria | Elementos por vetor |
|---|---:|
| P | 1.000 |
| M | 4.000 |
| G | 16.000 |

| Família | Construção | Comportamento esperado |
|---|---|---|
| `aleatoria` | Valores-base em ordem pseudoaleatória | Caso médio esperado do Quick |
| `crescente` | Valores em ordem crescente | Pior caso do Quick utilizado |
| `inversa` | Valores em ordem decrescente | Pior caso do Quick utilizado |
| `melhor_quick` | Pivôs finais próximos da mediana | Partições equilibradas no Quick |
| `pior_merge` | Ordem que maximiza comparações do Merge | Merge permanece em Θ(n log n) |

```text
4 implementações × 5 famílias × 3 tamanhos × 20 blocos = 1.200 medições
1.200 blocos × 10 vetores = 12.000 ordenações
```

---

## 📦 Requisitos

- Ubuntu 26.04.1 LTS no WSL2;
- Python 3.14.4;
- GCC 15.2.0;
- GNU Make;
- Matplotlib 3.10.7 para os gráficos.

Verifique as ferramentas:

```bash
python3 --version
gcc --version
```

Instale a dependência dos gráficos:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

## 🔨 Compilação

Na raiz do projeto:

```bash
make -C gerador
make -C c
make -C testes
make -C medicao
```

Comandos equivalentes:

```bash
gcc -std=c11 -O2 -Wall -Wextra -Wpedantic gerador/gerar_entradas.c -o gerador/gerar_entradas.exe
gcc -std=c11 -O2 -Wall -Wextra -Wpedantic c/executar.c c/ordenacao.c -o c/executar.exe
gcc -std=c11 -O2 -Wall -Wextra -Wpedantic testes/test_ordenacao.c c/ordenacao.c -o testes/test_ordenacao.exe
gcc -std=c11 -O2 -Wall -Wextra -Wpedantic medicao/medir_c.c c/ordenacao.c -o medicao/medir_c.exe
```

## 🗂️ Geração das entradas

O gerador deve ser executado uma única vez:

```bash
./gerador/gerar_entradas.exe
```

Ele produz 150 arquivos persistentes:

```text
3 tamanhos × 10 vetores × 5 famílias = 150 arquivos
```

Os mesmos arquivos são reutilizados nas quatro implementações e em todas as repetições. Não ocorre geração aleatória durante a medição.

Os arquivos correspondentes às cinco famílias contêm os mesmos valores, mudando apenas a ordem. Cada arquivo possui um valor por linha, sem cabeçalho.

## ✅ Testes

Depois de compilar e gerar as entradas:

```bash
python3 -m unittest discover -s testes -p "test_*.py"
./testes/test_ordenacao.exe
python3 testes/validar_entradas.py
```

Os testes verificam:

- Quick e Merge em Python;
- Quick e Merge em C;
- igualdade das quatro respostas;
- casos-limite;
- 150 arquivos no manifesto;
- quantidade e unicidade dos valores;
- igualdade dos conjuntos-base;
- equilíbrio das partições do melhor caso do Quick;
- máximo de comparações do pior caso do Merge.

## 🧪 Piloto obrigatório

Antes da coleta completa, execute o caso potencialmente mais demorado:

```bash
python3 medicao/medir_python.py quick crescente G_16000 resultados/brutos/piloto_python_quick_crescente_G.csv --repeticoes 1 --aquecimentos 0
```

Também pode ser testada a entrada inversa:

```bash
python3 medicao/medir_python.py quick inversa G_16000 resultados/brutos/piloto_python_quick_inversa_G.csv --repeticoes 1 --aquecimentos 0
```

O piloto deve ser analisado antes de iniciar as vinte repetições de todas as configurações.

## ⏱️ Coleta

Para executar as 60 configurações:

```bash
python3 medicao/coletar.py
```

Cada configuração gera um arquivo parcial. A coleta pode ser retomada depois de uma interrupção, pois configurações já concluídas são preservadas.

Para refazer tudo:

```bash
python3 medicao/coletar.py --refazer
```

O resultado consolidado será salvo em:

```text
resultados/brutos/tempos.csv
```

A ordem das configurações é embaralhada de forma determinística com semente 42. Cada configuração contém vinte observações, totalizando:

```text
4 implementações × 5 famílias × 3 tamanhos × 20 blocos = 1.200 medições
```

Como cada bloco contém dez vetores:

```text
1.200 × 10 = 12.000 ordenações
```

## ⏲️ Região medida

Ficam fora do cronômetro:

- leitura dos arquivos;
- geração das entradas;
- cópia e restauração dos vetores;
- criação dos vetores auxiliares;
- impressão;
- validação da saída.

A região medida contém exclusivamente as dez chamadas de ordenação do bloco.

Python usa:

- `time.perf_counter()` para tempo real;
- `time.process_time()` para CPU.

C no Ubuntu/WSL2 usa:

- `clock_gettime(CLOCK_MONOTONIC)` para tempo real;
- `clock_gettime(CLOCK_PROCESS_CPUTIME_ID)` para CPU.

## 📋 Resumo estatístico

Depois da coleta:

```bash
python3 analise/resumir.py
python3 resultados/calcular_resultados.py
```

O arquivo `resultados/resumos/resumo.csv` contém:

- média;
- desvio padrão amostral;
- mediana;
- mínimo;
- máximo;
- primeiro e terceiro quartis;
- intervalo interquartil;
- erro padrão;
- intervalo de confiança de 95%;
- quantidade de observações.

O segundo comando também produz:

- `resultados/resultados_numericos.csv`;
- `resultados/resultados_numericos.md`;
- `resultados/estatisticas_detalhadas.txt`.

O relatório detalhado segue uma estrutura por linguagem, algoritmo, família e
tamanho, com média, desvio-padrão, coeficiente de variação, intervalo de
confiança de 95%, quartis, intervalo interquartil, mediana, mínimo e máximo
para tempo real e tempo de CPU.

## 📈 Gráficos

```bash
.venv/bin/python analise/graficos.py
```

Os 32 gráficos são salvos em `resultados/graficos` e incluem:

- Quick versus Merge;
- barras de desvio padrão;
- escala log-log;
- razões `T(n)/(n log n)` e `T(n)/n²`;
- aceleração Python/C;
- tempo real versus CPU;
- coeficiente de variação por algoritmo e linguagem;
- razão direta Quick/Merge, com referência de igualdade;
- boxplots das vinte repetições;
- expoente empírico de crescimento;
- comparação direta dos tempos absolutos de C e Python.

## ▶️ Execução completa

Na raiz do projeto, execute os comandos na seguinte ordem:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt

make -C gerador
make -C c
make -C testes
make -C medicao

./gerador/gerar_entradas.exe

python3 -m unittest discover -s testes -p "test_*.py"
./testes/test_ordenacao.exe
python3 testes/validar_entradas.py

python3 medicao/medir_python.py quick crescente G_16000 resultados/brutos/piloto_python_quick_crescente_G.csv --repeticoes 1 --aquecimentos 0

python3 medicao/coletar.py

python3 analise/resumir.py
python3 resultados/calcular_resultados.py
.venv/bin/python analise/graficos.py
```

## 🔄 Fluxo do experimento

```text
Gerar 150 entradas persistentes
              ↓
Validar conteúdo e propriedades
              ↓
Executar 60 configurações
              ↓
Medir 20 blocos de 10 vetores por configuração
              ↓
Consolidar 1.200 observações
              ↓
Calcular estatísticas e gerar gráficos
```

As quatro implementações recebem exatamente os mesmos arquivos, mantendo a
comparação pareada e reprodutível.

## 📊 Resultados

Os resultados sustentam as previsões teóricas principais:

1. Quick Sort apresentou crescimento quadrático nas entradas crescente e inversa;
2. Quick Sort permaneceu compatível com Θ(n log n) nas entradas aleatória e de melhor caso;
3. Merge Sort permaneceu em Θ(n log n) nas cinco famílias;
4. C foi mais rápido que Python nas comparações equivalentes;
5. Quick foi mais rápido com partições equilibradas, mas muito mais lento com partições degeneradas.

Documentos disponíveis:

- [estatísticas detalhadas](resultados/estatisticas_detalhadas.txt);
- [resultados numéricos](resultados/resultados_numericos.md);

## 🖥️ Ambiente a registrar

Antes da coleta oficial, registre:

```bash
python3 --version
gcc --version
uname -a
lsb_release -a
lscpu
free -h
```

O ambiente oficial utilizado foi:

- Ubuntu 26.04.1 LTS no WSL2;
- kernel `6.18.58.1-microsoft-standard-WSL2`;
- arquitetura x86-64;
- 5 CPUs virtuais;
- Intel Xeon Platinum 8368 a 2,40 GHz;
- 9,7 GiB de RAM disponíveis ao WSL;
- CPython 3.14.4;
- GCC 15.2.0;
- compilação C com `-std=c11 -O2 -Wall -Wextra -Wpedantic`.

O relatório também deve identificar o Windows hospedeiro e explicar que os experimentos foram executados no WSL2.

## 📝 Uso de IA

O projeto utiliza IA como apoio no planejamento, implementação, elaboração dos testes, revisão da metodologia, análise e documentação. Esse uso deve ser declarado no relatório, e todos os integrantes devem ser capazes de explicar o código e os resultados.

## 📚 Documentação complementar

O planejamento completo está em [plano-de-implementação.md](plano-de-implementação.md).
