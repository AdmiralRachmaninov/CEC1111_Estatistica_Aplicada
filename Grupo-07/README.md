# Simulação de Filas M/M/1

Atividade prática da disciplina de **Estatística** — Prof. Drª Maria José Pereira Dantas  
Pontifícia Universidade Católica de Goiás (PUC Goiás)

---

## Descrição

Simulação computacional de um sistema de filas **M/M/1** com disciplina **FIFO**, validando os resultados analíticos por meio de eventos discretos implementados em Python.

**Parâmetros:**
- Taxa de chegada: λ = 1 cliente/min (TMEC = 1 min)
- Taxa de atendimento: μ = 2 clientes/min (TMA = 0,5 min)
- Fator de utilização: ρ = λ/μ = 0,5 (50%)
- Réplicas: 5 independentes
- Eventos por réplica: 1.000.000

---

## Estrutura

```
.
├── simulacao_mm1.py       # Código Python da simulação
├── Figuras/
│   └── simulacao_mm1.png  # Gráfico gerado pelo script
└── README.md
```

---

## Como executar

**Requisitos:** Python 3.8+, NumPy, Matplotlib

```bash
pip install numpy matplotlib
python simulacao_mm1.py
```

O script gera o gráfico `simulacao_mm1.png` na mesma pasta e imprime no terminal:
- Tabela com Wq e ρ de cada réplica
- Média e variância do conjunto de simulações
- Primeiros 10 clientes com todas as variáveis (aᵢ, bᵢ, cᵢ, wᵢ, uᵢ, oᵢ)

---

## Resultados obtidos

| Réplica | Ŵq | ρ̂ |
|---|---|---|
| 1 | 0,500536 | 0,500004 |
| 2 | 0,503565 | 0,501492 |
| 3 | 0,500982 | 0,499605 |
| 4 | 0,502286 | 0,500613 |
| 5 | 0,497042 | 0,498628 |
| **Média** | **0,500882** | **0,500068** |
| **Variância** | **6,01 × 10⁻⁶** | **1,15 × 10⁻⁶** |
| **Teórico** | **0,500000** | **0,500000** |

Erro médio: **0,18%** em Wq e **0,01%** em ρ.

---

## Referências

- PEREIRA, M. M.; DANTAS, M. J. P. Aplicação da modelagem e simulação nos sistemas de filas M/M/s. *Revista Produção Online*, v. 17, n. 1, pp. 49–75, 2017.
- CHWIF, L.; MEDINA, A. C. *Modelagem e Simulação de Eventos Discretos*. 3. ed. São Paulo, 2010.
- ROSS, S. M. *Introduction to Probability Models*. 11. ed. Academic Press, 2014.

---

## Autores

| Nome | Matrícula | Curso |
|---|---|---|
| Victor de Melo Lima Evangelista | 20232003800032 | Engenharia Elétrica |
| Santiago Oliveira Diniz | 20221011800334 | Engenharia de Controle e Automação |
| Artur Soares Bento | 20221011800180 | Engenharia de Controle e Automação |
| Pedro Francisco Lopes de Oliveira | 20212011800084 | Engenharia de Controle e Automação |
