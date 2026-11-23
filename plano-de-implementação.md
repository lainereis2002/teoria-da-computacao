# plano-de-implementação

## 1. Visão geral

Este projeto compara teórica e experimentalmente dois algoritmos de ordenação:

- Quick Sort com partição de Lomuto e pivô fixo no último elemento;
- Merge Sort top-down recursivo.

Cada algoritmo será implementado em duas linguagens:

- Python;
- C.

O projeto terá quatro implementações no total, todas executadas sobre exatamente as mesmas entradas. Os dados representarão índices sintéticos de eficiência de CPU usados para produzir um ranking de máquinas monitoradas.

O professor autorizou:

- uso de três tamanhos de entrada: P, M e G;
- dez vetores diferentes para cada tamanho e família;
- medição de um bloco contendo os dez vetores;
- vinte execuções de cada bloco;
- uso integral de IA, desde que declarado no relatório.

O prazo oficial atualizado é 20/11/2026.

---

## 2. Decisões confirmadas

| Item | Decisão |
|---|---|
| Problema | Ordenação |
| Algoritmo A | Quick Sort com pivô fixo no último elemento |
| Partição do Quick | Lomuto |
| Algoritmo B | Merge Sort |
| Linguagens | Python e C |
| Sistema de medição | Ubuntu 26.04.1 LTS no WSL2 |
| Compilador C | GCC 15.2.0 para Linux x86-64 |
| Otimização do C | `-O2` |
| Interpretador | CPython 3.14.4 |
| Tipo em Python | `float` |
| Tipo em C | `double` |
| Tamanho P | 1.000 elementos |
| Tamanho M | 4.000 elementos |
| Tamanho G | 16.000 elementos |
| Famílias | 5 |
| Vetores por tamanho e família | 10 |
| Repetições de cada bloco | 20 |
| Semente do gerador | 42 |
| Linguagem do gerador | C |
| Formato dos arquivos | Um valor por linha, sem cabeçalho |
| Valores | Únicos, de 0 a 100, com seis casas decimais |
| NaN e infinito | Não permitidos |
| Memória | Somente depois da conclusão dos requisitos obrigatórios |

Embora o enunciado geral mencione no mínimo seis tamanhos, o professor autorizou especificamente o uso de P, M e G, com dez vetores para cada tamanho.

---

## 3. Objetivos

### 3.1 Objetivo geral

Comparar o comportamento teórico e experimental do Quick Sort e do Merge Sort em Python e C, considerando diferentes tamanhos e formatos de entrada.

### 3.2 Objetivos específicos

- implementar corretamente os dois algoritmos nas duas linguagens;
- executar as quatro implementações sobre as mesmas entradas;
- analisar melhor caso, caso médio e pior caso;
- medir tempo real e tempo de CPU;
- calcular média e desvio padrão;
- comparar os resultados medidos com as funções assintóticas esperadas;
- comparar Quick Sort e Merge Sort;
- comparar Python e C;
- garantir a corretude com testes automatizados;
- discutir a aplicabilidade prática de cada algoritmo;
- discutir ordenação por reversões sem sinal como problema vizinho NP-difícil;
- disponibilizar código, entradas, resultados e instruções de reprodução no GitHub.

---

## 4. Famílias de entrada

Serão utilizadas cinco famílias.

| Família | Construção | Quick Sort | Merge Sort tradicional |
|---|---|---|---|
| Aleatória | Valores-base em ordem pseudoaleatória | Caso médio esperado, Θ(n log n) | Θ(n log n) |
| Crescente | Valores-base ordenados crescentemente | Pior caso, Θ(n²) | Menor número de comparações, mas Θ(n log n) |
| Inversa | Valores-base ordenados decrescentemente | Pior caso, Θ(n²) | Poucas comparações por intercalação, mas Θ(n log n) |
| Melhor Quick | Disposição que deixa o pivô final próximo da mediana em todas as partições | Melhor caso, Θ(n log n) | Θ(n log n) |
| Pior Merge | Disposição que maximiza a alternância entre as metades durante as intercalações | O comportamento será observado, sem classificação presumida | Máximo de comparações, mas Θ(n log n) |

