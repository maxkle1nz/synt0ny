# Pré-registro — Experimento 10 ("a ponte": verbo → frase) — FINAL
Data: 2026-07-10. Desenho: agente + verdict fugu CHANGE aplicado integralmente
(3 achados). Selo SHA-256 ANTES de qualquer embedding.

## Hipótese
O eixo da intenção (12 pares de verbos, Exp 5) transfere para frases inteiras.
O bloco adversarial decide O QUE o eixo mede: valência do evento ou tipo
lexical da ação — o resultado NOMEIA o mostrador do produto.

## Materiais (congelados; frases completas em exp10.py, selado junto)
- 52 frases pt (6-12 palavras), balanceadas 26 ⊕ / 26 ⊖, escritas e rotuladas
  antes de qualquer embedding. TRÊS estratos (achado 1 do fugu):
  · seen (24): contêm verbo do treino do eixo;
  · near (16): sem palavras do treino, mas com vizinhos semânticos diretos
    (reformar, restaurar, plantar, florescer, curar, resgatar / demolir,
    rasgar, apodrecer, contaminar, consumir-fogo, envenenar, abandonar,
    sabotar) — blacklist selada aqui;
  · far (12): sem palavras do treino E sem vizinhos diretos — ações sociais/
    abstratas (elogiar, doar, celebrar, adotar, alfabetizar, premiar,
    agradecer, ensinar / roubar, trair, humilhar, mentir, espalhar boato,
    cobrar juros abusivos). É o estrato que testa transferência FRASEAL.
- BLOCO ADVERSARIAL (achado 3; 8 frases FORA do cômputo de G1/G2): destruição
  benéfica (4, rótulo ⊕ pela valência do evento) e construção maléfica (4,
  rótulo ⊖), verbo lexicalmente oposto ao desfecho.
- Eixo: v_int = média L2 de e(pos)−e(neg) dos 12 pares de antônimos, cru.
- Classificador sem parâmetro livre: sinal de (proj − mediana das 52).
  Adversariais julgados com a MESMA mediana (não entram no seu cômputo).
- NULL MATCHED (achado 2): 300 eixos de 12 pares de verbos ALEATÓRIOS do banco
  de 227 (seed 136), mesmo classificador → p95. Null gaussiano: auxiliar.

## Gates (selados)
G1 (ponte): acurácia nas 52 >= 80% E > p95 do null matched.
G2 (transferência fraseal): estrato FAR >= 9/12 (75%).
A1 (o que o eixo mede — leituras seladas, qualquer resultado informa):
   · adversarial >= 6/8: o eixo lê VALÊNCIA DO EVENTO → mostrador batizado
     "valência" (é o que o produto de triagem quer);
   · adversarial <= 2/8: o eixo segue o VERBO → mostrador batizado "tipo de
     ação lexical" (útil, escopo diferente);
   · 3-5/8: misto — batismo adiado, sonda maior necessária.
Faixas de interpretação (herdadas): total 60-80% = recalibrar com frases;
< 60% = mostradores por-domínio.

## Aposta do agente
Total 82% · far 9/12 · adversarial 3/8 (aposto que o eixo segue parcialmente
o verbo — misto, tendendo a lexical).

## Regra de parada
Uma rodada. Sem métrica nova após os números.
