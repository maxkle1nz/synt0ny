# Pré-registro — Experimento 11 ("o atlas") — v2 pós-verdict fable
Status: verdict fable CHANGE aplicado (5 achados); aguardando fugu para fechar
o panel. Selo SHA-256 após o panel e ANTES de qualquer embedding do léxico.

## Mudanças v2 (achados fable, todos aplicados)
1. Q com exclusão de self POR ÍNDICE (duas fórmulas explícitas por
   pertencimento à amostra); self residual em mediana/std de linhas da amostra
   declarado (efeito <= 1/5000, desprezível).
2. Spearman com RANKS MÉDIOS em empates (zipf=0 em massa não contamina mais a
   parcial); fração de zipf=0 reportada.
3. Gate E3 endurecido: rho_parcial <= −0.10 E p < 0.001 E IC95 bootstrap
   (300 reamostras) inteiramente abaixo de −0.05.
4. Null E1 usa o MESMO conjunto de relações do teste real (guarda idêntica,
   gmeans pré-computadas; sem subconjunto [:400]).
5. PCA no léxico INTEIRO (float32; era subamostra de 40k); hubness continua em
   amostra de 5k, DECLARADA como subestimativa do fenômeno.
6. (Risco fable) Eixo secundário v_tep: PC1 das diferenças de 12 relações
   verbais do PRÓPRIO TeP sorteadas held-out (seed 136), testado nas demais —
   se replicar a fração do v12, mata "idiossincrasia dos 12 pares autorais".
   E LIMITAÇÃO EPISTÊMICA DECLARADA: bge-m3 e qwen3 são encoders treinados em
   corpora sobrepostos — "passa nos dois" refuta idiossincrasia de MODELO,
   não estabelece independência total; concordância inter-instrumento
   (Spearman entre Q_a/Q_b e proj_a/proj_b) será REPORTADA como medida da
   redundância entre instrumentos.

## Mudanças v3 (verdict fugu CHANGE, panel fechado — vereditos concordantes)
7. `compare` A×B implementado no script (rótulo final "geometria da língua"
   vs "idiossincrasia" + concordâncias) — obrigatório no fechamento.
8. GATE E1 endurecido com SEGUNDO null matched por categoria: 300 eixos de 12
   pares de VERBOS aleatórios (não só lemas quaisquer); o real deve superar o
   p95 dos DOIS nulls. Reportados: fração de grupos com 1 só palavra e E1
   restrito a grupos >= 2 (sensibilidade). Cluster-bootstrap por grupo NÃO
   implementado nesta rodada (justificativa: a métrica é por-relação com
   null matched; o cluster-IC refinaria a incerteza sem mudar o ponto —
   registrado como melhoria de Exp 12+).
9. E3 com regra única (ver seção E3) + sensibilidades fr>0 e 1-palavra.
Risco fugu aceito e declarado: cobertura/fonte/frequência/locução podem
mediar resultados; as sensibilidades seladas são o controle desta rodada.

## Objeto e instrumentos
- Léxico: união OWN-PT + TeP 2.0 = 83.918 lemas (atlas/README.md; locuções
  multi-palavra mantidas — é o léxico real).
- Instrumento A: bge-m3 (M4 Max local, 1024 dims).
- Instrumento B: qwen3-embedding:8b (GENESIS RX 7900 via túnel ssh, 4096 dims).
  B é CONDICIONAL ao pipeline (Ollama 0.31.2 em instalação); se indisponível,
  A roda e B fica pendente declarado.
- REGRA MULTI-INSTRUMENTO (selada): gates E1 e E3 só contam como "geometria da
  língua" se passarem NOS DOIS instrumentos; passando em um só = "idiossincrasia
  de modelo" (resultado válido, rótulo diferente).
- Espaço: embeddings L2, centrados no léxico completo, re-L2. SEM firmamento
  (léxico flexionado/famílias — lição do Exp 6; régua-por-par fica p/ Exp 12+).

## E1 — Validação externa do eixo da intenção (gate)
- Do TeP: todas as relações de antonímia VERBAL grupo↔grupo (~1.158; dedup de
  relações recíprocas). Grupo → média L2 dos espectros de suas palavras.
- Eixo v12: os MESMOS 12 pares de antônimos do dataset.json dos Exp 1-10
  (direção conhecida) — zero contato prévio com o TeP.
- Métrica: fração de relações com médias de grupo em LADOS OPOSTOS do eixo
  (produto das projeções < 0) — não exige saber qual lado é ⊕.
- Null matched: 300 eixos de 12 pares aleatórios de lemas (seed 136) → p95.
- GATE E1: fração real >= 0.75 E > p95, em A e B.
- Exploratório: mesma métrica nas antonímias ADJ/NOUN/ADV (transfer de
  categoria, sem gate).

## E2 — Atlas de modos (exploratório, sem gate numérico exceto replicação)
- PCA (SVD econômica) do léxico centrado, por instrumento.
- Replicação do Exp 8 em escala: top_frac(v12, 10 PCs) > p95 de null matched
  (300 eixos de pares aleatórios) — GATE leve, por instrumento.
- Leitura qualitativa selada: extremos (10 palavras/polo) de PC1..PC5;
  declarar se lembram os fatores de Osgood (avaliação/potência/atividade).
- Espectro de autovalores: expoente de lei de potência (PCs 1..200) e R²;
  comparar com Exp 8 (0,60) e córtex (~1). Sem gate.

## E3 — Lei Q × polissemia (gate)
- Polissemia ground-truth: nº de synsets OWN-PT do lema (fallback: nº de
  grupos TeP quando o lema não está no OWN-PT).
- Q(w) como no Exp 3: (média top-5 − mediana)/desvio das similaridades contra
  AMOSTRA fixa de 5.000 lemas (seed 136), self excluído.
- CONFUNDIDOR ANTECIPADO: frequência (palavras frequentes têm mais sentidos E
  espectros melhores). Controle: correlação PARCIAL de Spearman (ranks médios
  em empates) entre n_sentidos e Q, controlando log-frequência Zipf (wordfreq).
- GATE E3 (regra ÚNICA, unificada pós-panel): rho_parcial <= −0.10 E p < 0.001
  E IC95 bootstrap (300) inteiramente < −0.05 E sensibilidade no subconjunto
  fr>0 também <= −0.10 — em A e B. Sensibilidade adicional reportada sem gate:
  só lemas de 1 palavra com fr>0 (o bloco zipf=0/locuções é confundidor
  estrutural declarado — achado fugu #4).

## E4 — Hubness (exploratório)
- Na amostra de 5.000: k-ocorrência no top-10, skewness da distribuição,
  10 maiores hubs por instrumento. Sem gate; mapeia o fenômeno para Exp 12+.

## Custo estimado
A: ~12 min embedding + ~5 min análise. B: 25-60 min embedding (a medir) +
análise. Espectros ficam em atlas/data/*.npz (fora do git).

## Aposta do agente (calibrada baixo; placar da casa: acerta leitura, erra magnitude)
E1: A 0,78 · B 0,82 (passa nos dois). E2: replica nos dois; expoente 0,5-0,9;
PC1 interpretável, Osgood parcial (avaliação aparece, potência/atividade
incertos). E3: rho_parcial ≈ −0,12 (passa raspando nos dois). E4: hubs
existem, skew > 1.

## Regra de parada
Uma rodada por instrumento. Sem métrica nova após os números. Falha de
pipeline do B = B pendente, não improviso.
