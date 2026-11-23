# Resultados numéricos

## Quick Sort dividido por Merge Sort

| Linguagem | Família | n | Quick (s) | Merge (s) | Quick/Merge |
|---|---|---:|---:|---:|---:|
| Python | Aleatória | 1000 | 0.000822521 | 0.001310446 | 0.628× |
| Python | Aleatória | 4000 | 0.004346375 | 0.007178524 | 0.605× |
| Python | Aleatória | 16000 | 0.018457546 | 0.030603928 | 0.603× |
| Python | Crescente | 1000 | 0.029825353 | 0.001349659 | 22.098× |
| Python | Crescente | 4000 | 0.535315325 | 0.005744381 | 93.189× |
| Python | Crescente | 16000 | 7.768892774 | 0.028316855 | 274.356× |
| Python | Inversa | 1000 | 0.022711854 | 0.001189121 | 19.100× |
| Python | Inversa | 4000 | 0.366877351 | 0.006014580 | 60.998× |
| Python | Inversa | 16000 | 5.899041874 | 0.026882090 | 219.441× |
| Python | Melhor Quick | 1000 | 0.000550111 | 0.001322848 | 0.416× |
| Python | Melhor Quick | 4000 | 0.002704947 | 0.006197321 | 0.436× |
| Python | Melhor Quick | 16000 | 0.012199926 | 0.029697940 | 0.411× |
| Python | Pior Merge | 1000 | 0.000791617 | 0.001417865 | 0.558× |
| Python | Pior Merge | 4000 | 0.003972578 | 0.006731674 | 0.590× |
| Python | Pior Merge | 16000 | 0.018195188 | 0.030537572 | 0.596× |
| C | Aleatória | 1000 | 0.000053461 | 0.000061416 | 0.870× |
| C | Aleatória | 4000 | 0.000280690 | 0.000356577 | 0.787× |
| C | Aleatória | 16000 | 0.001191032 | 0.001488172 | 0.800× |
| C | Crescente | 1000 | 0.000375422 | 0.000017595 | 21.337× |
| C | Crescente | 4000 | 0.005973386 | 0.000098365 | 60.727× |
| C | Crescente | 16000 | 0.106130275 | 0.000347739 | 305.201× |
| C | Inversa | 1000 | 0.000406128 | 0.000017545 | 23.148× |
| C | Inversa | 4000 | 0.006090120 | 0.000118213 | 51.518× |
| C | Inversa | 16000 | 0.101971177 | 0.000362045 | 281.653× |
| C | Melhor Quick | 1000 | 0.000015335 | 0.000056228 | 0.273× |
| C | Melhor Quick | 4000 | 0.000035147 | 0.000080190 | 0.438× |
| C | Melhor Quick | 16000 | 0.000183675 | 0.000469184 | 0.391× |
| C | Pior Merge | 1000 | 0.000013315 | 0.000018287 | 0.728× |
| C | Pior Merge | 4000 | 0.000193842 | 0.000085716 | 2.261× |
| C | Pior Merge | 16000 | 0.001081056 | 0.000397480 | 2.720× |

## Aceleração de C em relação a Python

| Algoritmo | Família | n | Python/C |
|---|---|---:|---:|
| Quick | Aleatória | 1000 | 15.385× |
| Quick | Aleatória | 4000 | 15.485× |
| Quick | Aleatória | 16000 | 15.497× |
| Quick | Crescente | 1000 | 79.445× |
| Quick | Crescente | 4000 | 89.617× |
| Quick | Crescente | 16000 | 73.201× |
| Quick | Inversa | 1000 | 55.923× |
| Quick | Inversa | 4000 | 60.241× |
| Quick | Inversa | 16000 | 57.850× |
| Quick | Melhor Quick | 1000 | 35.873× |
| Quick | Melhor Quick | 4000 | 76.961× |
| Quick | Melhor Quick | 16000 | 66.421× |
| Quick | Pior Merge | 1000 | 59.453× |
| Quick | Pior Merge | 4000 | 20.494× |
| Quick | Pior Merge | 16000 | 16.831× |
| Merge | Aleatória | 1000 | 21.337× |
| Merge | Aleatória | 4000 | 20.132× |
| Merge | Aleatória | 16000 | 20.565× |
| Merge | Crescente | 1000 | 76.707× |
| Merge | Crescente | 4000 | 58.399× |
| Merge | Crescente | 16000 | 81.431× |
| Merge | Inversa | 1000 | 67.775× |
| Merge | Inversa | 4000 | 50.879× |
| Merge | Inversa | 16000 | 74.251× |
| Merge | Melhor Quick | 1000 | 23.526× |
| Merge | Melhor Quick | 4000 | 77.283× |
| Merge | Melhor Quick | 16000 | 63.297× |
| Merge | Pior Merge | 1000 | 77.534× |
| Merge | Pior Merge | 4000 | 78.535× |
| Merge | Pior Merge | 16000 | 76.828× |

