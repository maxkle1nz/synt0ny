# Pré-registro — Experimento 13 ("a espinha, fase 1")
Data: 2026-07-11. Selo ANTES de ler qualquer texto de report ou gerar
qualquer embedding. PUREZA DECLARADA: o agente viu somente contagens de
classe do ~/.m1nd/field-reports.jsonl (31 friction, 30 triage, 15 bug,
11 honesty, 10 win; 97 linhas; 53 agentes) — nenhum campo "what" foi lido.
Os 48 exemplos das réguas são AUTORAIS, em inglês, escritos de memória
sobre o estilo de field-reports, congelados em exp13.py (selado junto).

## Hipótese (o teste da espinha + a 1ª expansão de idioma do synt0ny)
Réguas de 12 exemplos, re-seladas em INGLÊS (lei do conselho: nunca
transplantar o eixo pt), triam telemetria real de agentes com utilidade
acima do null — a µs e custo zero — cobrindo a classe de micro-julgamentos
que hoje exigiria uma chamada de LLM por item.

## Materiais (congelados)
- Dados: campo "what" dos 97 reports (rótulo = campo "class", declarado por
  53 agentes ao longo de semanas — ground truth externo).
- Réguas (2): R1 bug↔win = unit(mean(12 ex. bug) − mean(12 ex. win));
  R2 honesty-smell = unit(mean(12 ex. overclaim) − mean(12 ex. calibrado)).
- Encoder: bge-m3 (A), embeddings crus L2. FIRMAMENTO: purification_policy =
  disabled, reason = domain-not-covered (treinado em trigramas de verbos pt;
  não se aplica a frases inglesas) — exercitando o RF9 do PRD: abster-se
  declarando, não inventar.
- Saída no measurement envelope v0 (RF10): axis_id+versão, score, percentil,
  riders codificados, max_effect=reverify. Governança no wire desde o 1º dia.
- Nulls matched: 300 eixos 12-vs-12 amostrados dos próprios 97 reports com
  rótulos aleatórios (mesma construção, mesmo domínio), por gate.
- Justificativa sem verdict de oráculo: desenho herda Exp 10/12 (3× auditado
  por panel); rodada de rotina da linha, declarada.

## Gates (selados)
G1 (R1 separa bug de win): AUC nos 25 reports reais dessas classes >= 0.80
   E > p95 do null de AUCs. (AUC como métrica primária — lição do artefato
   de mediana do Exp 12.)
G2 (R2 ranqueia honesty): precision@10 sobre os 97 >= 4/10 E > p95 do null.
   (acaso: ~1,1 honesty em 10.)
G3 (a economia da espinha): latência medida de projeção (µs/report) e de
   embedding 1× (ms/report) vs LLM local real (qwen2.5:7b no Ollama,
   classificação de 5 reports, s/report). Gate: razão reflexo-vs-LLM >= 10^4
   na fase quente (cache hit).

## Aposta do agente (leitura → histórico manda não subestimar demais)
G1 AUC 0,82 (passa). G2 3/10 (FALHA o gate — honesty é o sinal mais sutil).
G3 passa com folga (~10^5-10^6).

## Regra de parada
Uma rodada. Sem métrica nova após os números. Falha em inglês = primeira
fronteira de idioma mapeada com número, não desculpa.
