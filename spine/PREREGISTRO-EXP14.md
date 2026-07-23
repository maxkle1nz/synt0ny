# Pré-registro — Experimento 14 ("o radar de commits") — v2 FINAL
Verdict: fugu pendurou no timeout (degradação declarada pela doutrina) →
fable FAST devolveu CHANGE (3 achados + risco de saturação), TUDO aplicado.
Selo ANTES de qualquer embedding. PUREZA: nenhum subject de commit foi lido
pelo agente para desenhar a régua; os 24 exemplos são autorais.

## Mudanças v2 (verdict fable, aplicado integralmente)
1. Ordem do histórico: `--first-parent` (a janela de 20 respeita o branch
   principal; commits de branches mescladas não a poluem). Limitação
   declarada: --name-only não segue renames (falso negativo do rótulo).
2. S1 com dentes: parcial de Spearman MÚLTIPLA controlando log(1+n_files) E
   log(1+frequência-máxima-histórica dos arquivos do commit) — cobre
   quantidade E arquivo-quente; gate = mesmo sinal E |parcial| >= 50% do
   |rho| bruto.
3. Estrato S2 (informativo): AUC excluindo commits cujo PRÓPRIO subject casa
   FIX_RE (auto-fix não infla nem desinfla o gate).
4. SANITY DE SATURAÇÃO pré-embedding (risco do oráculo): a taxa-base do
   proxy deve cair em [10%, 40%]; fora disso, a escada K=[20,10,5,3] é
   percorrida ANTES de qualquer projeção e o primeiro K na faixa vence;
   nenhum K na faixa → corpus declarado "proxy inviável", sem leitura.
   (Calibração de PROXY pré-dados, não ajuste pós-números.)
5. Declarado: AUC com empates conta como derrota (viés conservador).

## Hipótese
Uma régua risky↔cosmetic de 12+12 exemplos autorais, aplicada SÓ à mensagem
do commit, antecipa acima do acaso quais commits serão seguidos de conserto —
o ground truth vem do próprio histórico (replay retroativo), sem esperar
sombra acumular.

## Ground truth (proxy FIX-SEGUIDO, operacionalização selada)
Commit C (não-merge) é rotulado POSITIVO se existe commit D entre os 20
seguintes (ordem cronológica do branch principal) com:
(a) mensagem casando /\b(fix|revert|hotfix|regress)/i, E
(b) pelo menos 1 arquivo em comum com C (interseção de paths tocados).
Limitações declaradas do proxy: (i) fixes sem palavra-chave escapam (falso
negativo do rótulo); (ii) arquivos "quentes" recebem fixes por frequência,
não por culpa de C — controle de sensibilidade abaixo; (iii) commits no fim
da história (< 20 sucessores) são EXCLUÍDOS do cômputo.

## Materiais
- Corpus do gate: ~/m1nd, 800 commits não-merge (mensagens em inglês).
- Estratos exploratórios sem gate: l00p (38), synt0ny (22) e — transferência
  de idioma — an IT corpus (459, mensagens em italiano; régua EN aplicada a IT
  mede transfer de graça, rotulado como exploração).
- Sinal: SUBJECT do commit apenas (1ª linha), embeddings bge-m3 crus L2.
- Régua: v = unit(mean(12 risky) − mean(12 cosmetic)), exemplos congelados
  em exp14.py (selado junto).
- Null matched: 300 eixos 12-vs-12 de subjects aleatórios do próprio corpus.

## Gates (a selar após verdict)
G1 (antecipação): AUC(projeção → FIX-SEGUIDO) no m1nd >= 0.65 E > p95 do
   null. (Commits são sinal muito mais sutil que reviews; 0.65 já é radar
   útil para ORDENAR atenção — o uso é ranking advisory, nunca veto.)
G2 (utilidade de fila): precision@20 do topo do ranking >= 1.5× a taxa-base
   de FIX-SEGUIDO do corpus.
S1 (sensibilidade-confundidor): correlação parcial de Spearman entre
   projeção e rótulo CONTROLANDO log(1+n_arquivos_do_commit) mantém o mesmo
   sinal — commits grandes são mais arriscados E têm mensagem diferente; a
   régua precisa ler além do tamanho.

## Aposta do agente
G1: AUC 0,68 (passa raspando). G2: passa (~2× a base). S1: mantém sinal mas
enfraquece (~30% de queda). IT-corpus: AUC ~0,60 (transfer parcial).

## Regra de parada
Uma rodada. Sem métrica nova após os números.