No Merge Sort top-down tradicional, melhor caso, caso médio e pior caso permanecem em Θ(n log n). As famílias crescente e de pior caso diferem no número exato de comparações, mas não na classe assintótica.

O Merge Sort não terá o atalho que deixa de intercalar quando os dois subvetores já estão globalmente ordenados.

---

## 5. Tamanhos e quantidade de dados

### 5.1 Tamanhos

| Categoria | Elementos por vetor |
|---|---:|
| P | 1.000 |
| M | 4.000 |
| G | 16.000 |

### 5.2 Arquivos de entrada

Para cada tamanho serão gerados:

- 10 conjuntos-base;
- 5 disposições de cada conjunto-base, uma para cada família.

Quantidade total:

```text
3 tamanhos × 10 vetores × 5 famílias = 150 arquivos
```

Os arquivos correspondentes nas cinco famílias terão exatamente o mesmo conjunto de valores, mudando apenas a ordem.

Exemplo:

```text
entradas/P_1000/aleatoria/vetor_01.txt
entradas/P_1000/crescente/vetor_01.txt
entradas/P_1000/inversa/vetor_01.txt
entradas/P_1000/melhor_quick/vetor_01.txt
entradas/P_1000/pior_merge/vetor_01.txt
```

### 5.3 Formato

Cada arquivo terá:

- um valor por linha;
- nenhuma linha de cabeçalho;
- ponto como separador decimal;
- seis casas decimais;
- codificação textual consistente;
- exatamente 1.000, 4.000 ou 16.000 linhas, conforme a categoria.

---

## 6. Gerador de entradas

Será criado um único programa em C responsável por gerar todos os 150 arquivos.

O gerador será executado uma única vez antes dos experimentos. Os 150 arquivos
produzidos serão persistidos e reutilizados, sem qualquer nova geração aleatória,
pelos dois algoritmos, pelas duas linguagens e por todas as vinte repetições. A
semente existe para permitir a reprodução futura do mesmo conjunto de arquivos,
e não para gerar novos valores durante a coleta.

### 6.1 Reprodutibilidade

- usar a semente fixa 42;
- preferir um gerador pseudoaleatório implementado explicitamente, em vez de depender da sequência específica de `rand()` de uma biblioteca;
- registrar no README o algoritmo pseudoaleatório e a semente;
- gerar sempre os arquivos com os mesmos nomes e na mesma ordem;
- criar um manifesto com tamanho, família, índice do vetor e quantidade de valores;
- opcionalmente registrar checksums para detectar alterações acidentais.

### 6.2 Valores

- intervalo de 0 a 100;
- seis casas decimais;
- valores únicos dentro de cada conjunto-base;
- nenhum NaN;
- nenhum infinito;
- valores representáveis e ordenáveis de forma consistente em Python e C.

Uma estratégia possível é gerar unidades inteiras entre 0 e 100.000.000 e escrever cada valor dividido por 1.000.000. Isso garante seis casas decimais e facilita o controle de unicidade.

### 6.3 Processo de geração

Para cada categoria P, M e G e para cada índice de 1 a 10:

1. gerar um conjunto-base de valores únicos;
2. produzir a disposição aleatória;
3. produzir a disposição crescente;
4. produzir a disposição inversa;
5. produzir a disposição de melhor caso do Quick Sort;
6. produzir a disposição de máximo de comparações do Merge Sort;
7. salvar cada disposição em seu arquivo;
8. validar a quantidade e a unicidade;
9. validar que as cinco disposições contêm exatamente os mesmos valores.

### 6.4 Validação do melhor caso do Quick

Uma versão instrumentada do Quick Sort deverá verificar:

- tamanho de cada partição;
- posição final de cada pivô;
- diferença máxima de um elemento entre as partições;
- número total de comparações;
- ausência de partições persistentemente desbalanceadas.

