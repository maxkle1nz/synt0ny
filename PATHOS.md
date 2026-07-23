# PATHOS — synt0ny

## Incidente 18-23/07: a espinha ficou muda 3 dias — achado e consertado (2026-07-23)
Três causas COMPOSTAS, descobertas na pergunta "que ponto estamos":
(1) o daemon do m1nd clona o MESMO alert com metadados mutantes
(daemon_alerts.json: 500 itens, 1 texto único) → nosso dedupe por hash
do item inteiro + corte sorted()[-500:] (LEXICOGRÁFICO, não temporal)
vazou → 283.547 envelopes duplicados em 18-20/07; (2) reboots do Mac em
20/07 → (3) os 3 launchd jobs estavam bootstrapped ad-hoc (plists NUNCA
instalados em ~/Library/LaunchAgents) E marcados disabled no gui/502 —
nada voltou; silêncio total 20-23/07. Consertos, todos provados:
dedupe do json_array agora por TEXTO extraído + seen em ordem de
inserção FIFO (idem github); shadow.jsonl deduplicado 284.180→823
(backup shadow.jsonl.bak-20260723.gz); seen seedado antes da religa;
plists instalados + enabled + bootstrapped; tick de retomada colheu o
backlog dos 3 dias (191 eventos, 1015 envelopes, painel UP, exit 0);
bug do daemon reportado em field-reports.jsonl E colhido pela própria
espinha no mesmo tick. Lições de arquitetura: watcher de fonte que
REESCREVE arquivo deduplica por conteúdo semântico, nunca por item;
sorted()[-N:] em seen-set é bug de vazamento; serviço só existe se o
plist mora em ~/Library/LaunchAgents E está enabled. PENDÊNCIAS: selar
janela 2 de auditoria (marco novo — o card "fase 2" do painel ainda
conta do selo velho de 10/07); decisão dos alerts anotados (T0.1
pleno); T1 da fronteira.

## Estratégia pós-F2 ratificada com o Max (2026-07-20)
Sessão de leitura fria do que a F2 significa. Três camadas fixadas:
(1) PROVADO = o instrumento sobre dados do m1nd (T0 conquistado);
(2) NÃO provado = o m1nd consumindo a leitura em fluxo real + efeito a
jusante (contrafactual tipo A/B do packet frio) — é o T1;
(3) lei do porte = método sim, artefato nunca (réguas re-seladas por
domínio/idioma). Pergunta do dono "estamos reinventando a roda?"
respondida com mapa de donors: componentes JÁ são rodas prontas
(bge-m3, cosseno, sklearn); original fino = firmamento + rito de
certificação + constituição advisory. Donors declarados para a fila:
SetFit (upgrade de cabeça das réguas), bge-reranker + FastEmbed/ONNX
(T2 — A/B SELADO donor-vs-dois-escores ANTES de construir; se o donor
vencer, adota-se), mecanismo de dedupe do mem0 (ler antes de escrever
o De-Echo), cleanlab (qualidade de rótulos do Foundry). Alternativa
LLM-API (~centavos/mês) nomeada e rejeitada pelos motivos do dono:
privacidade dos paths locais, 24/7 sem rede, custo marginal zero.
README reescrito do dia-1 para o estado real (espinha + F2 + método).

## A espinha SAIU DA SOMBRA — Fase 2 auditada e APROVADA (2026-07-15)
Janela aberta pelo relógio de eventos na leitura estrita (36/30 únicos,
5,0 dias, 0 ticks falhos). Amostra cega de 26 itens re-selada por rito
(sha do mapping commitado ANTES da rotulagem); rotulador = agente CEGO
distinto do selador (Opus, zero contexto/tools), como o selo previa.
**G-F2a PASSOU no fio exato: top-10 ranqueado 9/10 severos vs fila
cronológica 7/10 (gate: >= +2; random exploratório 8/10).** Honestidade:
taxa-base severa altíssima no período (21/26) comprimiu a margem; o
único benigno do top-10 é o flake de CI — a classe de FP conhecida (o
dial lê tom, não verdade). G-F2b passou com evidência (0 crash-loop;
no-op 0,04-0,09 s; escritas só em ~/.m1nd/synt0ny/). Decisão selada
aplicada: **T0.1** — painel desvela scores por default (véu era do
rotulador; provado no browser). Ata completa: spine/RELATORIO-FASE2.md
+ f2_mapping.json + f2_rotulos.json. Aposta do agente: direção certa,
magnitude errada dos dois lados (subestimou a taxa-base severa).
PENDENTE com o Max: desenho dos "alerts anotados" do T0.1 (nunca em
arquivo do m1nd — advisory absoluto; candidato: arquivo próprio em
~/.m1nd/synt0ny/ consumido via MCP/painel). Observação pós-auditoria:
stream daemon-alerts infla (500 envelopes; alerts re-emitidos mutam
hash e recontam) — candidato a dedupe semântico, fora da janela selada.

