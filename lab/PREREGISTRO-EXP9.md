# Pré-registro — Experimento 9 ("o paradigma dos irmãos") — FINAL
Data: 2026-07-10. Desenho: proposta fable (panel) + verdict fugu CHANGE aplicado
integralmente (3 achados). Selo SHA-256 ANTES de qualquer embedding.

## Hipótese
A transmutação geométrica falhou entre corpos distintos (Exp 5). Aqui os corpos
são idênticos (flexões do MESMO verbo): somar v_tempo ao pretérito deve
aterrissar no futuro do próprio verbo, julgado só entre os irmãos.

## Leitura honesta selada (achado 2 do fugu)
Um resultado positivo geral prova "eixo operável do paradigma morfotemporal".
A leitura mais forte — tempo SEMÂNTICO, não geometria de sufixo — depende do
falsificador supletivo F1b abaixo. As duas leituras ficam separadas por gate.

## Materiais
- 12 verbos × 5 formas 1ª sg (amo/amei/amava/amarei/amaria etc.; fazer e ir
  com paradigmas irregulares; fui→irei sem forma compartilhada). 60 espectros
  bge-m3 CRUS + 227 do banco para centragem; sem purificação.
- v_tempo: LOO nos 12 pares (perfeito, futuro); passo s = projeção média do fold.
- Julgamento: argmax de cosseno entre os 4 irmãos (acaso 25%).
  Ida: perfeito+s·v → alvo futuro. Volta: futuro−s·v → alvo perfeito.
- MARGEM POR ITEM (achado 3): acerto só é VÁLIDO se top1 = alvo E
  (cos_top1 − cos_top2) >= 0.001; item com margem < 0.001 = "instável",
  reportado à parte. Se > 50% dos itens forem instáveis → teto do instrumento,
  resultado TERMINAL.
- NULL EMPÍRICO (achado 1): 300 direções gaussianas unitárias (seed 136), cada
  uma rodando o protocolo completo (24 trials com margem, mesmo passo s do
  fold); distribuição do total de acertos → p95.
- Baseline sem transplante (argmax cos direto) reportado.

## Gates (selados)
G1 (transmutação): ida >= 9/12 válidos E volta >= 9/12 válidos.
G2 (null empírico): total real (ida+volta) > p95 do null de 300 direções.
F1a (decoy morfológico): condicional vence >= 6/12 idas → componente
    morfológica domina; manchete enfraquecida.
F1b (falsificador supletivo — separa sufixo de tempo): se ir E fazer somarem
    0/4 acertos válidos (ida+volta), o resultado positivo é declarado
    "geometria de sufixo", NÃO tempo semântico — mesmo com G1 aprovado.
    >= 1/4 nos supletivos mantém a leitura temporal viva; >= 2/4 a fortalece.
F2 (resolução): sim média irmão-irmão > 0.995 OU > 50% itens instáveis →
    teto do instrumento, terminal.

## Aposta do agente (calibrada baixo, viés documentado no PATHOS)
Ida 8/12, volta 7/12 (G1 falha por pouco), G2 passa, decoy 3/12,
supletivos 1/4 (leitura temporal sobrevive por um fio).

## Regra de parada
Uma rodada. Sem métrica nova após os números.
