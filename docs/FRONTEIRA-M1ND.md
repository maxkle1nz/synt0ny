# Fronteira sintonia × m1nd — síntese do conselho de 4 vozes
2026-07-11 · Vozes: fable (medium), fugu/Sakana (medium), gpt-5.6-sol (xhigh,
passada l00p), agente-orquestrador (proposta independente prévia). Todas
read-only, com evidência própria (arquivo:linha) nos dois repos.

## O fato de fundação (fable)
`m1nd-core/src/embed.rs` declara em comentário que o tier semântico atual é
model2vec estático ("NOT transformer-grade… the ONNX / bge transformer tier is
the path for maximal quality") e `embed_cache.rs` já invalida por
`model_id + dim`. O m1nd deixou a porta pronta; a sintonia é a chave.

## Convergências (por contagem de vozes)
1. DAEMON/TICK COMO PRIMEIRO HABITAT — 4/4. Reflexos advisory nos workflows
   automáticos: triagem de field-reports (fable), Reflex Router
   ingest_only/run_impact/alert_agent/escalate_llm (sol), Tick Spectrometer
   com réguas POR PROJETO — overclaim↔evidence, public↔internal, bug↔friction,
   stale↔fresh, risky↔cosmetic (fugu). Entrada: auto_ingest.rs +
   daemon_handlers.rs (antes de daemon_proactive_insights_for_file).
   Meta (sol): −50-80% escaladas a LLM com ≥95% recall dos perigosos.
2. HIGIENE DA MEDULLA — 4/4 em variantes complementares: stance_mismatch
   (postura epistêmica do texto vs confidence declarada — fable, entrada
   tools.rs handle_learn + promote_handlers.rs), Hygiene Gauge
   (private↔doctrine, evidence↔vibe — fugu; ataca risco documentado em
   docs/uml/medulla.md:251), Memory De-Echo no north/delegate (dedupe por
   cluster com representante, contradição SÓ por campos estruturados,
   corroboradores preservados — sol, entrada recall_memory_slice;
   20-35% menos tokens de memória por pacote), dedupe na promoção (agente).
3. SEEK DOIS-ESCORES + FIRMAMENTO — 3/4. Score bruto + score purificado por
   candidato; demoção apenas quando a margem residual cai no null E é
   explicada por forma; concordância entre encoders como boost; NUNCA
   substituir o ranking (mutilação de flexões provada). Restrito a nós de
   memória/claims — código mantém o canal de forma (identificadores são
   semânticos às vezes). Entrada: Embedder trait (embed.rs:38) +
   search_handlers/layer_handlers rerank. Gate: battery + harness R17.
4. LOOP DE DELEGAÇÃO — 2/4, complementares que fecham o ciclo: Scope
   Resonator PRÉ (packet projetado contra eixos aprendidos dos outcomes do
   debrief — fugu; métricas já definidas em docs/uml/delegation.md:224) +
   guarda de ressonância PÓS packet-vs-debrief (fable; teria pego o
   incidente #331, o runner que vagou até o timeout).

## Wildcards em escada (compõem um sistema imunológico)
- Guarda de deriva delegate/debrief (fable) — detector de filho-fora-da-missão.
- Null Oracle for Agent Echo (fugu) — claim só vira high confidence se
  ressoar com a própria evidência acima do p95 de null matched de vizinhos
  plausíveis; senão `semantic_evidence: weak/null_like` no trust_envelope.
- Reflex Foundry (sol) — a cada ≥30 outcomes rotulados (learn/debrief/
  field-reports), job periódico monta 12 exemplares balanceados, SELA uma
  régua nova, roda LOO + null + holdout temporal; só aprovadas viram
  artefatos consumíveis pelo daemon. O protocolo científico da sintonia
  como fábrica automática de reflexos.
- Placar do apostador como serviço (agente) — perfil de calibração por
  agente (lê-bem/escreve-mal) vivendo na medulla, herdado entre sessões.

## ARMADILHA UNÂNIME (4/4 — lei da integração)
O mostrador NUNCA escreve, decide, promove ou concede act. Sempre advisory,
riders capados em reverify, gates existentes intocados. Dupla fundação
independente: a trilogia experimental da sintonia (atributos legíveis, não
escrevíveis) e a constituição do m1nd ("a letter cannot color the map").
E (fugu): portar o MÉTODO (embeddings locais + firmamento + 12-exemplos +
LOO/null + cache por hash + advisory), NUNCA transplantar o artefato pt-BR
(v_int/valência) como semântica universal — re-selar réguas por domínio e
idioma (reports são majoritariamente em inglês).

## Fila executável (T0 → T3)
T0 (horas, sidecar Python, zero Rust): Tick Spectrometer MVP advisory com
   2-3 réguas re-seladas em inglês + auditor offline da medulla (relatório).
T1 (2-3 dias): stance_mismatch no memorize/promote (com bloco adversarial
   pré-registrado: claims tersos-mas-verificados) + De-Echo advisory no
   north/delegate.
T2 (3-5 dias, Rust): Embedder bge-m3+firmamento para memória (a vaga do
   embed.rs) + seek dois-escores, gates de battery obrigatórios.
T3 (fronteira): Scope Resonator + guarda de deriva (loop de delegação) →
   Null Oracle no mission_verify → Reflex Foundry.
Cada item entra pelo rito da casa: pré-registro selado, null empírico,
verdict de oráculo nos BIG, e réguas com laudo próprio (calibrate_envelope).