Não basta colocar a mediana no fim apenas uma vez. A propriedade precisa ser preservada recursivamente em todos os subvetores formados pela partição de Lomuto.

### 6.5 Validação do pior caso de comparações do Merge

Uma versão instrumentada do Merge Sort deverá contar comparações e conferir se a construção provoca a alternância esperada entre as metades.

Para potências de dois, o máximo clássico é:

```text
n log₂(n) - n + 1
```

Como os tamanhos escolhidos não são todos potências de dois, a validação usará a recorrência correspondente às divisões reais feitas pela implementação.

As versões instrumentadas serão usadas apenas para validar as entradas. Os contadores não ficarão ativos durante a medição oficial.

---

## 7. Implementações

## 7.1 Requisitos comuns

As quatro implementações devem:

- usar a mesma lógica algorítmica nas duas linguagens;
- ler os mesmos arquivos;
- ordenar em ordem crescente;
- não incluir leitura, escrita, geração ou impressão na região medida;
- não usar funções prontas de ordenação dentro dos algoritmos;
- preservar uma cópia original de cada entrada;
- restaurar os vetores fora da região medida;
- tornar o resultado observável para impedir eliminação pelo compilador;
- validar o resultado fora da região medida.

Em Python, `sort()` e `sorted()` serão permitidos somente nos testes de referência, nunca na implementação dos algoritmos.

## 7.2 Quick Sort

Características:

- partição de Lomuto;
- pivô no último elemento;
- política de comparação definida de forma idêntica em Python e C;
- implementação iterativa;
- pilha explícita;
- processamento imediato da partição menor;
- manutenção da partição maior na pilha;
- uso esperado de O(log n) de memória auxiliar.

O Quick Sort reorganiza os elementos no próprio vetor, mas não deve ser descrito como estritamente O(1) de memória, pois a implementação usa uma pilha explícita.

Classificação:

| Caso | Tempo |
|---|---|
| Melhor | Θ(n log n) |
| Médio esperado | Θ(n log n) |
| Pior | Θ(n²) |

## 7.3 Merge Sort

Características:

- top-down recursivo;
- divisão pelo ponto médio;
- profundidade O(log n);
- vetor auxiliar reutilizado;
- intercalação estável com `<=`;
- sem atalho para subvetores já ordenados.

Classificação:

| Caso | Tempo |
|---|---|
| Melhor | Θ(n log n) |
| Médio | Θ(n log n) |
| Pior | Θ(n log n) |
| Memória auxiliar | Θ(n) |

O vetor auxiliar poderá ser preparado fora do cronômetro e reutilizado, desde que isso seja declarado na metodologia. O custo das cópias e intercalações continuará dentro da medição.

---

## 8. Testes de corretude

Os testes automatizados deverão verificar que as quatro implementações produzem a mesma resposta.

### 8.1 Referência

- usar `sorted()` do Python somente no ambiente de testes;
- comparar cada saída diretamente com a referência;
- evitar depender apenas de hashes;
- verificar ordem não decrescente;
- verificar preservação da quantidade e multiplicidade dos valores.

### 8.2 Casos de teste

- vetor vazio;
- um elemento;
- dois elementos em ordem;
- dois elementos invertidos;
- tamanho par;
- tamanho ímpar;
- entrada crescente;
- entrada inversa;
- valores repetidos;
- valores negativos;
- valores decimais;
- melhor caso construído do Quick;
- pior caso construído do Merge;
- amostras dos arquivos P, M e G.

Embora os experimentos oficiais usem valores únicos e não negativos, os algoritmos devem funcionar também com repetidos e negativos.

### 8.3 Comparação entre linguagens

As saídas poderão ser exportadas temporariamente pelos executáveis de teste e comparadas por um controlador. Essa exportação não fará parte da medição de desempenho.

---

## 9. Metodologia de medição

### 9.1 Unidade experimental

Uma execução medida será um bloco contendo a ordenação dos dez vetores de uma combinação de:

