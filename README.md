# synt0ny

Laboratório de geometria semântica local + **a espinha**: um motor advisory
de discernimento que lê fluxos de texto com embeddings locais (Ollama,
`bge-m3`) e ordena a atenção de quem opera — sem LLM no caminho quente,
sem rede, sem nunca decidir nada sozinho.

Nasceu em 2026-07-10 de uma conversa sobre matrizes e LLMs. As hipóteses
especulativas morreram nos primeiros pré-registros (estão no `lab/`, com
número); o que sobreviveu aos gates virou instrumento. Em cinco dias a
campanha foi da primeira medição a uma auditoria cega de produção aprovada.

## O que está provado (cada número tem selo antes dos dados e laudo)

- **Firmamento** (Exp 4): 31,4% da variância do espectro `bge-m3` é forma
  ortográfica, removível por regressão de 50 eixos de trigrama; parônimos
  (casar/caçar) deixam de ressoar (d 3,74 → −1,85) e o sentido sobrevive.
- **Eixo da intenção** (Exp 5): direção única de 12 pares de antônimos,
  12/12 no leave-one-out, ortogonal ao eixo do tempo (cos −0,01, Exp 6).
- **Dial `bug_win_en`** (Exp 13): AUC 0,853 separando bug↔win em
  field-reports reais, acima do null matched.
- **Fase 2 — produção, auditoria cega pré-registrada** (2026-07-15): após
  5 dias de sombra autônoma (0 ticks falhos), o top-10 ranqueado pelo dial
  continha **9/10 reports severos vs 7/10 da fila cronológica** (gate de
  margem +2 vencido no fio; rotulador cego distinto do selador; ata em
  `spine/RELATORIO-FASE2.md`).
- **Operação**: tick de rotina 0,04–0,09 s; caminho quente ~56,6 milhões
  de vezes mais barato que consultar um LLM por leitura.
- **Refutados e publicados** (honestidade com número): transmutação de
  atributos (Exp 5/6/9 — atributos são legíveis, não escrevíveis),
  previsão de risco de commit (Exp 14), dial feat↔fix para certificação
  (Exp 15, AUC 0,719 < gate 0,80).

## O método é o produto

Toda medição segue o rito: pré-registro selado (SHA-256 **antes** dos
dados), null matched empírico, leave-one-out, gates e regra de parada
escritos de antemão, aposta do agente registrada, refutação commitada com
o mesmo destaque da vitória. Régua sem laudo não existe: cada dial carrega
manifest com certificação, bula e governança.

## Constituição (advisory absoluto)

Mostradores **leem, nunca escrevem** — não decidem, não promovem, não
bloqueiam; riders no máximo `reverify`; nenhuma escrita fora de
`~/.m1nd/synt0ny/`. Fundação dupla e independente: a trilogia experimental
da synt0ny (atributos são direções legíveis, não operações de escrita) e a
constituição do m1nd ("a letter cannot color the map").

## Anatomia

```
dials/    réguas certificadas (axis.npz + manifest com laudo e bula)
spine/    a espinha: shadowd (watcher launchd, 6 frentes), panel (:1341),
          mcp (tool synt0ny_read), hooks, pré-registros e atas da Fase 2
lab/      experimentos 1–15: pré-registros selados, resultados, dados
docs/     PRD, UML, FRONTEIRA-M1ND (fila T0–T3 do conselho de 4 vozes)
```

## Uso

```
venv/bin/python3 synt0ny.py buscar <verbo>       # vizinhos por ressonância
venv/bin/python3 synt0ny.py intencao <verbo>...  # posição no eixo ⊖/⊕
venv/bin/python3 synt0ny.py eixo                 # extremos do eixo no banco
```

Requer Ollama local com `bge-m3`. Palavras fora do banco funcionam
(zero-shot). A espinha roda por launchd (`com.kle1nz.synt0ny-shadowd`,
tick 5 min, fail-quiet) e o painel de saúde vive em `127.0.0.1:1341`
(`com.kle1nz.synt0ny-panel`). Agentes leem o motor via MCP
(`synt0ny_read`) ou `POST /api/read`.

## Fronteira

T0 (espinha advisory em sombra sobre o exausto do m1nd) está provado.
T1–T3 — higiene de memória, recall de dois escores, vigia de delegação,
Reflex Foundry — estão desenhados em `docs/FRONTEIRA-M1ND.md`. Regra
reuse-first declarada: donors maduros (SetFit, bge-reranker, FastEmbed,
cleanlab, mecanismo de dedupe do mem0) entram em A/B selado contra o que
construímos; se o donor vencer com número, adota-se o donor.

## Limites conhecidos (honestidade de laboratório)

- O dial lê **tom, não verdade**: um flake de CI declarado entrou no
  top-10 da auditoria porque *soa* severo. Classe de FP caracterizada.
- Single encoder no caminho quente (rider `SINGLE_ENCODER` em toda
  leitura); a regra multi-instrumento vale para promover achado a
  "geometria da língua".
- Uma auditoria de produção vencida, no fio exato do gate. Confiança
  composta vem das janelas seguintes — o rito re-audita de graça.
- A purificação linear é agressiva: separa parônimos, mas mutila pares
  cuja semelhança legítima corre paralela à forma (flexões — Exp 6).
- O eixo da intenção separa polaridade; NÃO transmuta (refletir "amar"
  não produz "odiar" — Exp 5). Atributos são direções; identidades são
  regiões.
