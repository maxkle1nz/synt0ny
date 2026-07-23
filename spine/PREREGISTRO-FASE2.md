# Pré-registro — Fase 2 ("a sombra é auditada")
Data: 2026-07-11, selado NO DIA da instalação do shadowd, ANTES de qualquer
dado de sombra acumular. A sombra nasce sabendo como será julgada.

## O que está instalado (T0, estado no selo)
- Dial certificado: bug_win_en v1.0.0 (laudo Exp 13: AUC 0,853; bula anexa).
- shadowd.py via launchd com.synt0ny-shadowd, tick 300 s, advisory
  (shadow.jsonl em ~/.m1nd/synt0ny/; NUNCA escreve em arquivo do m1nd).
- Smoke: backlog de 100 eventos em 7,5 s; tick incremental no-op silencioso;
  envelopes v0 com governança no wire.

## Janela de auditoria
O que vier primeiro: >= 7 dias corridos OU >= 30 eventos NOVOS pós-selo
(offsets do smoke são o marco zero; o backlog histórico NÃO conta).

## Desenho da auditoria (cego)
1. Amostra: os 10 eventos novos de MAIOR score no dial + 10 eventos novos
   aleatórios (seed 136), embaralhados numa lista única SEM scores.
2. Rotulagem: o rotulador (Max ou agente distinto do que selou) marca cada um
   como severo (bug-like, exige atenção) ou benigno, vendo APENAS o texto.
3. Comparação: mesma rotulagem aplicada aos 10 PRIMEIROS eventos em ordem
   cronológica do período (a fila que existe hoje, sem synt0ny).

## Gates (selados)
G-F2a (utilidade): nº de severos no top-10 ranqueado >= nº de severos na
  fila cronológica + 2. (A espinha precisa VENCER o status quo com margem,
  não empatar.)
G-F2b (operação): zero crash-loop no shadowd.log; nenhum tick incremental
  > 1 s (exceto o primeiro pós-boot); nenhuma escrita fora de
  ~/.m1nd/synt0ny/.
Decisão selada: G-F2a E G-F2b passam → a espinha sai da sombra (T0.1:
  scores anotados visíveis em alerts, ainda advisory). Qualquer falha →
  re-selagem da régua com exemplos reais held-out do período, OU
  arquivamento honesto da espinha com número.

## Aposta do agente
G-F2a passa com 6-7 severos no top-10 vs 2-3 na cronológica. G-F2b passa
limpo. Risco real: volume — se o período render < 30 eventos e < 7 dias de
variedade, a auditoria adia, não se força.

## Regra de parada
Uma auditoria por janela. Sem métrica nova após ver os dados da sombra.
