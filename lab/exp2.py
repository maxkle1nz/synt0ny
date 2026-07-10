#!/usr/bin/env python3
"""Exp 2 — espectro contextual. Emenda pré-registrada em PREREGISTRO-EXP2.md."""
import json, math, os, random, time
import numpy as np
from resonance import (load_dataset, embed, l2, char_sim, cohens_d,
                       perm_test, hit_at_5, SEED, DIR)

TEMPLATES = [
    "eles decidiram {w} ontem",
    "é difícil {w} todos os dias",
    "ela vai {w} amanhã de manhã",
    "o hábito de {w} mudou a vida dele",
]


def embed_ctx(words):
    acc = None
    for t in TEMPLATES:
        X = embed([t.format(w=w) for w in words])
        acc = X if acc is None else acc + X
    return l2(acc / len(TEMPLATES))


def main():
    d, words = load_dataset()
    idx = {w: i for i, w in enumerate(words)}
    n = len(words)
    t0 = time.perf_counter()
    X = embed_ctx(words)
    print(f"banco: {n} verbos · espectros contextuais (4 molduras) "
          f"em {time.perf_counter()-t0:.1f}s")
    S = X @ X.T

    labeled = set()
    for key in ("syn_distinct", "syn_shared", "antonyms", "paronyms"):
        for a, b in d[key]:
            labeled.add(frozenset((a, b)))
    rng = random.Random(SEED)
    rand_pairs = []
    while len(rand_pairs) < 42:
        a, b = rng.sample(words, 2)
        if frozenset((a, b)) not in labeled:
            rand_pairs.append((a, b))

    def sims(pairs):
        return np.array([S[idx[a], idx[b]] for a, b in pairs])

    sim_syn, sim_shared = sims(d["syn_distinct"]), sims(d["syn_shared"])
    sim_ant, sim_par, sim_rand = sims(d["antonyms"]), sims(d["paronyms"]), sims(rand_pairs)

    print("\n== P1: separação contextual ==")
    obs, p = perm_test(sim_syn, sim_rand)
    d_eff = cohens_d(sim_syn, sim_rand)
    print(f"sinônimos {np.mean(sim_syn):.4f} vs aleatórios {np.mean(sim_rand):.4f}"
          f"  delta {obs:+.4f}  d = {d_eff:.2f}  p(perm) = {p:.5f}")

    print("\n== P2: recuperação hit@5 ==")
    order = np.argsort(-S, axis=1)

    def rank_emb(q):
        i = idx[q]
        return [words[j] for j in order[i] if j != i]

    cache = {}

    def rank_char(q):
        if q not in cache:
            ss = sorted(((char_sim(q, w), w) for w in words if w != q), reverse=True)
            cache[q] = [w for _, w in ss]
        return cache[q]

    Xc = X - X.mean(axis=0)
    v1 = np.linalg.svd(Xc, full_matrices=False)[2][0]
    proj = Xc @ v1

    def rank_1d(q):
        i = idx[q]
        js = np.argsort(np.abs(proj - proj[i]))
        return [words[j] for j in js if j != i]

    h_emb = hit_at_5(d["syn_distinct"], rank_emb)
    h_char = hit_at_5(d["syn_distinct"], rank_char)
    h_1d = hit_at_5(d["syn_distinct"], rank_1d)
    print(f"espectro contextual: {100*h_emb:.1f}%")
    print(f"char-3gram (forma) : {100*h_char:.1f}%")
    print(f"PCA-1 (1 freq.)    : {100*h_1d:.1f}%")
    print(f"acaso              : {100*5/(n-1):.1f}%")

    print("\n== P3: parônimos no espectro contextual ==")
    print(f"parônimos {np.mean(sim_par):.4f} vs aleatórios {np.mean(sim_rand):.4f}"
          f"  (d = {cohens_d(sim_par, sim_rand):.2f}; Exp1 era d = 2.05)")

    print("\n== P4: antônimos ==")
    print(f"antônimos {np.mean(sim_ant):.4f} | sinônimos {np.mean(sim_syn):.4f} | "
          f"aleatórios {np.mean(sim_rand):.4f}"
          f"  d(ant vs rand) = {cohens_d(sim_ant, sim_rand):.2f}")

    print("\n== P5 (exploratório): fator Q ==")

    def q_factor(w):
        i = idx[w]
        s = np.delete(S[i], i)
        return (np.sort(s)[-5:].mean() - np.median(s)) / s.std()

    q_spec = [q_factor(w) for w in d["specific"]]
    q_poly = [q_factor(w) for w in d["polysemous"]]
    u = sum(1.0 if a > b else 0.5 if a == b else 0.0 for a in q_spec for b in q_poly)
    z = (u - 32.0) / math.sqrt(64 * 17 / 12)
    p_q = 0.5 * math.erfc(z / math.sqrt(2))
    print(f"Q específicos {np.mean(q_spec):.2f} vs polissêmicos {np.mean(q_poly):.2f}"
          f"  U = {u:.0f}  p = {p_q:.4f}")

    print("\n== demo: sintonize um verbo ==")
    for q in ("começar", "amar", "comprar"):
        top = rank_emb(q)[:5]
        print(f"  {q} ressoa com: {', '.join(top)}")

    json.dump({
        "mean_syn": float(np.mean(sim_syn)), "mean_shared": float(np.mean(sim_shared)),
        "mean_ant": float(np.mean(sim_ant)), "mean_par": float(np.mean(sim_par)),
        "mean_rand": float(np.mean(sim_rand)), "d_syn": float(d_eff), "p_syn": p,
        "hit5_emb": h_emb, "hit5_char": h_char, "hit5_1d": h_1d,
        "d_par": float(cohens_d(sim_par, sim_rand)),
        "d_ant": float(cohens_d(sim_ant, sim_rand)),
        "q_spec": float(np.mean(q_spec)), "q_poly": float(np.mean(q_poly)), "p_q": p_q,
    }, open(os.path.join(DIR, "results2.json"), "w"), indent=1)
    print("\nresults2.json gravado.")


if __name__ == "__main__":
    main()
