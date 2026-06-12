# Simulação de Monte Carlo — Viagem Internacional

Trabalho de Pesquisa Operacional — **Victor: Viagem internacional**

## O problema

Quanto custa uma viagem internacional? Não dá pra responder com um número exato,
porque o custo depende de variáveis que mudam o tempo todo: o preço da passagem,
o valor da diária do hotel e o câmbio do dólar. A simulação de Monte Carlo resolve
isso sorteando milhares de combinações possíveis dessas variáveis e observando a
distribuição dos resultados.

**Cenário simulado:** viagem de 7 noites para os Estados Unidos (Orlando).

## O modelo

```
Custo total (R$) = (passagem + diária × 7 noites) × câmbio
```

| Variável | Distribuição | Parâmetros | Por quê |
|---|---|---|---|
| Passagem aérea (US$) | Triangular | mín 600, moda 850, máx 1.400 | Sabemos o preço típico e os extremos de promoção/alta temporada |
| Diária de hospedagem (US$) | Triangular | mín 80, moda 120, máx 220 | Mesmo raciocínio: faixa conhecida com valor mais comum |
| Câmbio (R$/US$) | Normal | média 5,40, desvio 0,25 | O câmbio oscila simetricamente em torno do valor atual |

A distribuição **triangular** é usada quando conhecemos o mínimo, o máximo e o
valor mais provável — exatamente o caso de preços de passagem e hotel. A
**normal** modela bem o câmbio, que flutua em torno de um valor central.

## Como rodar

```bash
python3 simulacao_viagem.py
```

Requisitos: Python 3 com `numpy` e `matplotlib`.

O script roda **10.000 simulações** (configurável em `N_SIMULACOES`), imprime as
estatísticas, salva `resultados.txt` e gera três gráficos PNG.

## Resultados (semente fixa = 42)

| Estatística | Valor |
|---|---|
| Custo médio | R$ 10.436,44 |
| Custo mais provável (mediana) | R$ 10.349,40 |
| Melhor cenário | R$ 6.282,05 |
| Pior cenário | R$ 16.702,36 |
| Intervalo de 90% de confiança | R$ 8.104,04 a R$ 13.082,30 |

Probabilidade de estourar o orçamento:

- Com **R$ 10.000** de orçamento, há **58,8%** de chance de faltar dinheiro.
- Com **R$ 12.000**, o risco cai para **15,7%**.
- Para viajar com 95% de segurança, o orçamento deve ser de cerca de **R$ 13.100** (P95).

## Gráficos gerados

1. **`grafico_histograma.png`** — distribuição do custo total, com a média e os
   percentis 5% e 95% marcados. É o gráfico principal da apresentação.
2. **`grafico_acumulado.png`** — curva de probabilidade acumulada ("curva S"):
   permite ler diretamente "qual a chance de a viagem custar até X reais".
3. **`grafico_entradas.png`** — histogramas das três variáveis sorteadas, mostrando
   que as distribuições escolhidas foram respeitadas.

## Conclusão (pra ligar com a parte da Pessoa 3)

A simulação transforma três incertezas (passagem, hotel, câmbio) em uma resposta
prática: em vez de um único "chute" de custo, temos uma **faixa de valores com
probabilidades**. O viajante que orçar pela média (R$ ~10.400) tem quase 50% de
chance de estourar; quem quiser segurança deve orçar pelo P95 (R$ ~13.100).
Esse é o mesmo raciocínio usado na simulação de aposentadoria da Pessoa 2: lá as
incertezas são rendimento e inflação, e a pergunta é quanto poupar por mês.
