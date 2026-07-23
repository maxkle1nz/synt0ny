# Pré-registro — Janela 2 de auditoria da espinha
Data do selo: 2026-07-23. Selado ANTES de qualquer dado da janela.
Marco zero: 2026-07-23T04:00:00 (local). A janela 1 (Fase 2) foi
aprovada em 2026-07-15; esta é a primeira janela da confiança composta.

## Herança (idêntica por referência, sem re-litigação)
Desenho, amostra, cegueira, rotulador e G-F2a herdam VERBATIM de
PREREGISTRO-FASE2.md + PREREGISTRO-FASE2-ADENDO.md:
- Streams julgados: field-reports.jsonl + inbox.jsonl.
- Evento = input_sha256 único pós-marco (adendo §1).
- Janela: >= 7 dias corridos OU >= 30 eventos únicos, o que vier antes.
- Amostra: top-10 por score bug_win_en + 10 aleatórios (seed 136) +
  10 cronológicos; união dedupe; shuffle seed 136; lista SEM scores.
- Rotulador: Max ou agente distinto do selador, vendo só os textos.
- G-J2a = G-F2a: severos(top-10 ranqueado) >= severos(crono) + 2.

## G-J2b (operação) — herda o adendo §2 e ACRESCENTA uma cláusula
Herdado: zero crash-loop; tick no-op <= 1 s; nenhuma escrita fora de
~/.m1nd/synt0ny/. Acrescido pela lição do incidente 18-23/07:
nenhum silêncio do shadowd > 12 h COM a máquina ligada (julgável por
shadowd.log × uptime; período de máquina desligada não conta).

## Decisão selada
Passa tudo → confiança composta +1 e a fila de atenção (T0.1) segue.
Falha G-J2a → re-selagem da régua com exemplos held-out do período OU
rebaixamento honesto do dial no manifest. Falha G-J2b → conserto de
operação antes de qualquer nova janela.

## Aposta do agente
Ranked vence crono por +2 de novo, com taxa-base severa MENOR que os
81% da janela 1 (aquele período foi anormalmente denso em bug real);
chuto 60-70% de severos e ranked 8-9/10 vs crono 5-6/10.

## Regra de parada
Uma auditoria por janela. Sem métrica nova após ver os dados.
