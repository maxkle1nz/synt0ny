# Pré-registro — Experimento 4 ("o firmamento": separar forma de sentido)
Data: 2026-07-10, ANTES de qualquer computação do espaço purificado.

## Hipótese (do usuário, formulada via Gênese)
Separações explícitas de domínio purificam o espectro: removendo o subespaço da
FORMA (ortografia) do espectro bge-m3, o bloco restante (SENTIDO) deve
(a) parar de ouvir parônimos e (b) continuar recuperando sinônimos.

## Método (fixado)
1. Espectros: bge-m3, palavra crua, mesmos 227 verbos e seeds (dataset e1650...).
2. Matriz de forma F: contagens de char-3gramas (com padding) por verbo.
3. Subespaço da forma: primeiros K=50 componentes de F (SVD, determinístico).
4. Purificação ("regressing out"): centrar X e F; regressão por mínimos quadrados
   F50 → X; X_sem = L2(Xc − F50·B). Reportar a fração da variância de X explicada
   pela forma.
5. CONTROLE DE ATRIBUIÇÃO: todas as métricas também no espaço APENAS-CENTRADO
   (sem remoção) — a diferença centrado→purificado é o efeito causal da remoção.
6. Demo qualitativo pré-fixado: top-5 de "amar", "casar", "comprar" antes/depois.

## Gates e predições (selados)
P1 (G1'): separação de sinônimos se mantém no purificado: d >= 1.0, p < 0.01.
P2 (G2'): hit@5 purificado >= 50% (barra original) = sobreviveu;
          30–50% = degradação parcial declarada;
          < 30% = a forma carregava sentido de contrabando (descoberta alternativa).
P3 (G3'): parônimos no purificado: d < 0.5 — O GATE DO FIRMAMENTO (falhou no cru
          com d = 2.72; a hipótese do usuário prevê que agora passa).
P4 (R'): razão de afinação dos antônimos recalculada no purificado, MESMOS cortes
         selados (<= 0.25 dissonância; >= 0.60 afinação; entre = inconclusivo),
         condicionada a G1' passar.
P5: fator Q exploratório (sem gate).

## Aposta pessoal do agente (accountability; placar atual: errei 2 de 2)
G1' passa com d >= 1.5 · G2' >= 50% · G3' PASSA (d < 0.5) · R' >= 0.60.

## Regra de parada
Último experimento da noite. Nenhuma métrica nova ou ajuste após ver os números.
