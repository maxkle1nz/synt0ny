# UML — synt0ny e subsistemas
2026-07-11 · Autoria: assento Fable · Par do docs/PRD.md. Diagramas em
mermaid (renderizam no GitHub). Fonte de verdade do estado: PATHOS.md.

## 1. Componentes — o motor e a fronteira m1nd

```mermaid
flowchart TB
    subgraph SINTONIA["synt0ny — motor local de discernimento"]
        ENC["Espectrômetro\nOllama bge-m3 (A) · qwen3-8b (B)\ndeterminístico, local"]
        CACHE[("Cache de espectros\ncontent-hash + encoder + versão\n*.npz / *.bin")]
        FIRM["Firmamento\nremove camada ortográfica (k=50)\nNUNCA em flexões/código"]
        DIALS["Réguas (dials/)\n12 exemplos → eixo + LAUDO\nLOO · null-300 · sensibilidades\nversionadas (v12 aposentado → v_tep)"]
        RES["Ressonância\n1 consulta × N = 1 matmul (µs)\ndois escores: bruto + purificado"]
        RITO["O Rito (governança)\npré-registro selado · oráculos\nregra de parada · bula pública"]
    end
    TXT["texto\n(review, claim, diff, report)"] --> ENC
    ENC --> CACHE
    CACHE --> FIRM
    FIRM --> DIALS
    FIRM --> RES
    DIALS --> OUT["leituras ADVISORY\nscores + percentis + riders\n(nunca ação)"]
    RES --> OUT
    RITO -.->|"nenhuma régua sem laudo"| DIALS
    subgraph CONSUMERS["consumidores"]
        CLI["synt0ny.py CLI\nbuscar · intencao · eixo"]
        M1ND["m1nd (T0→T3)\ntick sidecar · medulla hygiene\nseek two-score · delegação"]
        AG["agentes LLM\ntriagem · dedupe · anti-eco"]
    end
    OUT --> CLI
    OUT --> M1ND
    OUT --> AG
```

## 2. Sequência — leitura de um texto (o caminho quente)

```mermaid
sequenceDiagram
    participant C as Consumidor (agente/CLI/m1nd)
    participant S as synt0ny
    participant K as Cache
    participant O as Ollama (local)
    C->>S: ler(texto, [réguas])
    S->>K: espectro(hash(texto, encoder))?
    alt cache hit (caso comum)
        K-->>S: espectro (0 ms)
    else miss
        S->>O: embed(texto)
        O-->>S: espectro (~10 ms, única vez)
        S->>K: grava
    end
    S->>S: firmamento (se aplicável ao domínio)
    S->>S: projeções = espectro @ eixos (µs)
    S-->>C: {régua: score, percentil, rider}*
    Note over C: decide o CONSUMIDOR.<br/>O mostrador nunca age.
```

## 3. Sequência — Tick Spectrometer no daemon do m1nd (T0)

```mermaid
sequenceDiagram
    participant D as m1nd daemon (tick)
    participant SC as sidecar synt0ny
    participant K as spectra cache (.m1nd/)
    participant A as fila de alerts
    participant LLM as agente/LLM (caro)
    D->>SC: evento (diff, doc, field-report)
    SC->>K: espectro cacheado? (miss → embed 1×)
    SC->>SC: réguas por projeto: risky↔cosmetic,\noverclaim↔evidence, bug↔friction (µs)
    SC-->>A: alert + scores (ADVISORY, rider reverify)
    alt maioria: rotina
        A->>A: arquivado/roteado no reflexo\n(sem LLM: −50-80% escaladas)
    else ambíguo/perigoso
        A->>LLM: sobe com contexto priorizado\n(recall crítico ≥95%)
    end
```

## 4. Estados — ciclo de vida de uma régua

```mermaid
stateDiagram-v2
    [*] --> Proposta: 12 exemplos rotulados\n(humano ou Reflex Foundry)
    Proposta --> Selada: pré-registro + SHA-256\nANTES de qualquer dado
    Selada --> Calibrada: laudo passa\n(LOO · null-300 · sensibilidades)
    Selada --> Refutada: laudo falha\n(registrada, nunca apagada)
    Calibrada --> EmObservação: shadow mode\n(pontua, não é exibida)
    EmObservação --> EmPainel: auditoria da sombra passa\n(precision em dados reais)
    EmPainel --> Suspensa: drift, troca de encoder\nou degradação em replay
    Suspensa --> Recalibrada: re-selo obrigatório\n(continua auditável, não lê)
    EmPainel --> Recalibrada: idioma/domínio novo\n→ re-selo obrigatório
    EmPainel --> Aposentada: herdeiro melhor replicado\n(ex.: v12 → v_tep, Exp 11)
    Refutada --> [*]
    Aposentada --> [*]: permanece auditável\n(hash + laudo no lab/)
```

## 5. Notas de fronteira (amarras aos fatos)
- O seam do m1nd é real: trait `Embedder` em `m1nd-core/src/embed.rs:39`,
  cache com invalidação por `model_id+dim` em `embed_cache.rs` — o comentário
  do próprio arquivo pede o tier transformer que o espectrômetro fornece.
- Pontos de entrada T0-T3 com arquivo:linha: docs/FRONTEIRA-M1ND.md.
- Todo diagrama acima descreve comportamento MEDIDO ou selado em pré-registro;
  o que é meta futura está marcado com os tiers do roadmap (PRD §8).