## Valores normalizados usados nos gráficos

| Linguagem | Algoritmo | Família | n | Média (s) | Desvio (s) | f(n) | T(n)/f(n) | CPU/real |
|---|---|---|---:|---:|---:|---|---:|---:|
| C | Merge | Aleatória | 1000 | 0.000061416 | 0.000003692 | n*log2(n) | 6.162686e-09 | 0.9963 |
| C | Merge | Aleatória | 4000 | 0.000356577 | 0.000141062 | n*log2(n) | 7.449930e-09 | 0.9993 |
| C | Merge | Aleatória | 16000 | 0.001488172 | 0.000111569 | n*log2(n) | 6.659902e-09 | 0.9997 |
| C | Merge | Crescente | 1000 | 0.000017595 | 0.000003207 | n*log2(n) | 1.765541e-09 | 0.9959 |
| C | Merge | Crescente | 4000 | 0.000098365 | 0.000040698 | n*log2(n) | 2.055131e-09 | 0.9942 |
| C | Merge | Crescente | 16000 | 0.000347739 | 0.000030064 | n*log2(n) | 1.556210e-09 | 0.9992 |
| C | Merge | Inversa | 1000 | 0.000017545 | 0.000004467 | n*log2(n) | 1.760524e-09 | 0.9961 |
| C | Merge | Inversa | 4000 | 0.000118213 | 0.000098349 | n*log2(n) | 2.469813e-09 | 0.9935 |
| C | Merge | Inversa | 16000 | 0.000362045 | 0.000084533 | n*log2(n) | 1.620232e-09 | 0.9990 |
| C | Merge | Melhor Quick | 1000 | 0.000056228 | 0.000171998 | n*log2(n) | 5.642105e-09 | 0.9988 |
| C | Merge | Melhor Quick | 4000 | 0.000080190 | 0.000006473 | n*log2(n) | 1.675402e-09 | 0.9983 |
| C | Merge | Melhor Quick | 16000 | 0.000469184 | 0.000234400 | n*log2(n) | 2.099703e-09 | 0.9994 |
| C | Merge | Pior Merge | 1000 | 0.000018287 | 0.000002900 | n*log2(n) | 1.834979e-09 | 0.9969 |
| C | Merge | Pior Merge | 4000 | 0.000085716 | 0.000009189 | n*log2(n) | 1.790856e-09 | 0.9968 |
| C | Merge | Pior Merge | 16000 | 0.000397480 | 0.000028651 | n*log2(n) | 1.778812e-09 | 0.9991 |
| C | Quick | Aleatória | 1000 | 0.000053461 | 0.000014914 | n*log2(n) | 5.364455e-09 | 0.9951 |
| C | Quick | Aleatória | 4000 | 0.000280690 | 0.000119353 | n*log2(n) | 5.864430e-09 | 0.9993 |
| C | Quick | Aleatória | 16000 | 0.001191032 | 0.000133321 | n*log2(n) | 5.330134e-09 | 0.9995 |
| C | Quick | Crescente | 1000 | 0.000375422 | 0.000037136 | n^2 | 3.754220e-10 | 0.9991 |
| C | Quick | Crescente | 4000 | 0.005973386 | 0.000466405 | n^2 | 3.733366e-10 | 0.9998 |
| C | Quick | Crescente | 16000 | 0.106130275 | 0.017831701 | n^2 | 4.145714e-10 | 0.9992 |
| C | Quick | Inversa | 1000 | 0.000406128 | 0.000117509 | n^2 | 4.061280e-10 | 0.9996 |
| C | Quick | Inversa | 4000 | 0.006090120 | 0.000283867 | n^2 | 3.806325e-10 | 0.9999 |
| C | Quick | Inversa | 16000 | 0.101971177 | 0.006252180 | n^2 | 3.983249e-10 | 0.9996 |
| C | Quick | Melhor Quick | 1000 | 0.000015335 | 0.000014185 | n*log2(n) | 1.538765e-09 | 0.9950 |
| C | Quick | Melhor Quick | 4000 | 0.000035147 | 0.000002816 | n*log2(n) | 7.343229e-10 | 0.9976 |
| C | Quick | Melhor Quick | 16000 | 0.000183675 | 0.000050603 | n*log2(n) | 8.219866e-10 | 0.9986 |
| C | Quick | Pior Merge | 1000 | 0.000013315 | 0.000004331 | n*log2(n) | 1.336071e-09 | 0.9958 |
| C | Quick | Pior Merge | 4000 | 0.000193842 | 0.000020362 | n*log2(n) | 4.049923e-09 | 0.9950 |
| C | Quick | Pior Merge | 16000 | 0.001081056 | 0.000208714 | n*log2(n) | 4.837967e-09 | 0.9995 |
| Python | Merge | Aleatória | 1000 | 0.001310446 | 0.000053531 | n*log2(n) | 1.314945e-07 | 0.9995 |
| Python | Merge | Aleatória | 4000 | 0.007178524 | 0.000629503 | n*log2(n) | 1.499802e-07 | 0.9994 |
| Python | Merge | Aleatória | 16000 | 0.030603928 | 0.001168711 | n*log2(n) | 1.369594e-07 | 0.9997 |
| Python | Merge | Crescente | 1000 | 0.001349659 | 0.000245115 | n*log2(n) | 1.354293e-07 | 0.9994 |
| Python | Merge | Crescente | 4000 | 0.005744381 | 0.000268160 | n*log2(n) | 1.200168e-07 | 0.9995 |
| Python | Merge | Crescente | 16000 | 0.028316855 | 0.005046604 | n*log2(n) | 1.267242e-07 | 0.9989 |
| Python | Merge | Inversa | 1000 | 0.001189121 | 0.000139340 | n*log2(n) | 1.193204e-07 | 0.9994 |
| Python | Merge | Inversa | 4000 | 0.006014580 | 0.000554168 | n*log2(n) | 1.256621e-07 | 0.9995 |
| Python | Merge | Inversa | 16000 | 0.026882090 | 0.001804984 | n*log2(n) | 1.203033e-07 | 0.9997 |
| Python | Merge | Melhor Quick | 1000 | 0.001322848 | 0.000170003 | n*log2(n) | 1.327390e-07 | 0.9995 |
| Python | Merge | Melhor Quick | 4000 | 0.006197321 | 0.000283103 | n*log2(n) | 1.294800e-07 | 0.9996 |
| Python | Merge | Melhor Quick | 16000 | 0.029697940 | 0.001258791 | n*log2(n) | 1.329049e-07 | 0.9995 |
| Python | Merge | Pior Merge | 1000 | 0.001417865 | 0.000234549 | n*log2(n) | 1.422733e-07 | 0.9986 |
| Python | Merge | Pior Merge | 4000 | 0.006731674 | 0.001291372 | n*log2(n) | 1.406442e-07 | 0.9996 |
| Python | Merge | Pior Merge | 16000 | 0.030537572 | 0.001381427 | n*log2(n) | 1.366624e-07 | 0.9995 |
| Python | Quick | Aleatória | 1000 | 0.000822521 | 0.000202784 | n*log2(n) | 8.253450e-08 | 0.9989 |
| Python | Quick | Aleatória | 4000 | 0.004346375 | 0.001650046 | n*log2(n) | 9.080840e-08 | 0.9997 |
| Python | Quick | Aleatória | 16000 | 0.018457546 | 0.000846853 | n*log2(n) | 8.260164e-08 | 0.9997 |
| Python | Quick | Crescente | 1000 | 0.029825353 | 0.001297669 | n^2 | 2.982535e-08 | 0.9998 |
| Python | Quick | Crescente | 4000 | 0.535315325 | 0.031434043 | n^2 | 3.345721e-08 | 0.9992 |
| Python | Quick | Crescente | 16000 | 7.768892774 | 0.071268550 | n^2 | 3.034724e-08 | 0.9997 |
| Python | Quick | Inversa | 1000 | 0.022711854 | 0.000813914 | n^2 | 2.271185e-08 | 0.9996 |
| Python | Quick | Inversa | 4000 | 0.366877351 | 0.019114047 | n^2 | 2.292983e-08 | 0.9995 |
| Python | Quick | Inversa | 16000 | 5.899041874 | 0.081542820 | n^2 | 2.304313e-08 | 0.9996 |
| Python | Quick | Melhor Quick | 1000 | 0.000550111 | 0.000153924 | n*log2(n) | 5.519997e-08 | 0.9985 |
| Python | Quick | Melhor Quick | 4000 | 0.002704947 | 0.000359433 | n*log2(n) | 5.651420e-08 | 0.9997 |
| Python | Quick | Melhor Quick | 16000 | 0.012199926 | 0.000473270 | n*log2(n) | 5.459739e-08 | 0.9997 |
| Python | Quick | Pior Merge | 1000 | 0.000791617 | 0.000095500 | n*log2(n) | 7.943349e-08 | 0.9993 |
| Python | Quick | Pior Merge | 4000 | 0.003972578 | 0.000259551 | n*log2(n) | 8.299870e-08 | 0.9994 |
| Python | Quick | Pior Merge | 16000 | 0.018195188 | 0.001332938 | n*log2(n) | 8.142753e-08 | 0.9997 |
