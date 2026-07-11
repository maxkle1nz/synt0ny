# Pré-registro — Experimento 15 ("tipo de commit": feat ↔ fix)
Data: 2026-07-11. Selo ANTES de qualquer embedding. Justificativa sem novo
verdict: desenho herda integralmente o Exp 13 (classificação binária com
ground truth externo + null matched), auditado 3× pelo panel nesta campanha.
PUREZA declarada: os 24 exemplos são autorais; o agente viu 5 subjects do
m1nd no Exp 14 (transcritos no placar) — os exemplos não derivam deles.

## Hipótese
Uma régua feat↔fix de 12+12 descrições autorais EN distingue, pela DESCRIÇÃO
SEM O PREFIXO, commits rotulados feat vs fix pela convenção do próprio repo —
rótulos automáticos, zero curadoria manual. Se passar, nasce o dial que
classifica tipo de commit em repos SEM convenção (telemetria de portfólio:
quanto do giro é construção vs conserto) — NUNCA previsão de risco (Exp 14).

## Materiais (congelados)
- Corpus: commits não-merge do ~/m1nd com subject casando ^(feat|fix)[(:]
  (contagem prévia: 243 feat + 130 fix). Texto = descrição APÓS o prefixo e
  o escopo (strip de "tipo(escopo):" / "tipo:"), rótulo = o prefixo removido.
- Régua: v = unit(mean(12 feat autorais) − mean(12 fix autorais)),
  exemplos congelados em exp15.py (selado junto). Encoder bge-m3 cru L2.
- Null matched: 300 eixos 12-vs-12 de descrições aleatórias do corpus.
- Transferência (exploratório, sem gate): mesmo teste em ~/l00p e ~/synt0ny
  se houver >= 20 commits convencionais; senão, declarado insuficiente.

## Gates (selados)
G1: AUC(projeção → rótulo feat/fix) >= 0.80 E > p95 do null matched.
G2 (utilidade): precision@20 do topo-fix >= 1.5× a taxa-base de fix.

## Aposta do agente
AUC 0,87 (descrições de feat e fix têm léxicos bem distintos; tarefa de
leitura — histórico manda não subestimar). G2 passa.

## Regra de parada
Uma rodada. Sem métrica nova após os números.