- linguagem;
- algoritmo;
- família;
- tamanho.

Cada bloco será repetido vinte vezes.

### 9.2 Processo de um bloco

1. carregar os dez arquivos fora da medição;
2. preparar ou restaurar as dez cópias fora da medição;
3. iniciar o cronômetro de tempo real;
4. iniciar ou consultar o cronômetro de CPU;
5. ordenar sequencialmente os dez vetores;
6. parar os cronômetros;
7. registrar o tempo total do bloco;
8. validar os dez resultados fora da medição;
9. restaurar os vetores fora da medição;
10. seguir para a próxima repetição.

### 9.3 Quantidade

```text
4 implementações × 5 famílias × 3 tamanhos × 20 blocos
= 1.200 medições
```

Cada bloco contém dez ordenações:

```text
1.200 blocos × 10 vetores = 12.000 ordenações
```

### 9.4 Cronômetros

Python:

- tempo real: `time.perf_counter()`;
- tempo de CPU: `time.process_time()`.

C no Ubuntu/WSL2:

- tempo real: `clock_gettime(CLOCK_MONOTONIC)`;
- tempo de CPU do processo: `clock_gettime(CLOCK_PROCESS_CPUTIME_ID)`.

### 9.5 Aquecimento

O CPython não usa JIT no cenário planejado, mas serão permitidos blocos de aquecimento previamente definidos e descartados para estabilizar:

- carregamento de páginas;
- bibliotecas;
- caches;
- frequência da CPU.

A quantidade de aquecimentos será igual para todas as combinações e será definida antes da coleta. Resultados não serão descartados depois de observados.

### 9.6 Controle do ambiente

Durante a coleta:

- usar a mesma máquina;
- manter o equipamento conectado à tomada;
- usar o mesmo modo de energia;
- fechar aplicações desnecessárias;
- evitar atualizações e tarefas pesadas em segundo plano;
- não executar outras cargas simultâneas;
- registrar CPU, RAM, Ubuntu, WSL2 e kernel;
- registrar o sistema Windows hospedeiro;
- registrar versão do Python;
- registrar versão do GCC;
- registrar arquitetura;
- registrar flags de compilação;
- manter constantes as condições entre Python e C.

### 9.7 Ordem de execução

A ordem dos blocos deverá ser equilibrada ou pseudoaleatorizada de forma reprodutível para reduzir viés de:

- aquecimento da máquina;
- temperatura;
- frequência dinâmica;
- mudanças graduais na carga do sistema.

Os dez vetores de cada bloco serão sempre identificáveis. Se a ordem interna for alterada, a mesma ordem deverá ser usada nas quatro implementações.

### 9.8 Prevenção contra otimização indevida

Depois da região medida:

- verificar que o vetor ficou ordenado;
- usar o resultado em uma validação ou checksum;
- garantir que o compilador não possa remover a chamada de ordenação.

A validação ocorre fora do cronômetro, mas torna o resultado computacionalmente observável.

---

## 10. Dados coletados

### 10.1 CSV bruto

Cada linha representará uma repetição de bloco e conterá:

```text
linguagem
algoritmo
familia
tamanho_categoria
n
repeticao
quantidade_vetores
tempo_real_bloco
tempo_cpu_bloco
tempo_real_medio_vetor
tempo_cpu_medio_vetor
ordem_execucao
semente
```

O tempo médio por vetor será:

```text
tempo do bloco / 10
```

### 10.2 Resumo estatístico

Para cada combinação serão calculados:

- número de observações;
- média;
- desvio padrão amostral;
- mediana;
- mínimo;
- máximo.

A média e o desvio padrão exigidos serão calculados sobre os vinte tempos de bloco.

O desvio padrão amostral usará denominador `n - 1`.

Nenhum outlier será removido sem uma regra objetiva definida previamente. Valores discrepantes serão mantidos e discutidos, quando necessário.

---

## 11. Análise teórica e experimental

### 11.1 Quick Sort

Melhor caso:

