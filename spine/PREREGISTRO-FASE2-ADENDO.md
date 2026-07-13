# Adendo ao pré-registro da Fase 2 — interpretações fixadas ex-ante
Data: 2026-07-13, ANTES de qualquer rotulagem. O selo original
(PREREGISTRO-FASE2.md) permanece intacto; nenhum gate muda. Este adendo
só FIXA a leitura de termos que o selo deixou ambíguos, e o faz antes
que a leitura possa decidir o resultado.

## 1. "Evento" = texto único, não envelope
O selo (T0) tinha 1 dial; cada evento gerava 1 envelope. O shadowd v1.1
passou a emitir 1 envelope POR DIAL (2× por evento). Leitura fixada:
evento = input_sha256 único pós-marco nos sources selados
(field-reports.jsonl, inbox.jsonl). Estado nesta data: 23/30 —
**a janela NÃO abriu**. Abre com 30 eventos únicos OU em
2026-07-17T21:50 (7 dias corridos), o que vier primeiro.
O painel dizia "JANELA ABERTA" contando envelopes (46) — overclaim de
display, corrigido nesta data (paneld conta sha únicos).

## 2. G-F2b, cláusula "nenhum tick incremental > 1 s"
Leitura fixada (âncora: o próprio selo distingue "backlog de 100 eventos
em 7,5 s" de "tick incremental no-op silencioso"): a cláusula rege o
tick de ROTINA SEM material novo (no-op), wall-clock da invocação.
Ticks que colhem material pagam custo unitário caracterizado — embed
Ollama ~2,5-3 s/texto novo; sonda GitHub ~1-8 s no máx. 1×/30 min — e
são julgados pelas outras cláusulas (zero crash-loop; nenhuma escrita
fora de ~/.m1nd/synt0ny/) + ausência de crescimento patológico.
Consertos de instrumento aplicados ANTES do fechamento: import lazy do
numpy + throttle da sonda GitHub. No-op medido pós-conserto: 0,04-0,09 s
(3 medições; antes: 1,3 s).

## 3. Ensaio de amostragem descartado
Em 2026-07-13 uma amostra foi selada por engano sob a leitura
envelope-count (painel). NENHUMA rotulagem ocorreu; scores foram vistos
apenas pelo selador (papel já autorizado a vê-los); o mapping foi
deletado. No fechamento real a amostra será re-selada pelo procedimento
do selo: top-10 por score + 10 aleatórios (seed 136) + 10 cronológicos,
união com dedupe por sha, shuffle (seed 136), lista SEM scores.

## 4. Rotulador
Inalterado: Max ou agente distinto do selador, vendo apenas os textos.
