# Pré-registro — Experimento 12 ("a rua": o espectrômetro em dados reais)
Data: 2026-07-11. Selo ANTES de qualquer embedding do lote. O lote foi
amostrado programaticamente (seed 136) SEM leitura dos textos nem projeções.

## Hipótese (o teste de produto)
O espectrômetro (eixo v12 + classificador-mediana, exatamente como validado no
Exp 10 em frases autorais) funciona em dados REAIS de produção que ele nunca
viu: reviews de e-commerce escritas por clientes, com ruído, typos e assuntos
alheios ao produto.

## Materiais (congelados)
- Lote: 500 reviews do B2W-Reviews01 (Americanas; dataset público) — 250 de
  nota 1★ (rótulo ⊖) e 250 de nota 5★ (rótulo ⊕), review_text >= 20 chars,
  seed 136. SHA-256 do lote: b1492b711506e10f1ecbb71645bcdcf26b0070257e08947
  805dd0f4fdc29f3f5. GROUND TRUTH EXTERNO: as estrelas dos próprios clientes.
- Instrumento: A (bge-m3 — o encoder do espectrômetro/CLI). Eixo v12 extraído
  de atlas/data/spectra_a.npz (mesmos 12 pares; sem re-embedding dos verbos).
- Classificador do Exp 10, sem parâmetro livre: sinal de (proj − mediana do
  lote balanceado). AUC (rank-based) reportada.
- Null matched: 300 eixos de 12 pares de lemas aleatórios do atlas (seed 136),
  mesmo classificador → p95.
- Justificativa de desenho sem novo verdict: herda integralmente o desenho do
  Exp 10, auditado por dois oráculos (fable + fugu); nenhum componente novo.

## Gates (selados)
G1 (a rua): acurácia >= 0.80 E > p95 do null matched.
Sensibilidades reportadas sem gate: acurácia em reviews curtas (< 100 chars)
vs longas; 5 erros típicos transcritos para diagnóstico qualitativo.
Faixas de interpretação: 0.70-0.80 = útil com supervisão (triagem, não
decisão); < 0.70 = espectrômetro reprovado na rua, arquivar camada de produto
com honestidade.

## Aposta do agente
Acurácia 83% · AUC 0.90 (extremos 1★/5★ são mais fáceis que adversariais,
mas a rua tem ruído que frases autorais não têm).

## Regra de parada
Uma rodada. Sem métrica nova após os números.
