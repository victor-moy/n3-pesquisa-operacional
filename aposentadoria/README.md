```
==================================================================
Simulação de Monte Carlo — Aposentadoria e Patrimônio
==================================================================
Trabalho de Pesquisa Operacional — Jhessica: Aposentadoria

1. O PROBLEMA
------------------------------------------------------------------
Quanto dinheiro eu terei daqui a 30 anos? É impossível cravar um 
número exato, pois o futuro depende de variáveis que oscilam: o 
rendimento dos investimentos, a inflação (que corrói o poder de 
compra) e a nossa própria disciplina de poupança (aportes). 

A simulação de Monte Carlo resolve isso rodando 100.000 cenários 
possíveis, nos dando uma visão probabilística do sucesso ou 
fracasso do plano.

Cenário simulado: plano de 30 anos (360 meses) de contribuição 
para atingir a meta de R$ 1.000.000 ou uma renda de R$ 5.000/mês.


2. O MODELO MATEMÁTICO
------------------------------------------------------------------
Patrimônio Final = Somatório corrigido dos aportes + juros compostos

Variáveis Incertas e Distribuições:

* Rendimento (a.m.): Triangular (mín 0.5%, moda 0.9%, máx 1.8%)
  -> Motivo: Simula o CDI/Tesouro com cenários realista vs. otimista.

* Inflação (a.a.): Uniforme (mín 3.0%, máx 9.0%)
  -> Motivo: Modelagem de incerteza ampla do custo de vida futuro.

* Aporte Mensal: Uniforme (±20% sobre o aporte base de R$ 1.000)
  -> Motivo: Simula a volatilidade da capacidade de poupança humana.

A distribuição triangular é ideal para o rendimento, onde temos um 
valor central (moda) e limites conhecidos. A uniforme foi escolhida 
para a inflação e aporte para representar uma incerteza mais ampla 
e sem um "valor central" de preferência.


3. COMO RODAR
------------------------------------------------------------------
Comando: python3 simulacao_aposentadoria.py

Requisitos: Python 3 com as bibliotecas 'numpy' e 'matplotlib'.

O script roda 100.000 simulações, imprime as estatísticas no 
terminal e exporta os componentes do dashboard de análise visual.


4. RESULTADOS (Semente fixa = 42)
------------------------------------------------------------------
A análise estatística dos dados gerados após 100.000 corridas
revelou os seguintes valores de fronteira e centralidade:

* Mediana (P50 - Saldo Nominal Final): R$ 3.800.000,00
* Mediana Real (P50 - Poder de Compra): R$ 708.000,00
* Cenário de Estresse (P10 - Valor Real): R$ 200.000,00
* Cenário Otimista (P90 - Valor Real): R$ 2.500.000,00

Probabilidade de Sucesso:
* Chance de atingir a meta de R$ 1M Nominal: 100.0%
* Chance de gerar renda nominal de R$ 5.000/mês: 94.3%
* Mediana da renda mensal nominal estimada: R$ 12.681,00


5. DASHBOARD VISUAL GERADO
------------------------------------------------------------------
O conjunto de gráficos gerados unifica as seguintes perspectivas:

1. Distribuição do Patrimônio Final (Nominal): Histograma com a
   frequência dos saldos acumulados. Mostra uma assimetria à direita,
   com a linha de meta de R$ 1M superada em todas as rodadas.
2. Nominal vs. Valor Real: O maior indicador de risco do modelo.
   Embora a mediana nominal chegue a R$ 3.8M, o poder de compra real
   corrigido pela inflação cai para R$ 708k (abaixo da meta ideal).
3. Renda Mensal na Aposentadoria: Histograma mostrando que em 94.3%
   dos casos a meta de renda de R$ 5.000/mês é superada, com ponto
   central (mediana) estabelecido em R$ 12.681,00 líquidos.
4. Pizza de Probabilidade: Validação visual confirmando que 100% 
   das simulações ultrapassaram o piso de R$ 1 milhão nominal.
5. Trajetória Temporal (Três Cenários): Demonstra a curva exponencial
   dos juros compostos agindo ao longo dos 30 anos para os cenários
   P10 (R$ 1.7M), P50 (R$ 3.8M) e P90 (R$ 12.4M).
6. Gráfico de Sensibilidade: Dispersão que evidencia o impacto crítico
   do rendimento mensal. Taxas acima de 1.4% ao mês geram um efeito
   exponencial avassalador no longo prazo.


6. CONCLUSÃO
------------------------------------------------------------------
A simulação prova que a aposentadoria não é um destino linear, mas 
sim uma faixa de possibilidades. O maior risco mapeado não é apenas 
o rendimento do mercado isolado, mas sim a inflação de longo prazo 
combinada com a inconsistência dos aportes mensais. 

O maior achado deste modelo de Pesquisa Operacional é o "efeito 
ilusão" da inflação: embora o investidor tenha 100% de certeza de
ficar milionário em termos nominais (em conta), em termos reais de
poder de compra de hoje, a mediana (P50 Real) fica em R$ 708k. 

Portanto, para o planejamento de longo prazo da Pessoa 3, o modelo
indica que o investidor precisa aumentar o aporte progressivamente
para cobrir a inflação ou buscar ativos que garantam ganho real
acima do custo de vida.
==================================================================

```