# Pré-registro — Experimento 5 ("a reflexão hermética")
Data: 2026-07-10, ANTES de qualquer computação de direções de polaridade.

## Hipótese (do usuário, via princípio hermético)
"Amar e odiar são a mesma coisa; o que muda é a intenção." Tradução operacional:
antônimos compartilham o corpo do espectro e diferem ao longo de UMA direção
comum — a INTENÇÃO (v_pol). Se ela existe: (a) projetar nela separa positivo de
negativo; (b) REFLETIR um verbo através do hiperplano perpendicular
(Householder: x − 2(x·v)v) deve transformá-lo no próprio antônimo.

## Materiais (congelados)
- Espaço primário dos gates: PURIFICADO do Exp 4 (bge-m3, centrado, forma
  removida). Espaço apenas-centrado reportado como controle de atribuição.
- 12 pares de antônimos do dataset.json, ordem [positivo, negativo] gravada
  DESDE O EXP 1 (rotulagem imune a ajuste presente).
- v_pol: média L2-normalizada de e(positivo) − e(negativo).
- Validação leave-one-out: v_pol aprendida com 11 pares, testada no 12º.
- Controle: direção aleatória gaussiana v_rand (seed 136, L2), mesmas contas.

## Gates e predições (selados)
P1 (separação de polaridade, LOO): acerto = proj(positivo) > proj(negativo) no
   par excluído. Sucesso: >= 10/12 com v_pol E <= 8/12 com v_rand (acaso ~6).
P2-forte (a reflexão hermética, tese do usuário): das 24 reflexões (12 pares ×
   2 direções), o antônimo verdadeiro aparece no top-5 do ranking da query
   refletida em >= 12/24 (50%). Baseline reportado: rank do antônimo SEM
   reflexão. Controle: reflexão por v_rand não melhora a mediana dos ranks.
P2-fraca: a mediana dos ranks cai para <= 50% da mediana sem reflexão
   (melhora real, sem atingir a forma forte).
P3 (exploratório, sem gate): projetar os 227 verbos em v_pol (12 pares) e
   inspecionar os extremos — o eixo da intenção existe como dimensão global?
   Reportar top-10 de cada ponta.

## Aposta pessoal do agente (placar na noite: 6 acertos, 3 erros)
P1 passa (>= 10/12). P2-forte FALHA e P2-fraca passa: a intenção existe como
direção, mas não é UM eixo universal — pares afetivos (amar/odiar) refletem
melhor que espaciais (abrir/fechar). O usuário ganha parcial; a forma plena
exige fase por domínio, não uma polaridade única.

## Regra de parada
Um experimento, uma rodada. Sem métrica nova após os números.
