# atlas — o léxico inteiro

Fundação do Exp 11 ("o atlas"): levar o laboratório de 227 verbos para o
léxico completo do português.

## Fontes (em `data/`, fora do git — ver .gitignore)
- `wn-data-por.tab` — OpenWordNet-PT via OMW (github.com/omwn/omw-data),
  licença CC BY-SA. 54.071 lemas únicos (55,6k entradas nominais, 8,2k
  verbais, 8,4k adjetivais, 1,9k adverbiais); synset = grupo de sinônimos.
- `tep_layout_one.txt` — TeP 2.0 (NILC/USP; espelho creditado
  github.com/stavarengo/portuguese-brazilian-synonyms), licença CC BY-SA
  (confirmada no PORTULAN CLARIN). 19.885 grupos de sinônimos (4.145
  verbais), 4.276 relações de antonímia (1.158 verbais) — padrão-ouro
  externo ~100× maior que os 12 pares autorais dos Exp 1-10.

## Números da fundação
- União dos dois léxicos: 83.918 lemas — o banco do atlas.
- Interseção (nas duas fontes): 13.273.
- Custo estimado no M4 Max (medido, 119 palavras/s): ~12 min de embedding,
  ~344 MB de espectros (84k × 1024 dims float32).
- Infra decidida por benchmark (2026-07-10): M4 Max local (119 p/s) vs
  GENESIS com RX 7900/ROCm (148 p/s) — 25% de ganho não paga a coordenação
  remota; GENESIS fica de reserva para modelos maiores (24 GB VRAM).

## Estado
Dados adquiridos e inventariados. NENHUM embedding rodado ainda — a doutrina
da casa sela o pré-registro do Exp 11 (com verdict cross-vendor no desenho)
ANTES de qualquer espectro. Desenho previsto: validação externa do eixo da
intenção (TeP), atlas de modos (PCA ~84k × Osgood), lei Q × polissemia
(acepções como ground truth), hubness em escala.
