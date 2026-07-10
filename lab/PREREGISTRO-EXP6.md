# Pré-registro — Experimento 6 ("Chronos": o tempo como eixo operável)
Data: 2026-07-10, ANTES de qualquer embedding das formas flexionadas.

## Hipótese (do usuário + anatomia dos Exp 4-5)
O tempo é uma grandeza do espectro: (a) existe uma direção única passado→futuro;
(b) A MANCHETE — a transmutação geométrica que FALHOU entre antônimos (corpos
distintos, Exp 5) deve FUNCIONAR entre tempos do mesmo verbo (corpo idêntico por
construção): e(amei) + v_tempo deve aterrissar em "amarei";
(c) tempo e intenção são eixos independentes (ortogonais) — o 4º dia da Gênese.

## Materiais (congelados)
- 12 pares (pretérito perfeito 1ª sg, futuro 1ª sg): amei/amarei, comprei/
  comprarei, ganhei/ganharei, vendi/venderei, comi/comerei, escrevi/escreverei,
  perdi/perderei, subi/subirei, abri/abrirei, dormi/dormirei, fiz/farei, fui/irei.
- RECORTE CÉTICO: irregulares fiz/farei e fui/irei (radicais distintos; fui/irei
  não compartilham NADA de forma). Se a tese cética ("a direção do tempo é só
  morfologia -ei→-rei") for verdadeira, o LOO e o transplante FALHAM neles.
- Banco de ranking: 227 infinitivos + 24 formas flexionadas = 251 itens.
- Espaços reconstruídos sobre os 251 pelo método EXATO do Exp 4 (bge-m3, centrar,
  remover k=50 eixos de trigrama). Primário: purificado; centrado = controle.
- v_tempo = média L2(e(futuro) − e(passado)); leave-one-out nos 12 pares;
  transplante: q = L2(e(src) ± s·v), s = projeção média dos 11 pares do fold.
- v_intenção: recomputada no espaço novo com os 12 pares de antônimos (ordem
  do dataset.json, inalterada). Controle: v_rand gaussiana, seed 136.
- Nota declarada: "fui" também é passado de "ser" (ambiguidade real do pt);
  característica do material, não defeito.

## Gates (selados)
G-T1 (direção do tempo, LOO): proj(futuro) > proj(passado) no par excluído em
     >= 10/12; controle aleatório <= 8/12.
G-T2 (a transmutação, MANCHETE): das 24 queries transplantadas (12 ida, 12 volta):
     alvo no top-5 em >= 12/24 E rank melhora vs baseline sem transplante em
     >= 17/24 E o controle aleatório não atinge nenhum dos dois critérios.
G-T3 (ortogonalidade): |cos(v_tempo, v_intenção)| <= 0.25.

## Aposta pessoal do agente (placar na noite: 8 acertos, 4 erros)
G-T1: 12/12. G-T2: PASSA (~18/24 top-5) — a anatomia prevê transmutação onde o
corpo coincide. G-T3: passa com |cos| < 0.15. Irregular mais difícil: fui+v acha
"irei" no top-10 mas não no top-5.

## Regra de parada
Uma rodada. Sem métrica nova após os números.
