#!/usr/bin/env python3
"""Exp 4 — o firmamento: remover o subespaço da forma. PREREGISTRO-EXP4.md."""
import json, os, random
import numpy as np
import resonance
from resonance import (load_dataset, l2, trigrams, cohens_d, perm_test,
                       hit_at_5, SEED, DIR)

resonance.MODEL = "bge-m3"
K_FORM = 50
DEMO = ["amar", "casar", "comprar"]


def build_spaces():
    d, words = load_dataset()
    X = l2(resonance.embed(words))
    vocab = sorted({t for w in words for t in trigrams(w)})
    tix = {t: j for j, t in enumerate(vocab)}
    F = np.zeros((len(words), len(vocab)))
    for i, w in enumerate(words):
        for t in trigrams(w):
            F[i, tix[t]] += 1
    Fc = F - F.mean(axis=0)
    U, Sv, _ = np.linalg.svd(Fc, full_matrices=False)
    F50 = U[:, :K_FORM] * Sv[:K_FORM]
    Xc = X - X.mean(axis=0)
    B, *_ = np.linalg.lstsq(F50, Xc, rcond=None)
    X_form = F50 @ B
    var_form = float(np.sum(X_form ** 2) / np.sum(Xc ** 2))
    return d, words, l2(Xc), l2(Xc - X_form), var_form


def metrics(tag, d, words, X):
    idx = {w: i for i, w in enumerate(words)}
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

    sim_syn, sim_ant = sims(d["syn_distinct"]), sims(d["antonyms"])
    sim_par, sim_rand = sims(d["paronyms"]), sims(rand_pairs)
    obs, p = perm_test(sim_syn, sim_rand)
    d_syn = cohens_d(sim_syn, sim_rand)
    d_par = cohens_d(sim_par, sim_rand)
    order = np.argsort(-S, axis=1)

    def rank(q):
        i = idx[q]
        return [words[j] for j in order[i] if j != i]

    h5 = hit_at_5(d["syn_distinct"], rank)
    r_aff = ((np.mean(sim_ant) - np.mean(sim_rand))
             / (np.mean(sim_syn) - np.mean(sim_rand)))

    def q_factor(w):
        i = idx[w]
        s = np.delete(S[i], i)
        return (np.sort(s)[-5:].mean() - np.median(s)) / s.std()

    q_spec = float(np.mean([q_factor(w) for w in d["specific"]]))
    q_poly = float(np.mean([q_factor(w) for w in d["polysemous"]]))

    print(f"\n[{tag}]")
    print(f"  G1 sinônimos: d = {d_syn:.2f}  p = {p:.5f}")
    print(f"  G2 hit@5    : {100*h5:.1f}%")
    print(f"  G3 parônimos: d = {d_par:.2f}")
    print(f"  R antônimos : {r_aff:.3f}")
    print(f"  Q espec/poli: {q_spec:.2f} / {q_poly:.2f}")
    for q in DEMO:
        print(f"  {q} → {', '.join(rank(q)[:5])}")
    return {"d_syn": float(d_syn), "p_syn": float(p), "hit5": h5,
            "d_par": float(d_par), "R": float(r_aff),
            "q_spec": q_spec, "q_poly": q_poly}


def main():
    d, words, X_cent, X_sem, var_form = build_spaces()
    print(f"banco: {len(words)} verbos · variância explicada pela forma "
          f"(k={K_FORM}): {100*var_form:.1f}%")
    out = {"var_form": var_form,
           "centrado": metrics("apenas centrado (controle)", d, words, X_cent),
           "purificado": metrics("purificado (sem forma)", d, words, X_sem)}
    json.dump(out, open(os.path.join(DIR, "results4.json"), "w"), indent=1)
    print("\nresults4.json gravado.")


if __name__ == "__main__":
    main()
