#!/usr/bin/env python3
"""Exp 12 — a rua: o espectrômetro em reviews reais. PREREGISTRO-EXP12.md."""
import csv
import json
import os

import numpy as np

from exp11 import DATA, DIR, PAIRS12, embed, l2

MODEL, URL = "bge-m3", "http://localhost:11434"


def unit(v):
    return v / np.linalg.norm(v)


def main():
    z = np.load(os.path.join(DATA, "spectra_a.npz"), allow_pickle=False)
    W = list(z["words"])
    X = l2(z["X"].astype(np.float32))
    idx = {w: i for i, w in enumerate(W)}
    v12 = unit(np.mean([X[idx[a]] - X[idx[b]] for a, b in PAIRS12], axis=0))

    texts, labels = [], []
    with open(os.path.join(DATA, "lote_b2w.csv"), newline="",
              encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            labels.append(int(row["label"]))
    labels = np.array(labels)
    print(f"lote: {len(texts)} reviews reais (B2W) · eixo v12 do atlas")

    F = l2(embed(texts, MODEL, URL))
    proj = F @ v12

    def acc_of(p, lab):
        pred = np.where(p - np.median(p) >= 0, 1, -1)
        return float(np.mean(pred == lab))

    acc = acc_of(proj, labels)
    pos, neg = proj[labels == 1], proj[labels == -1]
    auc = float(np.mean([p > n for p in pos for n in neg]))

    rng = np.random.default_rng(136)
    null = []
    for _ in range(300):
        ids = rng.choice(len(W), size=24, replace=False)
        vv = unit(np.mean(X[ids[:12]] - X[ids[12:]], axis=0))
        null.append(acc_of(F @ vv, labels))
    p95 = float(np.percentile(null, 95))

    short = np.array([len(t) < 100 for t in texts])
    acc_s = acc_of(proj[short], labels[short]) if short.any() else 0.0
    acc_l = acc_of(proj[~short], labels[~short]) if (~short).any() else 0.0

    g1 = acc >= 0.80 and acc > p95
    print(f"\nG1 a rua : acurácia {100*acc:.1f}%  (gate >= 80% e > p95 null "
          f"{100*p95:.1f}%)  -> {'PASSA' if g1 else 'FALHA'}")
    print(f"  AUC {auc:.3f} · null médio {100*np.mean(null):.1f}% · "
          f"curtas {100*acc_s:.1f}% (n={int(short.sum())}) · "
          f"longas {100*acc_l:.1f}%")

    med = np.median(proj)
    errs = [(proj[j] - med, labels[j], texts[j]) for j in range(len(texts))
            if (proj[j] - med >= 0) != (labels[j] > 0)]
    errs.sort(key=lambda e: -abs(e[0]))
    print(f"\nerros: {len(errs)}/500 · os 5 mais confiantes (e errados):")
    for d, lab, t in errs[:5]:
        print(f"  {d:+.3f} [real {'5★' if lab > 0 else '1★'}] {t[:110]}")

    json.dump({"acc": acc, "auc": auc, "null_p95": p95,
               "acc_short": acc_s, "acc_long": acc_l,
               "n_errors": len(errs)},
              open(os.path.join(DIR, "results12.json"), "w"), indent=1)
    print("\nresults12.json gravado.")


if __name__ == "__main__":
    main()