```text
T(n) = 2T(n/2) + Θ(n)
T(n) = Θ(n log n)
```

Pior caso:

```text
T(n) = T(n - 1) + Θ(n)
T(n) = Θ(n²)
```

Caso médio esperado:

```text
Θ(n log n)
```

### 11.2 Merge Sort

```text
T(n) = T(⌊n/2⌋) + T(⌈n/2⌉) + Θ(n)
T(n) = Θ(n log n)
```

Essa classificação vale para melhor caso, caso médio e pior caso na implementação tradicional planejada.

### 11.3 Uso correto de O, Ω e Θ

O relatório deve distinguir:

- limite superior O;
- limite inferior Ω;
- limite assintoticamente justo Θ;
- classificação por caso;
- classificação global do algoritmo.

Não será atribuída uma única classe Θ ao Quick Sort sem indicar o caso, pois seu comportamento depende da entrada.

---

## 12. Gráficos e tabelas

### 12.1 Teórico versus medido

- gráfico log-log de tempo por tamanho;
- sobreposição de curvas teóricas escaladas;
- `T(n)/(n log n)` para comportamentos Θ(n log n);
- `T(n)/n²` para o pior caso do Quick;
- análise da estabilização aproximada das razões.

Em escala log-log, a inclinação de `n log n` não é exatamente 1 para valores finitos. Ela tende a 1 assintoticamente.

### 12.2 Algoritmo versus algoritmo

- Quick versus Merge para cada família;
- tempo real médio com barras de desvio padrão;
- tempo de CPU médio com barras de desvio padrão;
- destaque para a degradação quadrática do Quick.

### 12.3 Linguagem versus linguagem

- Python versus C;
- fator de aceleração `tempo Python / tempo C`;
- comparação separada por algoritmo, família e tamanho.

### 12.4 Tempo real versus CPU

- valores lado a lado;
- diferença entre tempo decorrido e CPU consumida;
- discussão de interferência do sistema.

### 12.5 Interpretação

Os gráficos não serão apresentados sem análise. O relatório deverá explicar:

- se os resultados acompanham a teoria;
- onde overhead domina;
- efeitos de cache;
- interferência da máquina;
- diferenças de constante entre linguagens;
- impacto da forma da entrada;
- limitações do experimento.

---

## 13. Aplicabilidade prática

O cenário será um ranking de eficiência de CPU de máquinas monitoradas.

Pontos para discussão:

- dados quase ordenados podem surgir quando o ranking muda pouco entre coletas;
- o Quick com pivô fixo no último elemento degrada nesse cenário;
- o Merge apresenta tempo previsível;
- o Merge usa memória auxiliar linear;
- o Merge é estável;
- o Quick planejado não é estável;
- estabilidade é útil quando máquinas têm a mesma pontuação e uma ordem secundária deve ser preservada;
- valores repetidos não fazem parte do experimento principal e isso será declarado como limitação;
- o Quick com pivô fixo é uma escolha didática;
- implementações reais costumam usar pivô aleatório, medianas, introsort, Timsort ou outras estratégias.

---

## 14. Memória opcional

O bônus de memória será realizado somente se:

- as quatro implementações estiverem corretas;
- os testes estiverem passando;
- a coleta obrigatória estiver concluída;
- gráficos e relatório obrigatório estiverem encaminhados.

Teoria:

| Algoritmo | Memória auxiliar |
|---|---|
| Quick iterativo com estratégia da menor partição | O(log n) |
| Merge Sort | O(n) |

Possíveis métricas:

- maior quantidade de intervalos na pilha explícita do Quick;
- maior profundidade recursiva do Merge;
- quantidade de elementos do vetor auxiliar;
- bytes explicitamente alocados em C;
- memória adicional medida em relação a uma linha de base.

Ferramentas de Python e C não devem ser comparadas diretamente sem explicar o que cada uma mede.

---

## 15. Reflexão sobre P e NP

### 15.1 Ordenação comum

