# Fase 2 — amostra cega (rotular: severo ou benigno)
Selada 2026-07-15. Rotulador vê SÓ os textos. Sem scores.
Mapping selado à parte (sha256 344949a078f7010ac29da9b54920e5b2…) —
só entra no repo APÓS a rotulagem, junto com o relatório.

 1. mission_post valida completude do receipt_candidate (artifact_hash+evidence_refs) mas NÃO confere candidate.scope.boundary_version contra o boundary vivo do bloco (server.rs:2912, mission_letter.rs:477) — aceita candidate v1 sobre bloco v3 silenciosamente; foi assim que a carta stale msn_17a1d1f9b013 entrou

 2. workspace_root do owner servido flipou para /Users/kle1nz/m1nd/npm/bin após executor rodar o shim (via first-minute) de dentro de npm/bin — classe #326: verbo de conveniência rebindou owner compartilhado a partir do cwd; human_view card denunciou (bound: …/npm/bin)

 3. full re-federation of two immutable snapshots did not return after 60 seconds and was terminated

 4. two read-only seek calls over a 278-node federated graph did not return after 50 seconds and the orchestration cell had to be terminated

 5. RECORRÊNCIA do flip de workspace_root: agora /Users/kle1nz/m1nd/npm/test (ontem npm/bin). Gatilho desta vez: suite npm test do executor rodou m1nd-mcp local de dentro de npm/test. HIPÓTESE com mecanismo: processos m1nd-mcp locais/efêmeros escrevem entradas no instance registry (ou runtime compartilhado) e a resolução de workspace_root do owner lê a entrada mais fresca — qualquer run local de subdiretório envenena o binding do owner servido. Auto-heal de boot cura no kickstart mas re-envenena a cada test run

 6. Opening a dormant project brain from the Hall REGISTERS A NEW instance entry instead of upserting the existing one — the same store accumulated 3 registry entries and the Hall rendered 3 identical 'reporooms' cards (each with the duplicate-workspace badge: detection exists, cure does not). Clicking Open brain on a dormant card literally adds a card. The legacy ~/.m1nd/registry/ holds 252 historical instance entries from the stdio era.

 7. The tray STATUS ITEM never appears in the macOS menu bar on EITHER monitor (confirmed by eye via computer-use screenshots on H27T22 and ASUS MB16AMT): the Tauri process runs, the webview server lives, but no seal icon renders — the owner literally cannot find the bell. This was the PATHOS-declared 'visual proof pending (dev unsigned may be suppressed)'; it is now a confirmed defect. The app is ad-hoc signed; possible causes: NSStatusItem not created under the ad-hoc/Accessory config, icon asset failing to load in the bundled build (tray:dev vs tray:build divergence), or menu-bar overflow hiding it.

 8. CORRIGE meus 2 field reports de 03:20/03:30: NÃO havia bug de persistência de cartas — as 12 cartas do regime estão em ~/.m1nd/runtimes/claude/mission-control/ com mtime de criação; EU confundi o mailbox de LETTERS (mission_post board) com o mission-CONTROL, e li inst_f168ae como instance separado quando ele É o dono bound. O gate do P0 sempre esteve verde. Lição: verificar o disco ANTES de declarar bug de persistência; os dois sistemas com a palavra carta (P0-DIVERGENCES §2) são a armadilha real

 9. A fresh correctly bound Reson session reports memory_exists=1 and north returns the checkpoint file metadata/section, but seek tier=project with exact distinctive terms from the saved claims (Xcode 16.4, web atlas fallback, lint errors, zero Jest tests) returns only code nodes and no individual memory claims. The six claim markers are on disk, ingested=true, and stale=false, yet semantic claim retrieval is absent.

10. memorize recusou brainless_root: entre calls o caller_root reverteu de /Users/kle1nz/BrowserOS p/ /Users/kle1nz (sem brain), apesar do ingest ter bindado antes

11. one-call bootstrap (ingest project_root=~/redsky) reported wire session bound to project brain, but a system_blocks_seed_import write on the SAME wire session was refused with brainless_root because caller_root (~) != brain_root — write guard uses caller_root, not the session bind

12. G2: o detector git (diff --name-only vs baseline) é CEGO a arquivos untracked entre commits — arquivo novo não-addado nunca é visto pelo vigia

13. clicar em Scan num brain sem skeleton trava a UI um tempão sem loading bar, sem elapsed, sem estado visível — parece congelado durante o clustering de 2411 nós

14. after memorize (agent-memory ingest merge) the project-brain manifest workspace_root flipped from /Users/kle1nz/redsky to .../project-brains/<id>/agent-memory; north now returns reception caller_root_mismatch with bound_workspace=agent-memory and suggests ingest project_root=/Users/kle1nz (home!), which would be an overlap_parent trap

