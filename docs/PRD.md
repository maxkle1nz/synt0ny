# PRD — sintonia: motor local de discernimento (advisory)
Nome externo qualificado por review (2026-07-11): "instrumentação semântica
local" / "semantic instrumentation engine" — o qualificador é parte do nome
para o nome não induzir o overclaiming que o produto combate.
2026-07-11 · Autoria: assento Fable (main da sessão fundadora) · Fundamento:
12 experimentos pré-registrados (lab/), validação de rua (Exp 12), conselho
de 4 vozes (docs/FRONTEIRA-M1ND.md). Verdade viva operacional: PATHOS.md.

## 1. Visão
Um instrumento de medição para significado: transforma qualquer texto em
posições sobre réguas calibradas — localmente, em microssegundos, de forma
determinística — e conhece a própria margem de erro. É o sistema nervoso
periférico que agentes LLM não têm: percepção barata e contínua que filtra o
mundo antes do pensamento caro. Lê; não escreve, não gera, não decide.

## 2. Problema
Agentes LLM são córtex puro: todo micro-julgamento ("é duplicado?", "é
urgente?", "é do mesmo assunto?") custa uma inferência completa. Consequências
medidas nesta casa: atenção limitada por orçamento (vigilância contínua é
inviável), memória que cresce sem higiene (duplicação silenciosa), confiança
autodeclarada sem auditoria (overclaiming), retrieval contaminado por forma
ortográfica (31,4% do espectro de uma palavra é grafia — Exp 4), e deriva
entre sessões sem referencial externo. Alternativas existentes: APIs de LLM
(caras por chamada, não-determinísticas, dados saem da máquina) ou heurísticas
de substring (frágeis — risco literal documentado no m1nd, medulla.md:251).

## 3. Usuários
- U1 · Agentes LLM (primário): consomem leituras advisory em loops quentes —
  triagem, dedupe, roteamento, auto-verificação anti-eco.
- U2 · Sistemas agênticos (m1nd como primeiro cliente): reflexos embutidos em
  workflows automáticos (daemon/ticks, promoção de memória, delegação).
- U3 · O operador humano (Max): CLI para consultas diretas; laudos e placares
  para auditoria; réguas sob medida por 12 exemplos.

## 4. O que é (componentes) / O que NÃO é
É: (a) ESPECTRÔMETRO — embeddings locais determinísticos (Ollama; bge-m3
como encoder A validado) com cache por hash; (b) FIRMAMENTO — separação da
camada ortográfica (regressão k=50 sobre trigramas), aplicável a texto
natural, NUNCA a vocabulário flexionado/identificadores (mutilação provada,
Exp 6/9); (c) RÉGUAS — eixos semânticos extraídos de 12 exemplos rotulados,
cada um com laudo próprio (LOO + null empírico + sensibilidades) e ciclo de
vida versionado (o eixo autoral v12 foi aposentado pelo herdeiro v_tep do
padrão-ouro — Exp 11); (d) RESSONÂNCIA — busca/dedupe por produto interno,
1 consulta × N candidatos = 1 matmul (µs); (e) O RITO — pré-registro selado,
controles adversariais, verdict de oráculo nos BIG, regra de parada: o
protocolo é parte do produto (nenhuma régua entra sem laudo).
NÃO é: gerador (não escreve texto); editor de conceitos (transmutação
refutada 3×: atributos são legíveis, não escrevíveis); juiz (nunca decide,
promove, bloqueia ou concede act — advisory sempre); detector de verdade ou
contradição (antônimos AFINAM ~90% pelo corpo — Exp 7; contradição só por
campos estruturados); semântica universal (réguas valem por idioma+domínio
selados; re-selar ao portar).

## 5. Requisitos
Funcionais: RF1 espectro determinístico com cache por content-hash+encoder;
RF2 régua nova a partir de 12 exemplos com laudo automático (LOO, null-300,
sensibilidades) — sem laudo, sem painel; RF3 leitura multi-régua de um texto
em 1 chamada (perfil de mostradores + percentis); RF4 busca/dedupe por
ressonância com dois escores (bruto + purificado) onde o firmamento se
aplica; RF5 modo advisory-only: toda saída é score+rider, nunca ação; RF6
CLI (existente: sintonia.py buscar/intencao/eixo) e biblioteca importável;
RF7 replay offline sobre históricos (jsonl/csv) para calibração e auditoria;
RF8 versionamento de réguas (axis_id + versão + hash do laudo).
RF9 purification_policy explícita por leitura (disabled | natural_language |
explicit; limiares de densidade de identificadores; mixed_content → ABSTAIN)
— saída declara status e razão da abstenção: o mostrador não inventa onde
não vale; RF10 measurement envelope com governança no wire format
(axis_id+versão, score, percentil, riders CODIFICADOS com severidade,
allowed_actions/forbidden_actions, max_effect) — v0 mínimo no T0, v1 com
proveniência completa (input_hash, weights_hash, report_hash,
in_distribution) no T2.
Não-funcionais: RNF1 100% local (nenhum byte sai das máquinas do operador);
RNF2 saída REPRODUZÍVEL por perfil de execução selado (texto, encoder,
pesos/quantização, runtime, classe de hardware) com tolerância numérica
declarada; bit-a-bit somente onde certificado por perfil — medido: Δ=0,0
intra-perfil (M4/bge-m3); igualdade ENTRE perfis (Metal vs ROCm) nunca
testada e não prometida; RNF3 SLOs de latência SEPARADOS: cache-hit p95,
cache-miss p95, projeção (1/10/100 réguas), ressonância em lote
(1k/100k/1M), cold-start do sidecar e IPC Rust↔sidecar — o custo sistêmico
(spawn, socket, contenção no Ollama) é medido como cidadão de 1ª classe, não
só o matmul; RNF4 zero custo marginal por consulta; RNF5 honestidade
estrutural: limites publicados na bula de cada régua.

## 6. Métricas de sucesso
Já medidas (baseline): valência em produção 93,2%/AUC 0,979 (500 reviews
reais, zero-shot — Exp 12); eixo 12/12 LOO trans-domínio (Exp 5); v_tep
0,791/0,799 replicado em 2 encoders (Exp 11); busca 6.012× mais rápida que
varredura serial (Exp 1); ponte verbo→frase 100%, 14/14 em vocabulário
virgem (Exp 10). Alvo da integração (conselho, FRONTEIRA-M1ND.md): −50-80%
escaladas a LLM na triagem com recall ≥95% dos críticos; −20-35% tokens de
memória por pacote north/delegate; junk-rate do seek −30% sem substituir
ranking; overhead de tick < 5 ms.

## 7. Riscos e bula (públicos, por construção)
R1 ironia/mistas/sem-valência erram (34/500 na rua — casos onde humanos
divergem); R2 dependência de encoder em sinais finos (E3 inverteu de sinal
entre encoders — Exp 11): resultado fino exige 2 encoders antes de virar
afirmação; R3 firmamento mutila parentes legítimos (nunca em flexões/
código); R4 régua transplantada entre idiomas/domínios sem re-selo é
inválida; R5 anisotropia editorial em léxicos crus (modos de dicionário ≠
modos da língua — Exp 11); R6 o risco terminal: alguém promover mostrador a
botão — mitigação: a lei unânime do conselho gravada em governança.

## 8. Roadmap
Agora: Exp 13 "a espinha, fase 1" — replay dos 97 field-reports do m1nd
(réguas re-seladas em inglês; gates G1 classe, G2 precision@10 honesty, G3
custo reflexo-vs-LLM). T0 (horas): Tick Spectrometer sidecar advisory no
daemon + auditor offline da medulla. T1 (2-3 d): stance_mismatch no
memorize/promote + Memory De-Echo no north/delegate. T2 (3-5 d): Embedder
bge-m3+firmamento no seam do m1nd (embed.rs) + seek dois-escores com gate de
battery/R17. T3 (fronteira): Scope Resonator + guarda de deriva; Null
Oracle no mission_verify; Reflex Foundry (réguas auto-seladas de outcomes).
Trilhas de pesquisa abertas: atlas filtrado/Osgood (Exp 13+), sonda de
batismo do mostrador de valência, léxico multi-idioma.

## 9. Governança (a lei)
1. O mostrador nunca escreve, decide, promove ou bloqueia — advisory, riders
   capados em reverify. Fundamento duplo e independente: trilogia
   experimental da sintonia + constituição do m1nd ("a letter cannot color
   the map"). 2. Régua sem laudo não existe. 3. Mudança BIG passa por
   verdict de oráculo antes do selo. 4. Falha é publicada com número — a
   bula é interface, não apêndice.
