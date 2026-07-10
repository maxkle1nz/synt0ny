#!/usr/bin/env python3
"""Exp 7 — leitura por camadas do produto interno. PREREGISTRO-EXP7.md."""
import json
import os
import random

import numpy as np

from exp4 import build_spaces
from resonance import DIR, SEED, cohens_d, perm_test


def unit(v):
    return v / np.linalg.norm(v)


def run(tag, X, d, words):
    idx = {w: i for i, w in enumerate(words)}
    apairs = [(idx[a], idx[b]) for a, b in d["antonyms"]]
    diffs = np.array([X[a] - X[b] for a, b in apairs])
    v_full = unit(diffs.mean(axis=0))

    labeled = set()
    for key in ("syn_distinct", "syn_shared", "antonyms", "paronyms"):
        for a, b in d[key]:
            labeled.add(frozenset((a, b)))
    rng = random.Random(SEED)
    rand_pairs = []
    while len(rand_pairs) < 42:
        a, b = rng.sample(words, 2)
        if frozenset((a, b)) not in labeled:
            rand_pairs.append((idx[a], idx[b]))
    spairs = [(idx[a], idx[b]) for a, b in d["syn_distinct"]]

    def decomp(i, j, v):
        ce = float((X[i] @ v) * (X[j] @ v))
        return ce, float(X[i] @ X[j] - ce)

    ce_ant, cc_ant = zip(*[decomp(a, b, unit(np.delete(diffs, k, 0).mean(0)))
                           for k, (a, b) in enumerate(apairs)])
    ce_syn, cc_syn = zip(*[decomp(a, b, v_full) for a, b in spairs])
    ce_rnd, cc_rnd = zip(*[decomp(a, b, v_full) for a, b in rand_pairs])

    _, p1 = perm_test(list(ce_rnd), list(ce_ant))
    _, p2 = perm_test(list(ce_syn), list(ce_rnd))
    d3 = cohens_d(list(cc_ant), list(cc_rnd))

    def frac(ce, cc):
        return float(np.mean([abs(e) / (abs(e) + abs(c) + 1e-12)
                              for e, c in zip(ce, cc)]))

    print(f"\n[{tag}]")
    print("  camada do EIXO (intenção):")
    print(f"    antônimos {np.mean(ce_ant):+.4f} (LOO) · sinônimos "
          f"{np.mean(ce_syn):+.4f} · aleatórios {np.mean(ce_rnd):+.4f}")
    print(f"    P1 ant < 0 e < rand: média {np.mean(ce_ant):+.4f}, "
          f"p = {p1:.5f} -> {'PASSA' if np.mean(ce_ant) < 0 and p1 < 0.01 else 'FALHA'}")
    print(f"    P2 syn > rand: p = {p2:.5f} -> "
          f"{'PASSA' if p2 < 0.05 else 'FALHA'}")
    print("  camada do CORPO (resto):")
    print(f"    antônimos {np.mean(cc_ant):+.4f} · sinônimos "
          f"{np.mean(cc_syn):+.4f} · aleatórios {np.mean(cc_rnd):+.4f}")
    print(f"    P3 |d(ant,rand)| = {abs(d3):.2f} -> "
          f"{'PASSA' if abs(d3) < 0.5 else 'FALHA'}")
    print(f"  fração |eixo|/|total|: ant {frac(ce_ant, cc_ant):.0%} · "
          f"syn {frac(ce_syn, cc_syn):.0%} · rand {frac(ce_rnd, cc_rnd):.0%}")
    for k, (a, b) in enumerate(apairs):
        print(f"    {words[a]}/{words[b]}: eixo {ce_ant[k]:+.4f} · "
              f"corpo {cc_ant[k]:+.4f}")
    return {"ce_ant": float(np.mean(ce_ant)), "ce_syn": float(np.mean(ce_syn)),
            "ce_rnd": float(np.mean(ce_rnd)), "cc_ant": float(np.mean(cc_ant)),
            "cc_rnd": float(np.mean(cc_rnd)), "p1": p1, "p2": p2,
            "d3": float(d3)}


def main():
    d, words, X_cent, X_sem, _ = build_spaces()
    out = {"centrado": run("centrado (controle)", X_cent, d, words),
           "purificado": run("purificado (primário)", X_sem, d, words)}
    json.dump(out, open(os.path.join(DIR, "results7.json"), "w"), indent=1)
    print("\nresults7.json gravado.")


if __name__ == "__main__":
    main()
