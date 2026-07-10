# Review externa do PRD/UML — 2026-07-11 — e disposição da casa
Crítica trazida pelo operador (analista externo). Registro dos pontos e do
que a casa fez com cada um. Regra aplicada: crítica aceita vira diff no
mesmo burst; discordância vira nuance registrada, nunca silêncio.

## Aceites integrais (viraram commit neste burst)
1. NOME QUALIFICADO — "motor de discernimento" pode induzir o overclaiming
   que o produto combate. → Título do PRD agora carrega "(advisory)";
   linguagem externa: "instrumentação semântica local".
2. DETERMINISMO HONESTO — "bit-a-bit" era promessa excessiva (float + GPU +
   runtimes ≠ igualdade bitwise entre máquinas). → RNF2 reescrito:
   reprodutibilidade por perfil de execução selado + tolerância declarada;
   bit-a-bit só onde certificado. Fato registrado: nosso Δ=0,0 foi medido
   INTRA-perfil; igualdade Metal↔ROCm nunca testada (candidata a sanity no
   Exp 13).
3. SLOs SEPARADOS — o µs do matmul pode ser distração se IPC/spawn/contenção
   custarem 1000×. → RNF3 novo: hit/miss/projeção/lote/cold-start/IPC como
   métricas de 1ª classe; a Fase 2 (sombra) mede todos.
4. POLÍTICA DE APLICABILIDADE DO FIRMAMENTO — o sistema precisa saber quando
   está diante de flexões/código, e ABSTER-SE declarando razão. → RF9
   (purification_policy + status abstained no wire).
5. GOVERNANÇA NO WIRE FORMAT — riders estruturados com allowed/forbidden
   actions e max_effect; "a governança precisa aparecer no wire format, não
   apenas no manifesto". → RF10 (measurement envelope).
6. ESTADOS NOVOS NA RÉGUA — EmObservação (shadow) e Suspensa (drift):
   "passou no laboratório" ≠ "apta para produção". → UML §4 atualizado.

## Nuances da casa (registradas, não silenciadas)
A. "O ponto mais original é o protocolo" — quase: para agentes, a
   originalidade é o PRODUTO protocolo × custo-zero. Protocolo sem µs não
   escala para reflexo; µs sem protocolo é o caminho de degradação que o
   próprio crítico descreveu. Separados, ambos existem; o casamento é novo.
B. ENVELOPE COMPLETO NO T0 MATARIA O T0 — proveniência de 10 campos é o alvo
   certo com timing sequenciado: envelope v0 mínimo no sidecar (horas), v1
   completo quando entrar no Rust (T2). Adotar sem engolir.

## Nota do ecossistema
O crítico deduziu, só pelos princípios do PRD, a composição real do
portfólio do operador: "m1nd conhece · synt0ny mede · l1ght prova ·
h4nd age · o rito limita" — l1ght e h4nd existem e ocupam exatamente esses
assentos. Coerência externa confirmada por leitor cego.

## A frase que fica
"synt0ny não pensa pelo agente; impede que o agente precise pensar sobre
tudo."
