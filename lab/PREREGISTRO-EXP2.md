# Emenda pré-registrada — Experimento 2 (espectro contextual)
Data: 2026-07-10, APÓS o resultado do Exp 1 e ANTES de qualquer embedding contextual.

## Motivo (diagnóstico do Exp 1, dados em results.json)
Exp 1 FALHOU nas hipóteses semânticas: d(sinônimos)=0.09 (exigido >=1.0), hit@5=0%.
Assinatura da falha: parônimos (forma alta, sentido distante) ressoaram com d=2.05 —
o embedding de PALAVRA ISOLADA é dominado pela forma (caracteres/subwords), não pelo
significado. O instrumento media ortografia, não semântica. Sanity passou
(determinismo 0.0, matmul 3 µs — 6012× mais rápido que serial).

## Mudança ÚNICA (tudo o mais idêntico ao Exp 1)
Espectro contextual: embedding do verbo dentro de 4 frases-moldura FIXADAS AQUI,
média dos 4 vetores, L2-normalizada. A hipótese distribucional: o significado
emerge do uso; o contexto sintático ativa a semântica e dilui a forma.
T1 = "eles decidiram {w} ontem"
T2 = "é difícil {w} todos os dias"
T3 = "ela vai {w} amanhã de manhã"
T4 = "o hábito de {w} mudou a vida dele"

## Predições (fixadas agora)
P1 (H-R ctx): d(sinônimos distintos vs aleatórios) sobe substancialmente; sucesso
    pleno se d >= 1.0 e p < 0.01.
P2 (H-B ctx): hit@5 >= 50% e >= char-3gram + 20 p.p.
P3 (parônimos): a ressonância contextual deles CAI em direção aos aleatórios
    (d < 0.5) — se cair, prova que o novo espectro deixou de medir forma.
P4 (antônimos): permanecem ALTOS (perto dos sinônimos) — predição distribucional:
    produto interno mede afinação de contexto, não harmonia de sentido.
P5 (fator Q): exploratório (sem gate).
Regra de parada: Exp 2 é a ÚLTIMA tentativa desta sessão; se falhar, o veredicto
honesto é "operacionalização local insuficiente — requer instrumento melhor",
sem terceiro ajuste ad-hoc.
