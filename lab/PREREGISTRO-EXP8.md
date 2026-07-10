# Pré-registro — Experimento 8 ("o vocabulário de modos")
Data: 2026-07-10, ANTES de qualquer PCA. Proposta da 3ª voz (agente), inspirada
na observação do usuário sobre form constants / vocabulário geométrico universal.

## Hipótese
Se form constants são os modos próprios (eigenmodes) do córtex (Bressloff-Cowan)
e as representações neurais têm espectro fractal/lei-de-potência (Stringer 2019),
então: (a) os eixos que descobrimos com esforço — intenção (12 antônimos) e tempo
(12 flexões) — devem ser MODOS NATURAIS do espaço semântico (alinhados aos
componentes principais de topo), não direções arbitrárias; (b) os próprios
componentes principais do espaço devem ser interpretáveis, como form constants são
modos interpretáveis do córtex; (c) o espectro de autovalores deve tender a uma
lei de potência.

## Método (congelado)
- Espaço: purificado do Exp 4/6 (bge-m3, forma removida k=50), banco 251 itens
  (227 base + 24 flexões do Exp 6).
- v_intenção = média L2 de e(pos)−e(neg) sobre 12 antônimos; v_tempo = média L2
  de e(futuro)−e(passado) sobre 12 flexões.
- BASE PCA INDEPENDENTE (anti-circularidade): SVD do subconjunto que EXCLUI os 24
  antônimos E as 24 flexões (~191 verbos neutros, centrados). Vt = modos próprios.
- Alinhamento: top_frac(v,10) = soma dos quadrados das 10 primeiras coordenadas de
  v na base Vt (= fração da norma² nos 10 PCs de topo).
- NULL matched: 500 direções construídas como v_int (média de 12 diferenças de
  pares), mas de pares ALEATÓRIOS dentre os 251 itens (seed 136). p95 = limiar.

## Gates (selados)
G1 (eixos são modos naturais): top_frac(v_int,10) e top_frac(v_tempo,10) ambos
   > p95 do null E >= 0.40. (baseline direção aleatória pura ~ 10/1024 = 0.01.)
G2 (espectro, EXPLORATÓRIO — n baixo, sem gate): expoente da lei de potência nos
   PCs 1..80 (ajuste log-log) e R². Referência Stringer: expoente ~1.
G3 (modos interpretáveis, qualitativo): ler os extremos de PC1, PC2, PC3 do espaço
   neutro; declarar se correspondem a dimensões semânticas reconhecíveis.

## Interpretação selada
G1 passando: os eixos que custaram exemplos rotulados são modos que o espaço já
continha — "12 exemplos → 1 régua" REDESCOBRE geometria intrínseca, não a impõe.
G3 interpretável: o espaço tem seu próprio vocabulário de modos, análogo às form
constants. Isto é conexão estrutural (mesma matemática: modos de operador), NÃO
alegação de que significado e córtex sejam "a mesma coisa".

## Aposta pessoal do agente (placar: acerto EXISTÊNCIA de eixos, erro saltos/corpos)
G1 passa forte para intenção (top_frac >= 0.6) e moderado para tempo (>= 0.4).
G2: aproximadamente lei de potência, expoente em [0.7, 1.4]. G3: pelo menos 1 dos
3 PCs de topo é claramente interpretável. (Este é teste de EXISTÊNCIA de eixo —
meu ponto forte histórico.)

## Regra de parada
Uma rodada. Sem métrica nova após os números.
