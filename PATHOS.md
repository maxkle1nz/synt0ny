# PATHOS — sintonia

## Norte
Laboratório de geometria semântica em pt-BR: medir a estrutura real do
significado em embeddings locais (Ollama) com protocolo de pré-registro — e
consolidar o que sobrevive aos gates em ferramenta executável (`sintonia.py`).
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
- Ferramenta `sintonia.py` funcionando (buscar/intencao/eixo, zero-shot);
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
1. Validação do espectrômetro em DADOS REAIS (reviews/commits/tickets de
   verdade — o 100% é de frases autorais limpas; produção tem ruído).
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

## Prompt do próximo agente
Leia este PATHOS e `README.md`; a verdade viva é `lab/` (pré-registros +
results). Toda mudança de estado/doutrina volta para cá na mesma sessão.
Commits em inglês, autoria Max Kle1nz. O método não se negocia: selar antes de
medir, declarar toda falha com número, e nunca dar um sim falso.
