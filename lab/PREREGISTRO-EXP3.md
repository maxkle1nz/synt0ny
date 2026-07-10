# Pré-registro — Experimento 3 (instrumento à altura)
Data: 2026-07-10, ANTES do download do modelo e de qualquer embedding novo.

## Mudança ÚNICA vs Exp 1
Instrumento: nomic-embed-text (274 MB) → bge-m3 (multilíngue, ~1,2 GB, 1024 dims).
Todo o resto idêntico e reutilizado: dataset.json (hash e1650...02a8), palavra crua
no infinitivo, seed 136, mesmos 42 pares aleatórios, mesmas métricas e limiares.
Execução: exp3_run.py = cópia mecânica de resonance.py (hash f8104...37a1) com
exatamente 2 substituições (nome do modelo; nome do arquivo de resultados) —
diff auditável antes da run.

## Gates (idênticos ao Exp 1)
G1 separação: d(sinônimos distintos vs aleatórios) >= 1.0 E p(perm) < 0.01
G2 recuperação: hit@5 >= 50% E >= char-3gram + 20 p.p.
G3 forma: parônimos com d < 0.5 (o espectro deixa de ouvir as letras)
G4 dimensionalidade: hit@5(PCA-1) < 50% do hit@5(espectro completo)

## A questão decisiva — antônimos (predições rivais, seladas)
Razão de afinação R = (média_antônimos − média_aleatórios) / (média_sinônimos − média_aleatórios),
calculada SOMENTE se G1 passar (senão o instrumento não tem autoridade para decidir).
· R <= 0.25 → vence a FÍSICA-INGÊNUA: antônimos dissonam (ficam com os aleatórios).
· R >= 0.60 → vence a DISTRIBUCIONAL: antônimos afinam (produto interno mede
  afinação de contexto, não harmonia de sentido) → a fronteira da FASE se abre.
· 0.25 < R < 0.60 → inconclusivo, declarado como tal.

## Predição pessoal do agente (registrada para accountability)
Os 4 gates passam; antônimos dão R >= 0.60 (vence a distribucional).

## Exploratório (sem gate)
Fator Q (específicos vs polissêmicos), mesmas definições do Exp 1.

## Regra de parada
Experimento FINAL da linha "instrumento" nesta sessão. Resultado é o que for —
nenhum ajuste pós-dados, nenhuma métrica nova depois de ver os números.
