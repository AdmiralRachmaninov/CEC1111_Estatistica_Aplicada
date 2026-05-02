"""
Simulação de Fila M/M/1 — Chwif & Medina / Marina Meireles
λ=1, μ=2, n=10.000 clientes, 8 replicações
Saídas:
  - Console  : tabela resumo por replicação + estatísticas do conjunto
  - PNG 1    : convergência Wq (8 gráficos) + boxplot resumo
  - PNG 2    : tabela com as primeiras 20 linhas de cada variável (rep 1)
  - CSV      : tabela completa de todas as variáveis da replicação 1
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import csv, os

# ═══════════════════════════ PARÂMETROS ══════════════════════════════════════
LAMBDA      = 1.0
MU          = 2.0
N_CLIENTES  = 10_000
N_REPLIC    = 8
SEED_BASE   = 42

rho_teo = LAMBDA / MU                        # 0.50
Wq_teo  = LAMBDA / (MU * (MU - LAMBDA))      # 0.50 min

# Paleta de 8 cores
CORES = ["#E63946","#2A9D8F","#F4A261","#457B9D",
         "#A8DADC","#E9C46A","#9B5DE5","#F15BB5"]

BG      = "#0D1B2A"
PANEL   = "#162032"
GRID_C  = "#1E3050"
TICK_C  = "#8BA3C1"
LABEL_C = "#C8D8E8"
GOLD    = "#FFD166"

# ═══════════════════════════ NÚCLEO ══════════════════════════════════════════
def simular_mm1(n: int, lam: float, mu: float, seed: int, guardar_tabela=False):
    """
    Retorna dict com métricas finais, séries acumuladas, e (opcionalmente)
    a tabela linha-a-linha [ri, si, ai, bi, ci, wi, ui, oi].
    """
    random.seed(seed)

    wq_acum  = []
    rho_acum = []
    tabela   = [] if guardar_tabela else None

    soma_wi = soma_oi = 0.0
    ci_ant  = ai = 0.0

    for i in range(n):
        ri = random.expovariate(lam)
        si = random.expovariate(mu)

        ai = (ri if i == 0 else ai + ri)
        bi = max(ai, ci_ant)
        ci = bi + si
        wi = bi - ai          # espera na fila
        ui = ci - ai          # tempo total no sistema
        oi = max(0.0, bi - ci_ant)  # ociosidade do servidor

        soma_wi += wi
        soma_oi += oi
        ci_ant   = ci

        wq_acum.append(soma_wi / (i + 1))
        rho_acum.append(1.0 - soma_oi / ci_ant if ci_ant > 0 else 0.0)

        if guardar_tabela:
            tabela.append({
                "cliente": i,
                "ri": ri, "si": si,
                "ai": ai, "bi": bi, "ci": ci,
                "wi": wi, "ui": ui, "oi": oi
            })

    Wq_final  = soma_wi / n
    rho_final = 1.0 - soma_oi / ci_ant

    return dict(Wq_final=Wq_final, rho_final=rho_final,
                wq_acum=wq_acum, rho_acum=rho_acum, tabela=tabela)


# ═══════════════════════════ EXECUTA ═════════════════════════════════════════
resultados = []
print("=" * 72)
print(f"  Fila M/M/1  │  λ={LAMBDA}  μ={MU}  n={N_CLIENTES:,}  │  "
      f"ρ teórico={rho_teo:.4f}   Wq teórico={Wq_teo:.4f} min")
print("=" * 72)
print(f"  {'Rep':>3}  {'Wq final (min)':>16}  {'Erro Wq':>9}  "
      f"{'ρ final':>10}  {'Erro ρ':>8}")
print("-" * 72)

for i in range(N_REPLIC):
    guardar = (i == 0)          # guarda tabela só da replicação 1
    res = simular_mm1(N_CLIENTES, LAMBDA, MU, SEED_BASE + i, guardar_tabela=guardar)
    resultados.append(res)
    eWq  = abs(res["Wq_final"]  - Wq_teo)  / Wq_teo  * 100
    erho = abs(res["rho_final"] - rho_teo) / rho_teo * 100
    print(f"  {i+1:>3}  {res['Wq_final']:>16.6f}  {eWq:>8.2f}%  "
          f"{res['rho_final']:>10.6f}  {erho:>7.2f}%")

# ─── estatísticas do conjunto ────────────────────────────────────────────────
Wq_vals  = np.array([r["Wq_final"]  for r in resultados])
rho_vals = np.array([r["rho_final"] for r in resultados])

media_Wq   = Wq_vals.mean()
var_Wq     = Wq_vals.var(ddof=1)
dp_Wq      = Wq_vals.std(ddof=1)
media_rho  = rho_vals.mean()
var_rho    = rho_vals.var(ddof=1)
dp_rho     = rho_vals.std(ddof=1)

print("=" * 72)
print(f"  Média  Wq  = {media_Wq:.6f}   Variância Wq  = {var_Wq:.8f}   DP = {dp_Wq:.6f}")
print(f"  Teórico Wq = {Wq_teo:.6f}   Erro médio   = {abs(media_Wq-Wq_teo)/Wq_teo*100:.3f}%")
print()
print(f"  Média  ρ   = {media_rho:.6f}   Variância ρ   = {var_rho:.8f}   DP = {dp_rho:.6f}")
print(f"  Teórico ρ  = {rho_teo:.6f}   Erro médio   = {abs(media_rho-rho_teo)/rho_teo*100:.3f}%")
print("=" * 72)

# ═══════════════════════════ PNG 1 — CONVERGÊNCIAS ═══════════════════════════
fig1 = plt.figure(figsize=(22, 14))
fig1.patch.set_facecolor(BG)
gs1 = gridspec.GridSpec(3, 3, figure=fig1,
                        left=0.05, right=0.97, top=0.91, bottom=0.06,
                        hspace=0.45, wspace=0.32)

fig1.suptitle(
    f"Fila M/M/1  │  λ={LAMBDA}  μ={MU}  n={N_CLIENTES:,}  │  8 Replicações  │  "
    f"Wq teórico={Wq_teo:.4f} min   ρ teórico={rho_teo:.4f}",
    fontsize=12, fontweight="bold", color="white", y=0.955)

def estilizar(ax, titulo, xl, yl):
    ax.set_facecolor(PANEL)
    ax.tick_params(colors=TICK_C, labelsize=7.5)
    ax.set_title(titulo, color="white", fontsize=9, fontweight="bold", pad=7)
    ax.set_xlabel(xl, color=LABEL_C, fontsize=7.5)
    ax.set_ylabel(yl, color=LABEL_C, fontsize=7.5)
    ax.grid(color=GRID_C, linewidth=0.5, linestyle="--")
    for s in ax.spines.values():
        s.set_edgecolor(GRID_C)

idx_clientes = np.arange(1, N_CLIENTES + 1)
posicoes8 = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1)]

for idx, (r, c) in enumerate(posicoes8):
    ax  = fig1.add_subplot(gs1[r, c])
    res = resultados[idx]
    cor = CORES[idx]

    ax.plot(idx_clientes, res["wq_acum"],
            color=cor, lw=0.8, alpha=0.85)
    ax.axhline(Wq_teo, color=GOLD, lw=1.5, ls="--", zorder=5)
    ax.axhline(res["Wq_final"], color=cor, lw=1.1, ls=":", alpha=0.75)

    estilizar(ax,
              f"Rep {idx+1}  —  Wq={res['Wq_final']:.4f}   ρ={res['rho_final']:.4f}",
              "Clientes", "Wq médio acumulado (min)")

    handles = [
        Line2D([0],[0], color=cor, lw=1.5, label=f"Wq acum. rep {idx+1}"),
        Line2D([0],[0], color=GOLD, lw=1.5, ls="--", label=f"Teórico {Wq_teo:.2f}"),
        Line2D([0],[0], color=cor,  lw=1.2, ls=":", label=f"Final {res['Wq_final']:.4f}"),
    ]
    ax.legend(handles=handles, fontsize=6, loc="upper right",
              facecolor=BG, edgecolor=GRID_C, labelcolor="white", framealpha=0.85)

# ─── painel resumo (posição 2,2) ─────────────────────────────────────────────
ax_r = fig1.add_subplot(gs1[2, 2])
ax_r.set_facecolor(PANEL)
for s in ax_r.spines.values(): s.set_edgecolor(GRID_C)
ax_r.tick_params(colors=TICK_C, labelsize=8)
ax_r.set_title("Resumo das 8 Replicações", color="white", fontsize=9, fontweight="bold", pad=7)

reps = np.arange(1, N_REPLIC + 1)
ax_r.bar(reps - 0.2, Wq_vals,  0.35, color=[CORES[i] for i in range(N_REPLIC)],
         alpha=0.85, label="Wq")
ax_r.bar(reps + 0.2, rho_vals, 0.35, color=[CORES[i] for i in range(N_REPLIC)],
         alpha=0.45, edgecolor="white", linewidth=0.6, label="ρ")
ax_r.axhline(Wq_teo,   color=GOLD, lw=1.4, ls="--")
ax_r.axhline(rho_teo,  color="#A0FFD0", lw=1.4, ls="--")
ax_r.axhline(media_Wq, color="white", lw=0.9, ls=":")
ax_r.set_xticks(reps)
ax_r.set_xticklabels([f"R{i}" for i in reps], color=LABEL_C, fontsize=8)
ax_r.grid(color=GRID_C, lw=0.5, ls="--", axis="y")
ax_r.set_xlabel("Replicação", color=LABEL_C, fontsize=7.5)
ax_r.set_ylabel("Valor", color=LABEL_C, fontsize=7.5)

leg_items = [
    mpatches.Patch(color=GOLD,     label=f"Wq teórico={Wq_teo:.4f}"),
    mpatches.Patch(color="#A0FFD0",label=f"ρ teórico={rho_teo:.4f}"),
    Line2D([0],[0], color="white", ls=":", label=f"Média Wq={media_Wq:.4f}"),
]
ax_r.legend(handles=leg_items, fontsize=6, facecolor=BG,
            edgecolor=GRID_C, labelcolor="white", framealpha=0.85)

path1 = "/mnt/user-data/outputs/sim_mm1_convergencias.png"
fig1.savefig(path1, dpi=150, bbox_inches="tight", facecolor=BG)
plt.close(fig1)
print(f"\n[✓] Gráficos de convergência salvos em {path1}")


# ═══════════════════════════ PNG 2 — TABELA VARIÁVEIS (primeiros 20 clientes) ═
tabela = resultados[0]["tabela"]  # replicação 1
N_SHOW = 20
colunas = ["cliente","ri","si","ai","bi","ci","wi","ui","oi"]
headers = ["i","rᵢ (TEC)","sᵢ (TMA)","aᵢ (chegada)","bᵢ (ini.aten.)",
           "cᵢ (fim aten.)","wᵢ (espera)","uᵢ (no sistema)","oᵢ (ocioso)"]

linhas = [[str(row["cliente"])] +
          [f"{row[c]:.5f}" for c in colunas[1:]]
          for row in tabela[:N_SHOW]]

fig2, ax2 = plt.subplots(figsize=(20, 8))
fig2.patch.set_facecolor(BG)
ax2.set_facecolor(BG)
ax2.axis("off")
ax2.set_title(
    f"Fila M/M/1 — Tabela de variáveis por cliente  (Replicação 1 · primeiros {N_SHOW} clientes)\n"
    f"λ={LAMBDA}  μ={MU}  ρ teórico={rho_teo}  Wq teórico={Wq_teo}",
    color="white", fontsize=11, fontweight="bold", pad=14)

col_widths = [0.045, 0.095, 0.095, 0.115, 0.115, 0.115, 0.105, 0.125, 0.105]
table = ax2.table(
    cellText   = linhas,
    colLabels  = headers,
    cellLoc    = "center",
    loc        = "center",
    colWidths  = col_widths,
)
table.auto_set_font_size(False)
table.set_fontsize(8.5)
table.scale(1, 1.7)

# Estilizar células
for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor(GRID_C)
    if row == 0:
        cell.set_facecolor("#1E3A5A")
        cell.set_text_props(color=GOLD, fontweight="bold", fontsize=8)
    else:
        cell.set_facecolor(PANEL if row % 2 == 0 else "#111D2C")
        # colorir coluna wi (índice 6) em destaque
        if col == 6:
            txt = cell.get_text().get_text()
            val = float(txt)
            cell.set_facecolor("#2A1A0A" if val > 0 else "#0A2A1A")
            cell.set_text_props(color="#F4A261" if val > 0 else "#2A9D8F")
        else:
            cell.set_text_props(color=LABEL_C)

path2 = "/mnt/user-data/outputs/sim_mm1_tabela_variaveis.png"
fig2.savefig(path2, dpi=150, bbox_inches="tight", facecolor=BG)
plt.close(fig2)
print(f"[✓] Tabela de variáveis salva em {path2}")


# ═══════════════════════════ CSV COMPLETO ════════════════════════════════════
path_csv = "/mnt/user-data/outputs/sim_mm1_rep1_completo.csv"
with open(path_csv, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=colunas)
    writer.writeheader()
    writer.writerows(tabela)
print(f"[✓] CSV completo (10.000 linhas) salvo em {path_csv}")


# ═══════════════════════════ TABELA RESUMO FINAL ══════════════════════════════
print("\n" + "═" * 72)
print("  TABELA RESUMO — 8 REPLICAÇÕES")
print("═" * 72)
print(f"  {'Rep':>3}  {'Wq simulado':>14}  {'ρ simulado':>12}  "
      f"{'Erro Wq':>9}  {'Erro ρ':>8}")
print("-" * 72)
for i, res in enumerate(resultados):
    eWq  = (res["Wq_final"]  - Wq_teo)  / Wq_teo  * 100
    erho = (res["rho_final"] - rho_teo) / rho_teo * 100
    print(f"  {i+1:>3}  {res['Wq_final']:>14.6f}  {res['rho_final']:>12.6f}  "
          f"{eWq:>+8.3f}%  {erho:>+7.3f}%")
print("-" * 72)
print(f"  {'Média':>3}  {media_Wq:>14.6f}  {media_rho:>12.6f}")
print(f"  {'Var.' :>3}  {var_Wq:>14.8f}  {var_rho:>12.8f}")
print(f"  {'DP'   :>3}  {dp_Wq:>14.8f}  {dp_rho:>12.8f}")
print("═" * 72)
print(f"  Teórico      Wq = {Wq_teo:.6f}       ρ = {rho_teo:.6f}")
print("═" * 72)
