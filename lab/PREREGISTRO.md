# Pré-registro — Ressonância semântica de verbos (pt-BR)
Data: 2026-07-10 · Formulador da hipótese: Max Kle1nz · Desenho: agente + veredito askGOD (CHANGE aplicado integralmente)

## Fronteira epistêmica (exigência do oráculo, achado 2)
Este experimento testa a OPERACIONALIZAÇÃO da hipótese do usuário — "espectros
determinísticos + ressonância/dissonância como busca semântica quase instantânea" —
na tradução: espectro = embedding n-D aprendido do uso; ressonância = produto
interno; busca = 1 matmul. Ele NÃO testa (nem pode testar) a metafísica de
frequências intrínsecas das palavras. Um resultado positivo prova que o mecanismo
proposto FUNCIONA como descrito; não prova de onde os espectros "vêm".

## Hipóteses e predições (fixadas antes de qualquer embedding)
H-R (ressonância): sinônimos de radical DISTINTO ressoam (similaridade alta) muito
  acima de pares aleatórios. Predição: p<0.01 (permutação) E Cohen's d >= 1.0
  (limiar de efeito exigido pelo oráculo por causa da anisotropia do espaço).
H-B (busca): emitir o espectro de um verbo recupera seu sinônimo no top-5 do
  ranking (hit@5, query excluída, duas direções, pares radical-distinto).
  Sucesso: hit@5 >= 50% E hit@5(embedding) >= hit@5(char-3gram) + 20 p.p.
H-F (forma não é significado):
  [C1'] baseline char-3gram (o rival sério, exigido pelo oráculo no lugar do hash):
        deve perder de H-B por margem >= 20 p.p.
  [PAR] parônimos (casar/caçar…): similaridade de FORMA alta, mas ressonância
        semântica prevista ~= pares aleatórios (embedding não ressoa por letras).
H-1D (o acorde não cabe numa frequência):
  [C2] método FIXADO: projeção na 1ª componente principal (PCA-1 via SVD dos
       embeddings centrados — a MELHOR redução 1D possível, pior caso para nós);
       ranking por distância absoluta em 1D. Predição: hit@5(PCA-1) < 50% do
       hit@5(embedding completo).
H-A (antônimos — predições RIVAIS, deliberadamente em conflito):
  · Física-ingênua (dissonância máxima): sim(antônimos) ~= sim(aleatórios).
  · Linguística distribucional (afinação de contexto): sim(antônimos) >> aleatórios,
    aproximando-se dos sinônimos.
  O dado decide qual lente descreve o mecanismo.
H-Q (fator Q, expansão proposta pelo oráculo): Q(v) = (média sim top-5 − mediana
  sim banco) / desvio sim banco, query excluída. Predição: verbos ESPECÍFICOS
  (fotografar…) têm Q maior que POLISSÊMICOS (ficar, dar…) — polissemia =
  amortecimento. Mann-Whitney unicaudal, p<0.05, n=8+8.
SANITY (não é métrica de hipótese — achado 2 do oráculo): determinismo
  (mesma palavra → mesmo espectro em 2 execuções; max|Δ| < 1e-6) e latência
  (1 consulta = 1 matmul contra N verbos; reportar µs, comparar com varredura serial).

## Materiais e métodos (congelados)
- Espectros: Ollama local, modelo nomic-embed-text, endpoint /api/embed,
  palavra crua no infinitivo, sem prefixo de tarefa (uniforme para todos os métodos).
- Banco: dataset.json deste diretório (n ~= 210 verbos únicos: pares rotulados +
  distratores). Rotulagem lexicográfica feita ANTES de qualquer embedding; fonte =
  conhecimento lexicográfico padrão; limitação declarada: rotulador = o agente
  (viés mitigado por congelamento pré-coleta + hash).
- Similaridade: cosseno (produto interno de vetores L2-normalizados).
- Pares aleatórios de controle: 42 pares sorteados com seed fixa 136 (o "diapasão"
  do projeto), excluindo qualquer par rotulado.
- Estratificação (achado 1 do oráculo): H-R e H-B avaliados no estrato
  radical-DISTINTO (21 pares); estrato radical-compartilhado (6 pares) reportado
  separadamente, sem entrar no critério de sucesso.
- Permutação: 10.000 embaralhamentos, seed 136.
- Estatística Q: aproximação normal do Mann-Whitney (n pequeno; declarado).

## Critério de sucesso global
A ideia do usuário é declarada "possível e demonstrada" se H-R, H-B, H-F e H-1D
saírem como previsto. H-A e H-Q são descoberta, não gate: qualquer resultado neles
é informação nova sobre a natureza do mecanismo.
