#!/usr/bin/env python3
"""Exp 6 — Chronos: o tempo como eixo operável. PREREGISTRO-EXP6.md."""
import json
import os

import numpy as np

import resonance
from resonance import DIR, load_dataset, l2, trigrams

resonance.MODEL = "bge-m3"
K_FORM = 50

TENSE = [
    ("amei", "amarei"), ("comprei", "comprarei"), ("ganhei", "ganharei"),
    ("vendi", "venderei"), ("comi", "comerei"), ("escrevi", "escreverei"),
    ("perdi", "perderei"), ("subi", "subirei"), ("abri", "abrirei"),
    ("dormi", "dormirei"), ("fiz", "farei"), ("fui", "irei"),
]
IRREG = {("fiz", "farei"), ("fui", "irei")}


def unit(v):
    return v / np.linalg.norm(v)


def build(words):
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
    return l2(Xc), l2(Xc - F50 @ B)


def run(tag, X, d, words):
    idx = {w: i for i, w in enumerate(words)}
    tpairs = [(idx[p], idx[f]) for p, f in TENSE]
    diffs = np.array([X[f] - X[p] for p, f in tpairs])
    v_int = unit(np.mean([X[idx[a]] - X[idx[b]] for a, b in d["antonyms"]],
                         axis=0))
    v_full = unit(diffs.mean(axis=0))
    s_full = float(np.mean(diffs @ v_full))
    rng = np.random.default_rng(136)
    v_rand = unit(rng.standard_normal(X.shape[1]))

    def rank_of(qv, tgt, exc):
        sims = X @ qv
        sims[exc] = -np.inf
        return int(np.where(np.argsort(-sims) == tgt)[0][0]) + 1

    acc = acc_r = 0
    rows = []
    for k, (p, f) in enumerate(tpairs):
        rest = np.delete(diffs, k, axis=0)
        v = unit(rest.mean(axis=0))
        s = float(np.mean(rest @ v))
        if X[f] @ v > X[p] @ v:
            acc += 1
        if X[f] @ v_rand > X[p] @ v_rand:
            acc_r += 1
        for src, tgt, sg in ((p, f, 1.0), (f, p, -1.0)):
            rows.append({
                "par": f"{words[src]}→{words[tgt]}",
                "irreg": (TENSE[k] in IRREG),
                "antes": rank_of(X[src].copy(), tgt, src),
                "depois": rank_of(unit(X[src] + sg * s * v), tgt, src),
                "rand": rank_of(unit(X[src] + sg * s * v_rand), tgt, src),
            })

    top5 = sum(1 for r in rows if r["depois"] <= 5)
    top5_rand = sum(1 for r in rows if r["rand"] <= 5)
    melhora = sum(1 for r in rows if r["depois"] < r["antes"])
    melhora_rand = sum(1 for r in rows if r["rand"] < r["antes"])
    med = lambda key: float(np.median([r[key] for r in rows]))
    print(f"\n[{tag}]")
    print(f"  G-T1 direção do tempo LOO: v_tempo {acc}/12 · aleatória {acc_r}/12")
    print(f"  G-T2 transplante: top-5 {top5}/24 (rand {top5_rand}/24) · "
          f"melhora {melhora}/24 (rand {melhora_rand}/24)")
    print(f"       ranks medianos: antes {med('antes'):.0f} · depois "
          f"{med('depois'):.0f} · rand {med('rand'):.0f}")
    for r in rows:
        if r["irreg"]:
            print(f"       irregular {r['par']}: antes {r['antes']} → "
                  f"depois {r['depois']} (rand {r['rand']})")
    ct = float(v_full @ v_int)
    print(f"  G-T3 ortogonalidade: cos(v_tempo, v_intenção) = {ct:+.3f} "
          f"(sanidade |cos(v_int, v_rand)| = {abs(float(v_int @ v_rand)):.3f})")

    def top(qv, exc, n=5):
        sims = X @ qv
        sims[exc] = -np.inf
        return [words[j] for j in np.argsort(-sims)[:n]]

    ia = idx["amei"]
    print(f"  demo amei+futuro   → {', '.join(top(unit(X[ia] + s_full*v_full), ia))}")
    ifu = idx["fui"]
    print(f"  demo fui+futuro    → {', '.join(top(unit(X[ifu] + s_full*v_full), ifu))}")
    iam = idx["amarei"]
    print(f"  demo amarei−futuro → {', '.join(top(unit(X[iam] - s_full*v_full), iam))}")
    return {"acc": acc, "acc_rand": acc_r, "top5": top5, "top5_rand": top5_rand,
            "melhora": melhora, "melhora_rand": melhora_rand,
            "med_antes": med("antes"), "med_depois": med("depois"),
            "med_rand": med("rand"), "cos_tempo_int": ct, "rows": rows}


def main():
    d, base = load_dataset()
    flex = [w for pair in TENSE for w in pair]
    words = base + [w for w in flex if w not in base]
    print(f"banco estendido: {len(words)} itens (227 infinitivos + flexões)")
    X_cent, X_sem = build(words)
    out = {"centrado": run("centrado (controle)", X_cent, d, words),
           "purificado": run("purificado (primário)", X_sem, d, words)}
    json.dump(out, open(os.path.join(DIR, "results6.json"), "w"), indent=1)
    print("\nresults6.json gravado.")


if __name__ == "__main__":
    main()