Ordenação é resolvida em tempo polinomial. Mais precisamente, como problema funcional, pode ser classificada em FP. No vocabulário simplificado do enunciado, será descrita como tratável e pertencente a P.

O limite inferior para ordenação por comparações é:

```text
Ω(n log n)
```

O Merge Sort alcança Θ(n log n), sendo assintoticamente ótimo no modelo de comparação.

### 15.2 Problema vizinho

O problema vizinho é ordenação por reversões sem sinal:

- entrada: uma permutação;
- operação: inverter um segmento contíguo;
- objetivo: encontrar a menor quantidade de reversões que transforma a permutação na identidade.

### 15.3 Versão de decisão

Pergunta:

> É possível ordenar a permutação usando no máximo k reversões?

Ela está em NP porque uma sequência de até `k` reversões serve como certificado verificável em tempo polinomial.

O problema de otimização é NP-difícil. A dificuldade não existe simplesmente porque se trata de otimização, mas porque é necessário encontrar uma sequência globalmente mínima entre um espaço combinatoriamente grande de sequências de operações restritas.

### 15.4 Resultados a citar

- Caprara, 1997: NP-dificuldade da ordenação por reversões sem sinal;
- Hannenhalli e Pevzner: versão com sinais resolvível em tempo polinomial;
- Kececioglu e Sankoff: algoritmo de 2-aproximação;
- Berman, Hannenhalli e Karpinski, 2002: algoritmo de 1,375-aproximação;
- aplicação em rearranjos de genomas.

As referências bibliográficas originais deverão ser consultadas e citadas formalmente.

---

## 16. Estrutura planejada do repositório

```text
README.md
plano-de-implementação.md
gerador/
    fonte do gerador em C
entradas/
    P_1000/
    M_4000/
    G_16000/
python/
    Quick Sort
    Merge Sort
c/
    Quick Sort
    Merge Sort
medicao/
    execução dos blocos
testes/
    corretude e validação das entradas
analise/
    agregação, tabelas e gráficos
resultados/
    dados brutos
    dados resumidos
relatorio/
    materiais do relatório
```

O README deverá explicar:

- requisitos;
- versões utilizadas;
- como compilar;
- como gerar as entradas;
- como executar os testes;
- como executar a coleta;
- como gerar tabelas e gráficos;
- onde encontrar os resultados;
- semente utilizada;
- flags de compilação;
- estrutura dos arquivos.

---

## 17. Organização do relatório

O PDF seguirá a ordem exigida:

1. descrição do problema e dos algoritmos;
2. classificação assintótica com O, Ω e Θ;
3. melhor caso, pior caso e caso médio;
4. aplicabilidade prática;
5. simulação e metodologia;
6. gráficos e tabelas;
7. reflexão sobre P e NP.

Também incluirá:

- ambiente de execução;
- contribuições de cada integrante;
- referências bibliográficas;
- limitações;
- ameaças à validade;
- declaração de uso de IA.

### 17.1 Declaração de IA

A declaração deverá informar:

- ferramenta utilizada;
- apoio no planejamento;
- apoio na implementação;
- apoio na revisão;
- apoio na análise;
- apoio na elaboração de testes e documentação.

Todos os integrantes deverão entender e saber explicar todo o conteúdo produzido.

---

## 18. Divisão de responsabilidades

| Integrante | Responsabilidade principal |
|---|---|
| 1 | Gerador em C, entradas construídas e validação |
| 2 | Quick e Merge em C, compilação e medição em C |
| 3 | Quick e Merge em Python, medição e testes |
| 4 | Análise, gráficos, teoria, referências e relatório |

Todos deverão:

- revisar as quatro implementações;
- conhecer a metodologia;
- compreender os gráficos;
- ensaiar respostas;
- participar da apresentação.

---

## 19. Apresentação

A apresentação terá no máximo sete minutos e todos os quatro integrantes deverão falar.

Estrutura sugerida:

1. problema e algoritmos;
2. complexidade e famílias de entrada;
3. metodologia experimental;
4. principais resultados;
5. conclusão prática e reflexão P × NP.

