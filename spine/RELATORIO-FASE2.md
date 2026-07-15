# Relatório — Fase 2 ("a sombra é auditada")
Data: 2026-07-15. Selo: PREREGISTRO-FASE2.md + ADENDO (interpretações
ex-ante). Nenhuma métrica adicionada após os dados.

## Janela
Aberta pelo relógio de EVENTOS na leitura estrita do adendo: 36/30
eventos únicos pós-marco nos streams selados, aos 5,0 de 7 dias.
Operação do período: 0 ticks falhos no shadowd.log.

## Amostra e rotulagem
26 itens únicos = união dedupe de top-10 por score (bug_win_en v1.0.0)
+ 10 aleatórios (seed 136) + 10 primeiros cronológicos; shuffle seed
136; lista sem scores (f2_amostra.md, commitada ANTES da rotulagem com
o sha256 do mapping como prova de pré-selagem: 344949a0…).
Rotulador: agente CEGO distinto do selador (Opus, id a5d7278aedf553d20,
zero contexto da campanha, zero tools) — conforme o selo ("Max ou
agente distinto do que selou"). Resultado: 21 severos / 5 benignos; os
5 benignos são as 2 retratações/transientes, o flake de CI declarado,
a fricção de UX e o relato de vitória — rotulagem semanticamente fina.

## G-F2a (utilidade)
- top-10 ranqueado: 9/10 severos
- fila cronológica: 7/10 severos
- aleatório (exploratório, sem gate): 8/10
**9 >= 7 + 2 → PASSA — margem exata, sem folga.** Honestidade: a
taxa-base severa do período foi altíssima (21/26 = 81%), comprimindo a
diferença possível entre grupos; ainda assim o ranking venceu. O único
benigno do top-10 (n17, 9º lugar) é o flake de CI — léxico bug-like,
semântica de flake: a classe de FP já caracterizada do dial (lê tom,
não verdade; SINGLE_ENCODER rider vale).

## G-F2b (operação)
- Zero crash-loop: 0 "FAILED" no shadowd.log do período. ✓
- Tick de rotina <= 1 s (leitura do adendo §2): 0,04-0,09 s medido
  pós-conserto (lazy numpy + throttle GitHub). ✓
- Nenhuma escrita fora de ~/.m1nd/synt0ny/: revisão de código + nenhum
  arquivo do m1nd alterado pelo shadowd. ✓
**PASSA.**

## Decisão selada — aplicada
G-F2a E G-F2b passam → **a espinha SAI DA SOMBRA (T0.1)**: scores
anotados visíveis, ainda advisory absoluto (a constituição não muda:
gauges nunca escrevem/decidem/bloqueiam; riders cap em reverify).
Passo mínimo aplicado já: o painel desvela scores por default (o véu
existia para proteger o rotulador cego; a auditoria fechou).
Desenho pendente COM o Max: onde vivem os "alerts anotados" — nunca em
arquivo do m1nd (advisory absoluto); candidato: arquivo próprio em
~/.m1nd/synt0ny/ que consumidores leem via MCP/painel.

## Ata
- f2_mapping.json (grupos+scores, selado antes da rotulagem)
- f2_rotulos.json (rótulos do agente cego + contagem dos gates)
- Aposta do agente no selo: "6-7 severos no top-10 vs 2-3 na crono" —
  direção certa, magnitude errada nos DOIS lados (viés de subestimar a
  taxa-base severa de field-reports; consistente com o viés histórico
  de subestimar tarefas de leitura, registrado no PATHOS).
