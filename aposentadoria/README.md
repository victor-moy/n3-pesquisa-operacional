# Simulação de Monte Carlo — Aposentadoria

Trabalho de Pesquisa Operacional — Jhessica

## Objetivo

Simular o crescimento de um investimento mensal de **R$ 1.000** ao longo de **30 anos** para avaliar a viabilidade financeira da aposentadoria. A simulação considera a volatilidade de mercado através de variações aleatórias na **taxa de rendimento**, na **inflação** e no **comportamento de aporte**, rodando **100.000 simulações** via Método de Monte Carlo. 

O intuito é determinar a probabilidade do investidor atingir um patrimônio nominal de **R$ 1.000.000** e garantir uma renda equivalente a pelo menos **R$ 5.000 mensais** aos 60 anos (utilizando a regra de retirada de 4% a.a.).

## Estrutura do Projeto

- `simulacao_aposentadoria.py` — Código em Python com a lógica e geração de variáveis aleatórias.
- `simulacao_monte_carlo_aposentadoria.png` — Dashboard de gráficos gerado (distribuição, cenários P10/P50/P90 e sensibilidade).
- Este `README.md` — Descrição do modelo acadêmico, premissas estatísticas e análise dos resultados.