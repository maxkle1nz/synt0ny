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
   nos antônimos + Exp 8). Calibrar apostas futuras para baixo.
5. Demos não são gates: indício vai para o caderno como indício.

## Problemas conhecidos
- A purificação OLS (k=50 trigramas) confisca variância compartilhada:
  neutraliza parônimos mas MUTILA parentes legítimos (flexões foram a rank
  ~238/250). Não usar o espaço purificado para vocabulário flexionado até a
  régua-por-par entrar.
- Eixo da intenção zero-shot: forte no polo ⊖, morno no ⊕ (medido na CLI).
- Escala: tudo validado em 227 verbos pt; substantivos/frases = extrapolação.
- Voz fugu (Sakana) indisponível via codex exec: MCP do DEXT3R morto derruba o
  startup (`~/.codex/config.toml:406`, porta 9200). Fix: comentar a entrada ou
  subir o serviço.

## Próximos passos (fila real, em ordem)
1. "Paradigma dos irmãos" (proposta fable, panel de 2026-07-10): 5 formas por
   verbo, transplante de tempo julgado entre irmãos (chance 25%), decoy
   morfológico interno (amaria vs amarei). Predições já esboçadas no panel.
2. Régua por par (proposta fable): regressão S_ij ~ T_ij, resíduo como
   similaridade purificada — substitui a purificação vetorial sem mutilar.
3. Exp 9 candidato: "dicionário vs diário" — frames de Fillmore mensuráveis
   (verbo ressoa com seus papéis típicos?) vs conhecimento episódico (ausente
   por construção).
4. Auto-refresh do PATHOS (padrão git-cliff): opcional aqui — repo sem CI;
   instalar se o repo ganhar cadência.

## Prompt do próximo agente
Leia este PATHOS e `README.md`; a verdade viva é `lab/` (pré-registros +
results). Toda mudança de estado/doutrina volta para cá na mesma sessão.
Commits em inglês, autoria Max Kle1nz. O método não se negocia: selar antes de
medir, declarar toda falha com número, e nunca dar um sim falso.