## A régua pegou o próprio painel (2026-07-13)
Aos 2,6 dias de sombra o painel declarou "JANELA ABERTA" (46/30) — mas
contava ENVELOPES; o selo conta EVENTOS (23 únicos: o v1.1 dobrou envelopes
por evento ao somar o 2º dial). Overclaim de instrumento, pego pela leitura
estrita do selo e corrigido no dia: paneld conta sha únicos (23/30, fechada);
adendo ex-ante sela as interpretações ANTES de qualquer rotulagem
(spine/PREREGISTRO-FASE2-ADENDO.md, sha a930e814…); amostra-ensaio descartada
sem rotulagem. G-F2b endurecido de verdade: no-op era 1,3 s (import numpy +
sonda GitHub a CADA tick) → lazy import + throttle 30 min = 0,04-0,09 s.
Janela real: 30 eventos únicos OU 2026-07-17T21:50. Operação do período:
63+ ticks com colheita, 0 falhas, daemon-alerts acordou (71), github 185.

## O circuito (produto fechado em 2026-07-11)
medir→servir→consumir ligado: `POST /api/read` no paneld (espectro com cache
compartilhado + projeção nos dials + envelope v0; testado pt/en, ~80 ms);
biblioteca `dials/` v1.1 com bandas de referência e a régua de PRODUÇÃO
exportada (valencia_pt, laudo Exp 5/10/12) ao lado da bug_win_en; MCP server
`spine/mcp/synt0ny_mcp.py` com a tool `synt0ny_read` REGISTRADO user-scope no
Claude Code (todo agente da máquina enxerga o motor); hook UserPromptSubmit
pronto e testado (`spine/hooks/prompt-read.py`, fail-silent 1 s) — registro
no settings global reservado à MÃO HUMANA (classificador bloqueia agente
instalando hook em si mesmo; a casa concorda).

## As frentes da sombra (v1.2, 2026-07-11)
6 fontes em streams isolados (F2 blindada aos originais, verificado): field-
reports + inbox (a janela da auditoria), bridge (correio pt entre agentes,
valencia_pt + DOMAIN_SHIFT), daemon_alerts (armada, vazia), e GITHUB — o giro
do perfil inteiro por-repo via gh api (a events API censura payloads
privados; colheita = repos/{x}/commits com dedupe por SHA): 136 commits de 7
repos no 1º tick, com meta repo/sha e o rider anti-Exp14 (tom agregável,
NUNCA risco). Painel ganhou cards de portfólio e streams. Fora por decisão:
transcripts (a porta é o hook UserPromptSubmit, aguardando colagem humana no
settings) e previsão de risco de commits (refutada). Exp 15 (feat↔fix vs
prefixos conventional): AUC 0,719 > null 0,638 mas < gate 0,80 — REFUTADA
para certificação, sinal reconhecido, G2 de ranking passou (65%); re-selagem
= exemplos derivados do domínio (o estilo poético dos commits do m1nd vence
léxico genérico).

## A espinha (T0 — VIVO desde 2026-07-11)
O shadowd respira dentro do m1nd: launchd com.kle1nz.synt0ny-shadowd (tick
5 min), dial certificado bug_win_en v1.0.0 a bordo (laudo Exp 13 no manifest),
envelopes v0 com governança no wire em ~/.m1nd/synt0ny/shadow.jsonl. ADVISORY
absoluto: nunca escreve em arquivo do m1nd. Honesty refutada fica FORA até
re-selagem. Fase 2 (auditoria cega ranqueada-vs-cronológica, gate de margem
+2) SELADA no dia da instalação — janela: >= 7 dias ou >= 30 eventos novos
(spine/PREREGISTRO-FASE2.md). Admin panel local no login:
com.kle1nz.synt0ny-panel serve 127.0.0.1:1341 (spine/panel/) — saúde do
Ollama, pulso do shadowd, dials, progresso da janela, histograma agregado;
scores individuais VELADOS por default (proteção do rotulador cego da F2). Exp 13 provou: inglês é a 2ª língua com número
(AUC 0,853) e a economia da espinha é 56,6M× no caminho quente.

## Norte
Laboratório de geometria semântica em pt-BR: medir a estrutura real do
significado em embeddings locais (Ollama) com protocolo de pré-registro — e
consolidar o que sobrevive aos gates em ferramenta executável (`synt0ny.py`).
Nasceu de uma conversa (2026-07-10, "das matrizes ao vocabulário de modos");
o método é o produto tanto quanto os resultados.