15. grafo do owner ENCOLHEU 10573→704 nós: graph_snapshot.json multi-MB sobrescrito por 641K (hoje 19:47). Cadeia suspeita: prova viva do #370 rodou ingests estrangeiros no binário buggy contra o owner vivo (flip de workspace_root) → owner persistiu grafo pequeno/poluído sobre o snapshot canônico. ingest_roots.json íntegro (recuperável por re-ingest total). Residual conhecido do #370 (ingest estrangeiro ainda muta o GRAFO) compôs com persist

16. após o ciclo de hoje (daemon ligado no bound + restarts), o seam REST sem brain selector responde SEMPRE caller_root_mismatch (bound_workspace = agent-memory dir vs caller home) — a voz/cockpit via REST puro perderam o cartão de estado; ontem o mesmo curl devolvia recv:match com sino

17. flake de CI no macos-latest: o guard-port do teste de migração offline detectou um listener em porta efêmera (49307) — provável colisão com teste paralelo do mesmo run que sobe listener; o teste recusa honestamente e falha

18. The three promoted house laws EXIST in the medulla box (agent-memory .light.md with the full promotion chain, C8.4-verified) but semantic recall does not surface them: seek tier=medulla for 'who may land a receipt, who may ratify, may an engine abstain' returned only code-graph nodes (an enum variant named May, the ratify fn), and the north memory beat says '30 claims, none surfaced'. Likely: the freshly written/promoted .light.md files have not been re-ingested into the graph embedding space yet (the agent-memory ingest root updates on tick/persist), or the medulla tier path searches an index the promotion did not touch.

19. memorize via REST POST /api/tools/memorize?brain=/Users/kle1nz/m1nd refused with ok:false claims_written:0 even when curl ran from cwd=/Users/kle1nz/m1nd (an ingest_root of the served owner). caller_root resolved to the process cwd and the write gate treated it as caller_root_mismatch, suggesting ingest project_root. Wrote to the mission report instead.

20. The supersession gate refuses ANY rewrite when either side lacks a confidence field ('unknown confidence => cannot compare => WouldDowngrade') — a claim authored without confidence becomes IMMUTABLE via memorize: even a strictly stronger rewrite (authored->verified, same text, by a different agent) is refused with the generic would_downgrade note, which does not name the real cause (missing confidence). The C8.4 verification flow hit this live: the verifier could not flip two FAITHFUL doctrine claims to verified. Workaround: delete the draft (author's own, unpromoted) and FirstWrite the verified version.

21. From a Codex task rooted in a generated projectless folder, ingest(project_root=reson-app) and memorize succeeded in the Reson project brain. Immediate cross_verify transiently listed the new L1GHT file as missing_from_graph, while the next north did retrieve it stale=false. That north simultaneously reported binding.ok=true/full_trust for the Reson brain and reception caller_root_mismatch for the generated Codex cwd, making continued write safety ambiguous even though memory delivery worked.

22. After refreshing PATHOS at HEAD and re-ingesting the bound RESON brain, soul_check correctly reports zero commit lag and no consistency findings but classifies 72 evidence claims as stale; most ordinary state bullets are unanchored, and the canonical GitHub HTTPS remote is misclassified as a local path with evidence_file_missing.

23. cross_verify reports all 10 agent-memory .light.md files as missing_from_graph even though memorize ingested the new memory and an explicit light merge ingest parsed all 10 files with 158 nodes created and 134 evidence links resolved.

24. abrir README.md de um bloco no Build Map de um brain recém-criado devolve tool_error: invalid params for file_view: system-block store I/O error: No such file or directory (os error 2)

25. REFINAMENTO do report anterior: as cartas do regime (aceitas com proof packets via mission_start/event/close ?brain=/Users/kle1nz/m1nd) têm ZERO arquivos em qualquer mission-control/ do disco — viveram em memória num runtime de instance hospedado e MORRERAM nos kickstarts do dia; as 2 cartas codex-redsky do mesmo período persistiram normalmente no project-brain delas — o caminho hospedado-por-?brain= aceita e responde mas não persiste (ou persiste em runtime efêmero)

26. FIRST LIVE F12 curation end-to-end in production, and the guards proved themselves twice in one hour: (1) the first hand-runner mission curated a fresh 35-block candidate into 31 blocks (4 architectural merges, all 31 renamed with domain language, deliberate non-merges justified in the report) — 34 ops proposed as DATA, o5-sanitized, applied seat runner under OCC, summary letter on the chain, ~80s wall clock; the owner ratified the curated map touching only the review screen and the ratify button (the F12-TECH §5 arc gate, met exactly). (2) A SECOND mission's proposal referenced a hallucinated survivor block id (a doubled slug) and the preflight refused the WHOLE batch atomically with the honest reason on screen — nothing persisted.
