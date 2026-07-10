# synt0ny

Busca semântica por ressonância + eixo da intenção, para verbos pt-BR.
Consolidação executável dos 6 experimentos pré-registrados de 2026-07-10
(caderno completo, hashes e dados brutos em `lab/`).

O que está por trás (tudo medido, ver `lab/PREREGISTRO*.md`):

- Espectros bge-m3 locais (Ollama), determinísticos (Δ = 0,0).
- Espaço purificado de forma — o "firmamento" (Exp 4): remove os 50 eixos de
  trigrama que carregavam 31,4% da variância; parônimos (casar/caçar) deixam
  de ressoar (d 3,74 → −1,85) e o sentido sobrevive (hit@5 59,5%).
- Eixo da intenção (Exp 5): direção única aprendida de 12 pares de antônimos,
  separa positivo/negativo em 12/12 no leave-one-out; ortogonal ao eixo do
  tempo (cos = −0,01, Exp 6).

## Uso

```
venv/bin/python3 synt0ny.py buscar <verbo>       # vizinhos por ressonância
venv/bin/python3 synt0ny.py intencao <verbo>...  # posição no eixo ⊖/⊕
venv/bin/python3 synt0ny.py eixo                 # extremos do eixo no banco
```

Palavras fora do banco de 227 funcionam (zero-shot): o espectro é gerado na
hora e passa pelo mesmo pipeline de purificação. Requer Ollama local com
`bge-m3`. Primeira execução constrói `cache.npz` (~3 s).

## Limites conhecidos (honestidade de laboratório)

- A purificação linear é agressiva: separa parônimos, mas mutila pares cuja
  semelhança legítima corre paralela à forma (flexões do mesmo verbo — Exp 6).
- O eixo da intenção separa polaridade; NÃO transmuta (refletir "amar" não
  produz "odiar" — Exp 5). Atributos são direções; identidades são regiões.