## Estado real (2026-07-10, fim da primeira sessão)
- Exp 1-8 completos, todos pré-registrados e hasheados ANTES dos dados
  (`lab/PREREGISTRO*.md`, `lab/results*.json`).
- Âncoras medidas: 31,4% do espectro bge-m3 é forma ortográfica (separável por
  regressão); eixo da intenção 12/12 no leave-one-out e alinhado ao PC1 do
  espaço (fração 0,41 vs null p95 0,36); eixo do tempo real porém profundo
  (PC88), ortogonal à intenção (cos −0,01); antônimos afinam pelo corpo
  (domínio compartilhado, ~90% da massa) e dissonam ~10% pelo eixo; espectro
  ~lei de potência (expoente 0,60, R² 0,94); PC1 interpretável sem supervisão
  (abstrato ↔ concreto).
- Refutados: transmutação linear entre corpos distintos (espelhar amar ≠
  odiar); "uma frequência por palavra" (PCA-1: 0% de recuperação); dissonância
  física de antônimos.
- Exp 9 (paradigma dos irmãos, desenho fable + verdict fugu CHANGE aplicado):
  transmutação FALHOU até com corpo idêntico (ida 4/12, volta 3/12 vs gate 9;
  supletivos 0/4 → o sinal fraco que existe é geometria de sufixo). Mas o
  vetor-tempo carrega sinal real (7/24 vs null p95 = 3). CONCLUSÃO DA TRILOGIA
  (Exp 5, 6, 9): neste espaço, atributos são LEGÍVEIS (projeção classifica
  12/12) mas não ESCREVÍVEIS (aritmética vetorial não edita palavras) — painel
  de MOSTRADORES, não de botões. Observação qualitativa não-gate: futuro −
  v_tempo caiu 6/12 vezes no condicional (futuro do pretérito) — erro
  sistemático gramaticalmente coerente; hipótese para investigação futura.
- Ferramenta `synt0ny.py` funcionando (buscar/intencao/eixo, zero-shot);
  caderno publicado como artifact (`caderno.html`).

## Doutrina de operação (o que fez esta casa funcionar)
1. Pré-registro selado com SHA-256 ANTES de qualquer dado; gates numéricos;
   interpretação selada junto. Regra de parada por experimento — sem métrica
   nova depois de ver números.
2. Controles adversariais sempre: parônimos (forma), null matched (500
   direções de pares aleatórios), leave-one-out, espaço primário declarado +
   controle de atribuição (centrado vs purificado).
3. askGOD no DESENHO dos gates — a única rodada sem oráculo (Exp 6) saiu com
   gate-teto invencível. Lição medida, não opinião.
4. Apostas do agente registradas por experimento. Viés conhecido e reincidente:
   acerta a EXISTÊNCIA de eixos, superestima magnitudes e saltos (4 derrotas
   nos antônimos + Exp 8). No Exp 9 a calibração "para baixo" AINDA superestimou
   (apostou 8-7-3-1, veio 4-3-2-0): calibrar operações de ESCRITA perto do null,
   não perto da vontade.
5. Verdict cross-vendor antes do selo endurece o teste: o CHANGE do fugu no
   Exp 9 (null empírico de 300 direções, falsificador supletivo, margem por
   item) foi o que permitiu separar "sinal real fraco" de "transmutação" — sem
   ele, 7/24 contra um v_rand único teria dado leitura confusa.
5. Demos não são gates: indício vai para o caderno como indício.

## Problemas conhecidos
- A purificação OLS (k=50 trigramas) confisca variância compartilhada:
  neutraliza parônimos mas MUTILA parentes legítimos (flexões foram a rank
  ~238/250). Não usar o espaço purificado para vocabulário flexionado até a
  régua-por-par entrar.
- Eixo da intenção zero-shot: forte no polo ⊖, morno no ⊕ (medido na CLI).
- Escala: tudo validado em 227 verbos pt; substantivos/frases = extrapolação.
- Voz fugu (Sakana): o MCP do DEXT3R morto (`~/.codex/config.toml:406`, porta
  9200) derruba o startup — FIX PROVADO (Exp 9): `codex exec -c
  'mcp_servers={}'` anula sem tocar no config; WAF exige VPN ligada.

