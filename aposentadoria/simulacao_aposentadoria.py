"""
Simulação de Monte Carlo — Aposentadoria

Trabalho de Pesquisa Operacional — Jhessica

Cenário: plano de acumulação financeira de 30 anos (360 meses) para aposentadoria.
O patrimônio final e a renda gerada dependem de três variáveis incertas:

    Rendimento mensal dos investimentos -> distribuição triangular
    Inflação anual (poder de compra)    -> distribuição uniforme
    Variação do aporte mensal humano   -> distribuição uniforme (±20%)

Patrimônio Final (R$) = Somatório corrigido dos aportes mensais + juros compostos

São rodadas 100.000 simulações para estimar o patrimônio mais provável,
a probabilidade de atingir a meta de R$ 1 milhão e a renda mensal real estimada.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FuncFormatter
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────
#  PARÂMETROS BASE
# ─────────────────────────────────────────
np.random.seed(42)

N_SIMULACOES      = 100_000   
ANOS_CONTRIBUICAO = 30      
MESES             = ANOS_CONTRIBUICAO * 12
APORTE_MENSAL     = 1_000   
META_PATRIMONIO   = 1_000_000 
RENDA_DESEJADA_MES = 5_000    # R$ renda mensal desejada na aposentadoria

# Distribuições das variáveis aleatórias
# Rendimento mensal bruto — triangular (mín, moda, máx)
REND_MIN  = 0.005   # 0.5% ao mês
REND_MODA = 0.009   # 0.9% ao mês (CDI/Tesouro realista)
REND_MAX  = 0.018   # 1.8% ao mês (cenário otimista)

# Inflação anual — uniforme
INF_MIN = 0.03   # 3% a.a.
INF_MAX = 0.09   # 9% a.a.

# ─────────────────────────────────────────
#  GERAÇÃO DAS VARIÁVEIS ALEATÓRIAS
# ─────────────────────────────────────────
# 100k rendimentos mensais (triangular)
rendimentos = np.random.triangular(REND_MIN, REND_MODA, REND_MAX, N_SIMULACOES)

# 100k inflações anuais (uniforme) → convertida para mensal
inflacoes_anuais = np.random.uniform(INF_MIN, INF_MAX, N_SIMULACOES)
inflacoes_mensais = (1 + inflacoes_anuais) ** (1/12) - 1

# Variação do aporte ao longo do tempo (±20% de aleatoriedade humana)
# Simula meses com aportes menores ou maiores
variacao_aporte = np.random.uniform(0.80, 1.20, (N_SIMULACOES, MESES))

# ─────────────────────────────────────────
#  SIMULAÇÃO PRINCIPAL
# ─────────────────────────────────────────
patrimonios_finais  = np.zeros(N_SIMULACOES)
patrimonios_reais   = np.zeros(N_SIMULACOES)  # corrigido pela inflação
rendas_mensais      = np.zeros(N_SIMULACOES)

for i in range(N_SIMULACOES):
    r   = rendimentos[i]       # rendimento mensal desta simulação
    inf = inflacoes_mensais[i] # inflação mensal desta simulação
    
    patrimonio = 0.0
    for m in range(MESES):
        aporte = APORTE_MENSAL * variacao_aporte[i, m]
        patrimonio = patrimonio * (1 + r) + aporte
    
    # Patrimônio nominal
    patrimonios_finais[i] = patrimonio
    
    # Patrimônio em valor real (poder de compra de hoje)
    fator_inflacao = (1 + inf) ** MESES
    patrimonios_reais[i] = patrimonio / fator_inflacao
    
    # Renda mensal possível (regra dos 4% ao ano = 0.33% ao mês)
    rendas_mensais[i] = patrimonio * 0.0033

# ─────────────────────────────────────────
#  MÉTRICAS
# ─────────────────────────────────────────
atingiram_meta   = np.sum(patrimonios_finais >= META_PATRIMONIO)
prob_meta        = atingiram_meta / N_SIMULACOES * 100

atingiram_renda  = np.sum(rendas_mensais >= RENDA_DESEJADA_MES)
prob_renda       = atingiram_renda / N_SIMULACOES * 100

p10  = np.percentile(patrimonios_finais, 10)
p25  = np.percentile(patrimonios_finais, 25)
p50  = np.percentile(patrimonios_finais, 50)
p75  = np.percentile(patrimonios_finais, 75)
p90  = np.percentile(patrimonios_finais, 90)
media = np.mean(patrimonios_finais)

p10r = np.percentile(patrimonios_reais, 10)
p50r = np.percentile(patrimonios_reais, 50)
p90r = np.percentile(patrimonios_reais, 90)

print("=" * 55)
print("  SIMULAÇÃO DE MONTE CARLO — APOSENTADORIA")
print(f"  {N_SIMULACOES:,} simulações | {ANOS_CONTRIBUICAO} anos | R$ {APORTE_MENSAL:,}/mês")
print("=" * 55)
print(f"\n  PATRIMÔNIO NOMINAL ao final de {ANOS_CONTRIBUICAO} anos:")
print(f"    Pior caso  (P10):  R$ {p10:>14,.2f}")
print(f"    Quartil    (P25):  R$ {p25:>14,.2f}")
print(f"    Mediana    (P50):  R$ {p50:>14,.2f}")
print(f"    Média:             R$ {media:>14,.2f}")
print(f"    Quartil    (P75):  R$ {p75:>14,.2f}")
print(f"    Melhor caso(P90):  R$ {p90:>14,.2f}")
print(f"\n  PATRIMÔNIO REAL (poder de compra atual):")
print(f"    Pior caso  (P10):  R$ {p10r:>14,.2f}")
print(f"    Mediana    (P50):  R$ {p50r:>14,.2f}")
print(f"    Melhor caso(P90):  R$ {p90r:>14,.2f}")
print(f"\n  META DE R$ {META_PATRIMONIO:,.0f}:")
print(f"    Probabilidade de atingir: {prob_meta:.1f}%")
print(f"\n  RENDA MENSAL de R$ {RENDA_DESEJADA_MES:,.0f}:")
print(f"    Probabilidade de atingir: {prob_renda:.1f}%")
print("=" * 55)

# ─────────────────────────────────────────
#  GRÁFICOS
# ─────────────────────────────────────────
DARK_BG    = "#0f1117"
CARD_BG    = "#1a1d27"
ACCENT     = "#6C63FF"    # violeta
GREEN      = "#3DDC84"    # verde sucesso
ORANGE     = "#FF9F43"    # laranja alerta
RED        = "#FF6B6B"    # vermelho risco
TEXT       = "#E8E8F0"
MUTED      = "#8888AA"
GRID       = "#2a2d3e"

fmt_reais = FuncFormatter(lambda x, _: f"R$ {x/1e6:.1f}M" if x >= 1e6 else f"R$ {x/1e3:.0f}k")

plt.rcParams.update({
    "figure.facecolor": DARK_BG,
    "axes.facecolor":   CARD_BG,
    "axes.edgecolor":   GRID,
    "axes.labelcolor":  TEXT,
    "xtick.color":      MUTED,
    "ytick.color":      MUTED,
    "text.color":       TEXT,
    "grid.color":       GRID,
    "grid.linewidth":   0.5,
    "font.family":      "DejaVu Sans",
})

fig = plt.figure(figsize=(18, 13), facecolor=DARK_BG)
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.50, wspace=0.35,
                        left=0.06, right=0.97, top=0.90, bottom=0.07)

# ── Título ──────────────────────────────
fig.text(0.5, 0.955, "Simulação de Monte Carlo — Aposentadoria",
         ha="center", fontsize=20, fontweight="bold", color=TEXT)
fig.text(0.5, 0.930,
         f"{N_SIMULACOES:,} simulações  ·  {ANOS_CONTRIBUICAO} anos de aporte  ·  R$ {APORTE_MENSAL:,}/mês",
         ha="center", fontsize=12, color=MUTED)

# ── 1. Histograma patrimônio nominal ────
ax1 = fig.add_subplot(gs[0, :2])
vals_clip = np.clip(patrimonios_finais, 0, np.percentile(patrimonios_finais, 99))
n, bins, patches = ax1.hist(vals_clip, bins=120, color=ACCENT, alpha=0.85, edgecolor="none")

# Colorir barras por zona
for patch, left in zip(patches, bins[:-1]):
    if left < META_PATRIMONIO:
        patch.set_facecolor(RED)
        patch.set_alpha(0.7)
    else:
        patch.set_facecolor(GREEN)
        patch.set_alpha(0.85)

ax1.axvline(META_PATRIMONIO, color=ORANGE, lw=2, ls="--", label=f"Meta R$ {META_PATRIMONIO/1e6:.0f}M")
ax1.axvline(p50, color=TEXT, lw=1.5, ls=":", label=f"Mediana {fmt_reais(p50, None)}")
ax1.xaxis.set_major_formatter(fmt_reais)
ax1.set_title("Distribuição do Patrimônio Final (Nominal)", color=TEXT, fontsize=12, pad=8)
ax1.set_xlabel("Patrimônio acumulado")
ax1.set_ylabel("Frequência")
ax1.legend(fontsize=9, framealpha=0.2)
ax1.grid(axis="y", alpha=0.4)

# ── 2. KPI cards ────────────────────────
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis("off")
kpis = [
    ("Prob. de atingir\nR$ 1 milhão", f"{prob_meta:.1f}%", GREEN if prob_meta > 50 else ORANGE),
    ("Renda mensal\nR$ 5.000+", f"{prob_renda:.1f}%", GREEN if prob_renda > 50 else ORANGE),
    ("Mediana\npatrimônio", fmt_reais(p50, None), ACCENT),
]
for idx, (label, valor, cor) in enumerate(kpis):
    y = 0.78 - idx * 0.33
    ax2.text(0.5, y + 0.10, valor, ha="center", va="center",
             fontsize=22, fontweight="bold", color=cor,
             transform=ax2.transAxes)
    ax2.text(0.5, y - 0.01, label, ha="center", va="center",
             fontsize=9, color=MUTED, transform=ax2.transAxes)

ax2.set_title("Indicadores-Chave", color=TEXT, fontsize=12, pad=8)

# ── 3. Percentis nominal vs real ────────
ax3 = fig.add_subplot(gs[1, 0])
cenarios = ["P10\n(Pior)", "P25", "P50\n(Mediana)", "P75", "P90\n(Melhor)"]
vals_nom = [p10, p25, p50, p75, p90]
vals_rea = [np.percentile(patrimonios_reais, p) for p in [10, 25, 50, 75, 90]]
x = np.arange(len(cenarios))
w = 0.38
bars1 = ax3.bar(x - w/2, vals_nom, w, color=ACCENT, alpha=0.85, label="Nominal")
bars2 = ax3.bar(x + w/2, vals_rea, w, color=GREEN,  alpha=0.75, label="Real (hoje)")
ax3.axhline(META_PATRIMONIO, color=ORANGE, lw=1.5, ls="--", alpha=0.8)
ax3.set_xticks(x); ax3.set_xticklabels(cenarios, fontsize=8)
ax3.yaxis.set_major_formatter(fmt_reais)
ax3.set_title("Nominal vs. Valor Real\n(corrigido pela inflação)", color=TEXT, fontsize=10, pad=6)
ax3.legend(fontsize=8, framealpha=0.2)
ax3.grid(axis="y", alpha=0.4)

# ── 4. Distribuição da renda mensal ─────
ax4 = fig.add_subplot(gs[1, 1])
renda_clip = np.clip(rendas_mensais, 0, np.percentile(rendas_mensais, 99))
ax4.hist(renda_clip, bins=100, color=ORANGE, alpha=0.85, edgecolor="none")
ax4.axvline(RENDA_DESEJADA_MES, color=GREEN, lw=2, ls="--",
            label=f"Meta R$ {RENDA_DESEJADA_MES:,.0f}")
ax4.axvline(np.median(rendas_mensais), color=TEXT, lw=1.5, ls=":",
            label=f"Mediana R$ {np.median(rendas_mensais):,.0f}")
ax4.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"R$ {x:,.0f}"))
ax4.set_title("Renda Mensal na Aposentadoria\n(regra dos 4% a.a.)", color=TEXT, fontsize=10, pad=6)
ax4.set_xlabel("Renda mensal possível")
ax4.set_ylabel("Frequência")
ax4.legend(fontsize=8, framealpha=0.2)
ax4.grid(axis="y", alpha=0.4)

# ── 5. Pizza / prob de atingir meta ─────
ax5 = fig.add_subplot(gs[1, 2])
sizes  = [prob_meta, 100 - prob_meta]
colors = [GREEN, RED]
labels = [f"Atingem\n{prob_meta:.1f}%", f"Não atingem\n{100-prob_meta:.1f}%"]
wedges, texts = ax5.pie(sizes, colors=colors, startangle=90,
                         wedgeprops=dict(width=0.55, edgecolor=DARK_BG, linewidth=2))
ax5.text(0, 0, f"{prob_meta:.0f}%", ha="center", va="center",
         fontsize=20, fontweight="bold", color=GREEN)
ax5.legend(wedges, labels, loc="lower center", fontsize=8,
           bbox_to_anchor=(0.5, -0.08), framealpha=0.2)
ax5.set_title(f"Probabilidade de atingir\nR$ {META_PATRIMONIO/1e6:.0f} milhão", color=TEXT, fontsize=10, pad=6)

# ── 6. Evolução por cenário (trajetória) ─
ax6 = fig.add_subplot(gs[2, :2])

# Seleciona 3 simulações representativas dos percentis
def simular_trajetoria(rend, inf_men):
    pat = 0.0
    traj = [0.0]
    for m in range(MESES):
        aporte = APORTE_MENSAL
        pat = pat * (1 + rend) + aporte
        traj.append(pat)
    return traj

# P10, P50, P90
idx_p10 = np.argmin(np.abs(patrimonios_finais - p10))
idx_p50 = np.argmin(np.abs(patrimonios_finais - p50))
idx_p90 = np.argmin(np.abs(patrimonios_finais - p90))

traj_p10 = simular_trajetoria(rendimentos[idx_p10], inflacoes_mensais[idx_p10])
traj_p50 = simular_trajetoria(rendimentos[idx_p50], inflacoes_mensais[idx_p50])
traj_p90 = simular_trajetoria(rendimentos[idx_p90], inflacoes_mensais[idx_p90])

meses_eixo = np.arange(MESES + 1)
anos_eixo  = meses_eixo / 12

ax6.fill_between(anos_eixo, traj_p10, traj_p90, alpha=0.15, color=ACCENT)
ax6.plot(anos_eixo, traj_p90, color=GREEN,  lw=2,   label=f"Melhor (P90) — {fmt_reais(p90, None)}")
ax6.plot(anos_eixo, traj_p50, color=ACCENT, lw=2.5, label=f"Mediana (P50) — {fmt_reais(p50, None)}")
ax6.plot(anos_eixo, traj_p10, color=RED,    lw=2,   label=f"Pior (P10) — {fmt_reais(p10, None)}")
ax6.axhline(META_PATRIMONIO, color=ORANGE, lw=1.5, ls="--", alpha=0.8, label="Meta R$ 1M")
ax6.yaxis.set_major_formatter(fmt_reais)
ax6.set_xlabel("Anos de contribuição")
ax6.set_ylabel("Patrimônio acumulado")
ax6.set_title("Trajetória do Patrimônio — Três Cenários", color=TEXT, fontsize=11, pad=8)
ax6.legend(fontsize=9, framealpha=0.2)
ax6.grid(alpha=0.3)

# ── 7. Sensibilidade: rend x patrimônio ─
ax7 = fig.add_subplot(gs[2, 2])
scatter_x = rendimentos * 100
scatter_y = patrimonios_finais / 1e6
ax7.scatter(scatter_x, scatter_y, s=0.3, alpha=0.3, color=ACCENT)
ax7.axhline(META_PATRIMONIO / 1e6, color=ORANGE, lw=1.5, ls="--", alpha=0.8)
ax7.set_xlabel("Rendimento mensal (%)")
ax7.set_ylabel("Patrimônio final (R$ M)")
ax7.set_title("Sensibilidade:\nRendimento × Patrimônio", color=TEXT, fontsize=10, pad=6)
ax7.grid(alpha=0.3)

plt.savefig("/mnt/user-data/outputs/simulacao_monte_carlo_aposentadoria.png",
            dpi=160, bbox_inches="tight", facecolor=DARK_BG)
print("\nGráfico salvo!")
