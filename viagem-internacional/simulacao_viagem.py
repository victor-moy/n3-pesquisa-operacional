"""
Simulação de Monte Carlo — Custo total de uma viagem internacional
==================================================================
Trabalho de Pesquisa Operacional — Victor

Cenário: viagem de 7 noites para os Estados Unidos (Orlando).
O custo total em reais depende de três variáveis incertas:

  1. Passagem aérea (ida e volta), em dólares  -> distribuição triangular
  2. Diária de hospedagem, em dólares          -> distribuição triangular
  3. Câmbio do dólar (R$/US$)                  -> distribuição normal

Custo total (R$) = (passagem + diária x noites) x câmbio

São rodadas 10.000 simulações para estimar o custo mais provável
e identificar o melhor e o pior cenário de orçamento.
"""

import numpy as np
import matplotlib

matplotlib.use("Agg")  # gera os gráficos sem abrir janela
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Parâmetros da simulação
# ----------------------------------------------------------------------
N_SIMULACOES = 10_000
NOITES = 7
SEED = 42  # semente fixa para o resultado ser reproduzível

# Passagem aérea ida e volta (US$): mínimo, mais provável, máximo
PASSAGEM_MIN, PASSAGEM_MODA, PASSAGEM_MAX = 600, 850, 1_400

# Diária de hospedagem (US$): mínimo, mais provável, máximo
DIARIA_MIN, DIARIA_MODA, DIARIA_MAX = 80, 120, 220

# Câmbio do dólar (R$/US$): média e desvio padrão
CAMBIO_MEDIA, CAMBIO_DESVIO = 5.40, 0.25

rng = np.random.default_rng(SEED)

# ----------------------------------------------------------------------
# Sorteio das variáveis aleatórias (uma linha = 10.000 sorteios de vez)
# ----------------------------------------------------------------------
passagem = rng.triangular(PASSAGEM_MIN, PASSAGEM_MODA, PASSAGEM_MAX, N_SIMULACOES)
diaria = rng.triangular(DIARIA_MIN, DIARIA_MODA, DIARIA_MAX, N_SIMULACOES)
cambio = rng.normal(CAMBIO_MEDIA, CAMBIO_DESVIO, N_SIMULACOES)
cambio = np.clip(cambio, 4.50, 6.50)  # evita valores irreais nas caudas

custo_usd = passagem + diaria * NOITES
custo_brl = custo_usd * cambio

# ----------------------------------------------------------------------
# Estatísticas
# ----------------------------------------------------------------------
media = custo_brl.mean()
mediana = np.median(custo_brl)
desvio = custo_brl.std()
p5, p95 = np.percentile(custo_brl, [5, 95])
melhor = custo_brl.min()
pior = custo_brl.max()

# probabilidade de estourar alguns orçamentos de referência
orcamentos = [8_000, 9_000, 10_000, 11_000, 12_000]

fmt = lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

linhas = [
    "SIMULAÇÃO DE MONTE CARLO — VIAGEM INTERNACIONAL (7 noites, EUA)",
    f"Número de simulações: {N_SIMULACOES:,}".replace(",", "."),
    "",
    f"Custo médio:            {fmt(media)}",
    f"Custo mais provável*:   {fmt(mediana)}   (*mediana)",
    f"Desvio padrão:          {fmt(desvio)}",
    "",
    f"Melhor cenário (mín):   {fmt(melhor)}",
    f"Pior cenário (máx):     {fmt(pior)}",
    f"Intervalo de 90%:       {fmt(p5)}  a  {fmt(p95)}",
    "",
    "Probabilidade de o custo ULTRAPASSAR o orçamento:",
]
for orc in orcamentos:
    prob = (custo_brl > orc).mean() * 100
    linhas.append(f"  Orçamento de {fmt(orc)}: {prob:5.1f}%")

relatorio = "\n".join(linhas)
print(relatorio)
with open("resultados.txt", "w", encoding="utf-8") as f:
    f.write(relatorio + "\n")

# ----------------------------------------------------------------------
# Gráfico 1 — Histograma do custo total
# ----------------------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.hist(custo_brl, bins=60, color="#4C9BE8", edgecolor="white")
plt.axvline(media, color="#D62728", lw=2, label=f"Média: {fmt(media)}")
plt.axvline(p5, color="#2CA02C", lw=2, ls="--", label=f"P5 (melhor 5%): {fmt(p5)}")
plt.axvline(p95, color="#FF7F0E", lw=2, ls="--", label=f"P95 (pior 5%): {fmt(p95)}")
plt.title(f"Custo total da viagem — {N_SIMULACOES:,} simulações de Monte Carlo".replace(",", "."))
plt.xlabel("Custo total (R$)")
plt.ylabel("Frequência")
plt.legend()
plt.tight_layout()
plt.savefig("grafico_histograma.png", dpi=150)
plt.close()

# ----------------------------------------------------------------------
# Gráfico 2 — Probabilidade acumulada (curva S)
# ----------------------------------------------------------------------
ordenado = np.sort(custo_brl)
acumulada = np.arange(1, N_SIMULACOES + 1) / N_SIMULACOES * 100

plt.figure(figsize=(10, 6))
plt.plot(ordenado, acumulada, color="#4C9BE8", lw=2)
plt.axhline(90, color="#FF7F0E", ls="--", lw=1.5)
plt.axvline(np.percentile(custo_brl, 90), color="#FF7F0E", ls="--", lw=1.5,
            label=f"90% das simulações até {fmt(np.percentile(custo_brl, 90))}")
plt.title("Probabilidade acumulada do custo total")
plt.xlabel("Custo total (R$)")
plt.ylabel("Probabilidade de o custo ficar abaixo do valor (%)")
plt.legend(loc="lower right")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("grafico_acumulado.png", dpi=150)
plt.close()

# ----------------------------------------------------------------------
# Gráfico 3 — Distribuição das variáveis de entrada
# ----------------------------------------------------------------------
fig, eixos = plt.subplots(1, 3, figsize=(15, 4.5))
entradas = [
    (passagem, "Passagem aérea (US$)", "Triangular (600 / 850 / 1.400)"),
    (diaria, "Diária de hospedagem (US$)", "Triangular (80 / 120 / 220)"),
    (cambio, "Câmbio (R\\$/US\\$)", "Normal (média 5,40 | desvio 0,25)"),
]
for eixo, (dados, titulo, dist) in zip(eixos, entradas):
    eixo.hist(dados, bins=50, color="#4C9BE8", edgecolor="white")
    eixo.set_title(f"{titulo}\n{dist}", fontsize=10)
    eixo.set_ylabel("Frequência")
fig.suptitle("Variáveis de entrada da simulação", fontsize=13)
plt.tight_layout()
plt.savefig("grafico_entradas.png", dpi=150)
plt.close()

print("\nGráficos salvos: grafico_histograma.png, grafico_acumulado.png, grafico_entradas.png")