- Exp 10 (a ponte, verdict fugu CHANGE aplicado): o eixo da intenção TRANSFERE
  para frases — 100% em 52 frases (AUC 1.0; null matched p95 80,8%), 14/14 em
  vocabulário nunca visto. ESPECTRÔMETRO VIÁVEL. Batismo do mostrador adiado:
  bloco adversarial 3/8 (o eixo mistura valência do evento com tipo lexical do
  verbo — contexto forte vence o verbo, contexto sutil perde). Limites
  declarados: dataset autoral (não é produção); discrepância 12-vs-14 no
  tamanho do estrato far entre texto do prereg e lista selada (lista prevalece;
  resultado inalterado).

## Próximos passos (fila real, em ordem)
0. [EXECUTADO 2026-07-10] Exp 11 "o atlas" — 83.917 lemas × 2 encoders
   (A bge-m3/M4, B qwen3-embedding:8b/GENESIS RX 7900), panel duplo no
   desenho (fable + fugu, ambos CHANGE aplicados). PLACAR:
   · E1 gate (v12 >= 0,75): FALHOU em A (0,685) e B (0,678) → "não
     estabelecido". DESCOBERTA REPLICADA: eixo v_tep (12 relações held-out
     do padrão-ouro) fez 0,791/0,799 — cruza o limiar NOS DOIS. O eixo
     autoral está aposentado; v_tep é o herdeiro (exige pré-registro novo).
   · E3 (Q × polissemia): sinais OPOSTOS entre encoders (+0,064 A /
     −0,087 B) → ARTEFATO DE INSTRUMENTO, não geometria da língua. A
     "refutação limpa" do interim (só A) estava ERRADA — o multi-instrumento
     corrigiu o próprio laboratório em tempo real.
   · E2: replicou raspando nos dois (0,312/0,377 vs p95); expoentes
     0,67/0,83. Osgood CAIU nos dois: modos de topo do léxico cru =
     registro/morfologia/enciclopédia ("des-", nomes próprios, jargão).
     O dicionário cru tem geometria EDITORIAL.
   · Concordância inter-encoder: Q 0,21 (baixa!) · proj(v12) 0,52 — os
     encoders são menos redundantes que o risco fable temia; onde concordam,
     vale mais.
   Trilhas futuras bancada B (registradas): SAEs sobre espectros,
   observatório noturno, qwen3:32b rotulador auxiliar validado por amostra.
0b. Exp 12 candidato: o atlas FILTRADO (vocabulário comum, 1 palavra, fr>0)
   + régua-por-par + v_tep como eixo primário — reperguntar Osgood e E1
   na parte da língua que não é editorial.
1. [EXECUTADO 2026-07-11] Exp 12 "a rua": espectrômetro validado em PRODUÇÃO
   — 500 reviews reais (B2W, ground truth = estrelas dos clientes): 93,2%
   zero-shot, AUC 0,979 (gate 80%, null matched p95 81,2%). Os 34 erros são
   a bula prevista: ironia, mistas (produto 5★/entrega péssima), notas sem
   valência. VEREDITO DE UTILIDADE: triagem de valência pt local/grátis/
   determinística é caso de uso REAL comprovado. Ressalvas declaradas:
   estratos subestimados por mediana local; bugfix de broadcasting pós-selo
   (sem mudança de métrica).
2. Sonda de batismo maior: ~24 adversariais para nomear o mostrador
   (valência do evento vs tipo lexical) com poder estatístico.
3. Régua por par (proposta fable): regressão S_ij ~ T_ij, resíduo como
   similaridade purificada — substitui a purificação vetorial sem mutilar.
4. "Dicionário vs diário" — frames de Fillmore mensuráveis (verbo ressoa com
   seus papéis típicos?) vs conhecimento episódico (ausente por construção).
5. Hipótese nova do Exp 9 (não-gate): futuro − v_tempo → condicional (futuro
   do pretérito) — o erro sistemático merece teste próprio.
6. Auto-refresh do PATHOS (padrão git-cliff): opcional aqui — repo sem CI;
   instalar se o repo ganhar cadência.

## Documentos canônicos
`docs/PRD.md` (visão, requisitos, métricas, riscos, roadmap, governança) e
`docs/UML.md` (componentes, sequências, ciclo de vida de régua) — autoria
assento Fable, 2026-07-11, baselined nos Exp 1-12 + conselho de 4 vozes
(`docs/FRONTEIRA-M1ND.md`). Mudança de arquitetura/escopo atualiza PRD/UML
no mesmo burst (doc-gate).

## Prompt do próximo agente
Leia este PATHOS e `README.md`; a verdade viva é `lab/` (pré-registros +
results). Toda mudança de estado/doutrina volta para cá na mesma sessão.
Commits em inglês, autoria Max Kle1nz. O método não se negocia: selar antes de
medir, declarar toda falha com número, e nunca dar um sim falso.