Cada integrante terá aproximadamente um minuto e quarenta segundos.

---

## 20. Cronograma atualizado

| Data | Atividade |
|---|---|
| 16/11 | Fechar planejamento, estrutura e metodologia |
| 17/11 | Criar gerador, gerar e validar as 150 entradas |
| 18/11 | Implementar os algoritmos e concluir os testes |
| 19/11 | Fazer piloto, coleta oficial, gráficos e relatório |
| 20/11 | Revisar, reproduzir, ensaiar e enviar antes do prazo |

O bônus de memória não terá prioridade sobre qualquer atividade obrigatória.

---

## 21. Riscos e respostas

### 21.1 Quick quadrático no tamanho G

Risco:

- o Quick em Python pode demorar muito para ordenar blocos de dez vetores crescentes ou inversos com 16.000 elementos.

Resposta:

- executar um piloto assim que as implementações estiverem corretas;
- registrar o tempo real;
- não alterar tamanhos silenciosamente;
- sinalizar imediatamente se a coleta completa for impraticável.

### 21.2 Erro nas entradas construídas

Risco:

- a disposição chamada de melhor ou pior caso não provocar o comportamento esperado.

Resposta:

- usar versões instrumentadas;
- contar comparações;
- verificar tamanhos das partições;
- manter a instrumentação fora do benchmark.

### 21.3 Comparação injusta

Risco:

- linguagens ou algoritmos receberem entradas diferentes.

Resposta:

- reutilizar os mesmos 150 arquivos;
- manter nomes e índices;
- validar conjuntos de valores;
- registrar manifesto e checksums.

### 21.4 Medição contaminada

Risco:

- incluir leitura, cópia, impressão ou validação no cronômetro.

Resposta:

- delimitar claramente a região medida;
- preparar cópias antes;
- validar depois;
- revisar o fluxo de medição.

### 21.5 Otimização remover o trabalho em C

Risco:

- o compilador considerar o resultado não utilizado.

Resposta:

- tornar a saída observável depois do cronômetro;
- usar validação ou checksum;
- conferir o executável otimizado.

### 21.6 Resultados não reproduzíveis

Risco:

- depender do gerador aleatório da biblioteca ou não registrar o ambiente.

Resposta:

- PRNG determinístico;
- semente 42;
- arquivos persistidos;
- versões e comandos documentados;
- README reprodutível.

---

## 22. Ordem de execução do projeto

1. criar a estrutura de diretórios;
2. implementar o gerador em C;
3. gerar os 150 arquivos;
4. validar valores e correspondência entre famílias;
5. implementar as versões instrumentadas;
6. validar melhor Quick e pior Merge;
7. implementar Quick e Merge oficiais em Python;
8. implementar Quick e Merge oficiais em C;
9. criar testes automatizados;
10. comparar as quatro implementações;
11. criar o programa de medição em blocos;
12. fazer o piloto do Quick quadrático em G;
13. executar a coleta oficial;
14. preservar o CSV bruto;
15. gerar resumo estatístico;
16. produzir gráficos e tabelas;
17. interpretar os resultados;
18. escrever e revisar o relatório;
19. concluir README e instruções;
20. ensaiar a apresentação;
21. verificar a reprodução completa;
22. enviar antes do prazo.

---

## 23. Critérios para considerar o projeto concluído

- 150 arquivos de entrada gerados e validados;
- quatro implementações corretas;
- testes automatizados passando;
- mesmos resultados nas quatro implementações;
- 1.200 medições de bloco registradas, salvo impedimento documentado;
- dados brutos preservados;
- médias e desvios padrão calculados;
- comparações teóricas e práticas produzidas;
- comparações entre algoritmos e linguagens produzidas;
- ambiente completamente documentado;
- relatório seguindo os sete itens;
- declaração de IA incluída;
- contribuições dos integrantes incluídas;
- README reproduzível;
- apresentação de até sete minutos preparada.
