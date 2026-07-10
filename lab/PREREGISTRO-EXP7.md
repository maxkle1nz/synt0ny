# Pré-registro — Experimento 7 ("a leitura por camadas")
Data: 2026-07-10, ANTES de qualquer decomposição. Proposta da 3ª voz (agente),
independente das propostas dos oráculos fable/fugu (despachados em paralelo,
sem conhecimento mútuo).

## Hipótese
A questão dos antônimos ficou inconclusiva 2× (R = 0,56 → 0,38) porque o
cosseno SOMA camadas com sinais opostos. Decomposição exata do produto
interno com o eixo da intenção v (unitário):
  x·y = (x·v)(y·v) + x⊥·y⊥   [c_eixo + c_corpo]
Predição da anatomia: antônimos DISSONAM na camada do eixo (c_eixo < 0 —
os polos cruzam o zero) e são INDEPENDENTES na camada do corpo
(c_corpo ≈ aleatórios). "Afinam ou dissonam?" tem resposta dupla, uma por
camada — e o R total nunca poderia vê-la.

## Método (congelado)
- Espaços do Exp 4 reconstruídos (build_spaces): purificado = primário,
  centrado = controle.
- ANTI-CIRCULARIDADE: para cada par de antônimos, c_eixo é medido com o eixo
  v_{-k} aprendido SEM aquele par (leave-one-out). Sinônimos e aleatórios
  usam o v global (não participaram do eixo — sem circularidade).
- Grupos: 21 pares sinônimos radical-distinto · 12 antônimos · 42 aleatórios
  (seed 136, mesmos de sempre).
- Nota: c_eixo < 0 NÃO é garantido pelo 12/12 do Exp 5 (separação exige só
  proj(pos) > proj(neg); dissonância exige cruzar o ZERO). É afirmação nova.

## Gates (selados)
P1 (dissonância no eixo): média c_eixo(antônimos) < 0 E < c_eixo(aleatórios)
   com permutação p < 0.01.
P2 (afinação no eixo, sinônimos): c_eixo(sinônimos) > c_eixo(aleatórios),
   p < 0.05.
P3 (corpos independentes): |d| de c_corpo(antônimos) vs c_corpo(aleatórios)
   < 0.5.
Interpretação selada: P1+P3 passando, a LACUNA 3 fecha — antônimos dissonam
na camada da intenção e são estranhos na camada do corpo; o R era
inconclusivo por construção. Reportar também a fração |c_eixo|/|x·y| por
grupo.

## Aposta pessoal do agente
P1 passa; P2 passa (fraco); P3 passa com |d| < 0.3. Placar na noite: acerto
eixos, erro saltos — isto é um teste de eixo.

## Regra de parada
Uma rodada. Sem métrica nova após os números.
