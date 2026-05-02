"""
Simulação M/M/1 - Teoria de Filas
λ=1, μ=2, FIFO — 5 réplicas de 1.000.000 eventos cada

Variáveis (conforme quadro da professora):
    a_i : instante de chegada
    b_i : início do atendimento
    c_i : fim do atendimento
    w_i : tempo de espera na fila  = b_i - a_i
    u_i : tempo de serviço         = c_i - b_i
    o_i : tempo ocioso do servidor = b_i - c_{i-1}
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# ─── Parâmetros ────────────────────────────────────────────────────────────────
LAMBDA     = 1
MU         = 2
N          = 1_000_000
N_REPLICAS = 5

# Valores teóricos M/M/1
rho_teo = LAMBDA / MU
Wq_teo  = rho_teo / (MU * (1 - rho_teo))   # = 0.5

print("=" * 55)
print(f"  Simulação M/M/1 | λ={LAMBDA} μ={MU} N={N:,} réplicas={N_REPLICAS}")
print(f"  Teórico: Wq={Wq_teo:.6f}  ρ={rho_teo:.6f}")
print("=" * 55)

# ─── Figura com subplots (2 por réplica: Wq e ρ) ──────────────────────────────
fig, axes = plt.subplots(N_REPLICAS, 2, figsize=(14, N_REPLICAS * 3))
fig.suptitle(f"Simulação M/M/1 | λ={LAMBDA}, μ={MU}, N={N:,}", fontsize=13, fontweight='bold')
plt.subplots_adjust(hspace=0.5, wspace=0.3)

resultados_Wq  = []
resultados_rho = []

for rep in range(N_REPLICAS):
    rng = np.random.default_rng(rep)

    # ── Gerar tempos ────────────────────────────────────────────────────────
    inter_chegadas = rng.exponential(1 / LAMBDA, N)
    tempos_servico = rng.exponential(1 / MU,     N)

    # ── Calcular a_i, b_i, c_i ─────────────────────────────────────────────
    a = np.cumsum(inter_chegadas)
    b = np.empty(N)
    c = np.empty(N)

    b[0] = a[0]
    c[0] = b[0] + tempos_servico[0]
    for i in range(1, N):
        b[i] = max(a[i], c[i - 1])
        c[i] = b[i] + tempos_servico[i]

    # ── Métricas ────────────────────────────────────────────────────────────
    w = b - a
    u = tempos_servico
    o = np.empty(N)
    o[0] = b[0]
    o[1:] = np.maximum(0.0, b[1:] - c[:-1])

    # ── Médias cumulativas ──────────────────────────────────────────────────
    indices = np.arange(1, N + 1)
    Wq_cum  = np.cumsum(w) / indices
    rho_cum = np.cumsum(u) / (a + u)

    Wq_final  = Wq_cum[-1]
    rho_final = np.sum(u) / (c[-1] - a[0])

    resultados_Wq.append(Wq_final)
    resultados_rho.append(rho_final)

    print(f"  Réplica {rep+1}: Wq = {Wq_final:.6f}   ρ = {rho_final:.6f}")

    # ── Gráfico Wq ──────────────────────────────────────────────────────────
    ax1 = axes[rep, 0]
    ax1.plot(indices, Wq_cum, color='steelblue', lw=0.5,
             label='Tempo médio de fila Wq')
    ax1.axhline(Wq_teo, color='tomato', lw=1.2, ls='--',
                label='Tempo médio de fila teórico')
    ax1.set_title(f"Réplica {rep+1} — Wq simulado x Teórico para fila M/M/1", fontsize=9)
    ax1.set_xlabel("Numero de Pontos", fontsize=8)
    ax1.set_ylabel("Tempo médio na fila", fontsize=8)
    ax1.legend(fontsize=7)
    ax1.set_xlim(0, N)

    # ── Gráfico ρ ───────────────────────────────────────────────────────────
    ax2 = axes[rep, 1]
    ax2.plot(indices, rho_cum, color='steelblue', lw=0.5,
             label='Ociosidade Servidor Simulado')
    ax2.axhline(rho_teo, color='tomato', lw=1.2, ls='--',
                label='Ociosidade Servidor Teórico')
    ax2.set_title(f"Réplica {rep+1} — p simulado x Teórico para fila M/M/1", fontsize=9)
    ax2.set_xlabel("Numero de Pontos", fontsize=8)
    ax2.set_ylabel("Taxa de ocupação", fontsize=8)
    ax2.legend(fontsize=7)
    ax2.set_xlim(0, N)

# ─── Resumo final ──────────────────────────────────────────────────────────────
print("=" * 55)
print(f"  Média Wq  = {np.mean(resultados_Wq):.6f}  (teórico {Wq_teo:.6f})")
print(f"  Média ρ   = {np.mean(resultados_rho):.6f}  (teórico {rho_teo:.6f})")
print("=" * 55)

output_path = SCRIPT_DIR / "simulacao_mm1.png"
plt.savefig(output_path, dpi=120, bbox_inches='tight')
print(f"Gráfico salvo: {output_path}")
