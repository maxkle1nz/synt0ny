#!/usr/bin/env python3
"""Exp 5 — a reflexão hermética. PREREGISTRO-EXP5.md."""
import json
import os

import numpy as np

from exp4 import build_spaces
from resonance import DIR


def unit(v):
    return v / np.linalg.norm(v)


def run(tag, X, d, words):
    idx = {w: i for i, w in enumerate(words)}
    pairs = [(idx[a], idx[b]) for a, b in d["antonyms"]]
    diffs = np.array([X[p] - X[n] for p, n in pairs])
    rng = np.random.default_rng(136)
    v_rand = unit(rng.standard_normal(X.shape[1]))

    def rank_of(query_vec, target_i, exclude_i):
        sims = X @ query_vec
        sims[exclude_i] = -np.inf
        order = np.argsort(-sims)
        return int(np.where(order == target_i)[0][0]) + 1

    acc_pol = acc_rnd = 0
    ranks_before, ranks_pol, ranks_rnd = [], [], []
    for k, (p, n) in enumerate(pairs):
        v = unit(np.delete(diffs, k, axis=0).mean(axis=0))
        if X[p] @ v > X[n] @ v:
            acc_pol += 1
        if X[p] @ v_rand > X[n] @ v_rand:
            acc_rnd += 1
        for src, tgt in ((p, n), (n, p)):
            ranks_before.append(rank_of(X[src].copy(), tgt, src))
            refl = X[src] - 2 * (X[src] @ v) * v
            ranks_pol.append(rank_of(refl, tgt, src))
            refl_r = X[src] - 2 * (X[src] @ v_rand) * v_rand
            ranks_rnd.append(rank_of(refl_r, tgt, src))

    top5 = sum(1 for r in ranks_pol if r <= 5)
    print(f"\n[{tag}]")
    print(f"  P1 separação LOO : v_pol {acc_pol}/12 · v_rand {acc_rnd}/12")
    print(f"  P2 rank do antônimo — mediana: antes {np.median(ranks_before):.0f}"
          f" · refletido {np.median(ranks_pol):.0f}"
          f" · controle aleatório {np.median(ranks_rnd):.0f}")
    print(f"  P2 top-5 pós-reflexão: {top5}/24")

    v_full = unit(diffs.mean(axis=0))
    proj = X @ v_full
    order = np.argsort(-proj)
    pos = [words[i] for i in order[:10]]
    neg = [words[i] for i in order[-10:][::-1]]
    print(f"  P3 eixo da intenção ⊕: {', '.join(pos)}")
    print(f"  P3 eixo da intenção ⊖: {', '.join(neg)}")

    ia, io = idx["amar"], idx["odiar"]
    v_loo = unit(np.delete(diffs, [i for i, pr in enumerate(pairs)
                                   if pr == (ia, io)], axis=0).mean(axis=0))
    refl_amar = X[ia] - 2 * (X[ia] @ v_loo) * v_loo
    print(f"  manchete: cos(amar, odiar) = {X[ia] @ X[io]:.3f} → "
          f"cos(refletir(amar), odiar) = {unit(refl_amar) @ X[io]:.3f}")
    return {"acc_pol": acc_pol, "acc_rnd": acc_rnd,
            "med_before": float(np.median(ranks_before)),
            "med_pol": float(np.median(ranks_pol)),
            "med_rnd": float(np.median(ranks_rnd)), "top5": top5,
            "axis_pos": pos, "axis_neg": neg}


def main():
    d, words, X_cent, X_sem, _ = build_spaces()
    out = {"centrado": run("centrado (controle)", X_cent, d, words),
           "purificado": run("purificado (espaço primário)", X_sem, d, words)}
    json.dump(out, open(os.path.join(DIR, "results5.json"), "w"), indent=1)
    print("\nresults5.json gravado.")


if __name__ == "__main__":
    main()
