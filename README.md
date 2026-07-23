# synt0ny

A local lab for the geometry of meaning, and an advisory engine built from what survived it. Reads text with local embeddings, orders an operator's attention, and never decides anything.

## What this is

Two things that grew into one. A **lab** that measures the real structure of meaning inside local embeddings (Ollama, `bge-m3`) under a pre-registration protocol. And **the spine** — an advisory engine that reads streams of text and ranks what an operator should look at first. No LLM in the hot path. No network. It never decides, promotes, or blocks.

It started 2026-07-10 as a conversation about matrices and LLMs. The speculative hypotheses died in the first pre-registrations — they are still in `lab/`, numbered, with their seals. What passed the gates became an instrument. In five days the work went from the first measurement to an approved blind production audit.

The method is the product. Every measurement follows the rite: a pre-registration sealed with SHA-256 **before** the data, an empirical matched null, leave-one-out, gates and a stopping rule written in advance, the agent's bet recorded, and every refutation committed with the same weight as a win.

## Status — honest

**Proven** (each carries a seal dated before the data, and a written report):

- **Firmament** (Exp 4): 31.4% of the `bge-m3` spectrum's variance is orthographic form, removable by regressing out 50 trigram axes. Paronyms (*casar*/*caçar*) stop resonating (d 3.74 → −1.85) and the meaning survives.
- **Intent axis** (Exp 5): one direction drawn from 12 antonym pairs, 12/12 on leave-one-out, orthogonal to the time axis (cos −0.01, Exp 6).
- **Dial `bug_win_en`** (Exp 13): AUC 0.853 separating bug↔win in real field reports, above the matched null (0.747). Ground truth: 97 reports labeled by 53 agents.
- **Dial `valencia_pt`**: 12/12 leave-one-out (Exp 5), the axis carries to phrases (100% on 52 phrases, 14/14 on unseen vocabulary — Exp 10), and it holds in production — 93.2% accuracy, AUC 0.979 on 500 real customer reviews (Exp 12).
- **Phase 2 — blind, pre-registered production audit** (2026-07-15): after 5 days of autonomous shadow (0 failed ticks), the dial-ranked top-10 held **9/10 severe reports against 7/10 for the chronological queue** — the +2 margin gate cleared on the wire. The blind labeler was a separate agent from the one who sealed the sample. Minutes: `spine/RELATORIO-FASE2.md`.
- **Operation**: a routine tick costs 0.04–0.09s; the hot path is roughly 56.6 million times cheaper than asking an LLM per read.

**Refuted, and published with the same prominence** (honesty carries a number):

- Attribute transmutation (Exp 5 / 6 / 9): attributes are *readable* directions, not *writable* operations. Reflecting "love" does not produce "hate."
- Commit-risk prediction (Exp 14): AUC 0.439. Dead.
- A `feat↔fix` dial for certification (Exp 15): AUC 0.719, under the 0.80 gate. The signal is real; it does not clear the bar.

**Where it stopped.** T0 — the advisory spine running in shadow over m1nd's exhaust — is proven. T1–T3 are designed, not built (see `docs/FRONTEIRA-M1ND.md`). And the production audit was won once, on the exact edge of its gate; composite confidence is meant to come from the windows that follow, which the rite re-audits for free.

**Known limits, stated plainly:**

- The dial reads **tone, not truth**. A declared CI flake reached the audit's top-10 because it *sounds* severe. That false-positive class is characterized, not hidden.
- Single encoder in the hot path (every read carries a `SINGLE_ENCODER` rider). Promoting a finding to "geometry of the language" needs a second instrument.
- Linear purification is aggressive: it separates paronyms but mutilates pairs whose legitimate similarity runs parallel to spelling (inflections — Exp 6).
- Validated on 227 Portuguese verbs; nouns and phrases are extrapolation until re-sealed.

## The constitution

Dials **read, never write**. They do not decide, promote, or block; a rider's strongest effect is `reverify`; nothing is written outside `~/.m1nd/synt0ny/`. The rule rests on two independent foundations: synt0ny's own experimental trilogy (attributes are readable directions, not write operations) and m1nd's constitution — *a letter cannot color the map*.

## Run it

The tool needs Python with `numpy` and a local Ollama serving `bge-m3`. The first run builds and caches the spectra.

```
python3 synt0ny.py buscar <verb>          # neighbors by resonance (zero-shot)
python3 synt0ny.py intencao <verb> ...    # position on the ⊖ dissipation / accrual ⊕ axis
python3 synt0ny.py eixo                    # the extremes of the axis in the bank
```

Words outside the bank work zero-shot. The spine runs as a launchd job (`com.synt0ny-shadowd`, 5-minute tick, fail-quiet); a health panel lives at `127.0.0.1:1341` (`com.synt0ny-panel`). Agents read the engine through MCP (the `synt0ny_read` tool) or `POST /api/read`.

The numbered experiments in `lab/`, `atlas/`, and `spine/` are the living record — pre-registration, code, and results side by side. The dials in `dials/` ship as `axis.npz` plus a manifest carrying their certification and their `bula` (the limits label).

## Continue from here

MIT — see `LICENSE`. Fork it. The one rule that does not bend: seal before you measure, and report every failure with a number.

The next attacks, reading the code:

- **T1 — the downstream test.** T0 proved the instrument reads m1nd's exhaust. T1 is the counterfactual: does the reading actually change what happens next? That is the A/B the frontier doc is waiting on.
- **Break the single-encoder ceiling.** Every hot-path read is one encoder by declaration. A second instrument is what turns a dial reading into a claim about the language.
- **Reuse-first, honestly.** The frontier names its own donors — SetFit, bge-reranker, FastEmbed, cleanlab, mem0's dedupe. Each enters a sealed A/B against what's here. If the donor wins with a number, adopt the donor.

---
<p align="center">
  <img src="assets/deviance-prism-icon.png" width="44" alt="DEViance Intelligence">
  <br>
  <sub>A <b>DEViance Intelligence</b> prototype — <i>beyond the edge</i> · by <a href="https://github.com/maxkle1nz">Max Kle1nz</a></sub>
</p>
