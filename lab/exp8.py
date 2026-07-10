#!/usr/bin/env python3
"""Exp 8 — o vocabulário de modos: os eixos são modos naturais? PREREGISTRO-EXP8.md."""
import json
import os

import numpy as np

from exp6 import TENSE, build
from resonance import DIR, load_dataset


def unit(v):
    return v / np.linalg.norm(v)


def main():
    d, base = load_dataset()
    flex = [w for pair in TENSE for w in pair]
    words = base + [w for w in flex if w not in base]
    _, X_sem = build(words)
    idx = {w: i for i, w in enumerate(words)}

    v_int = unit(np.mean([X_sem[idx[a]] - X_sem[idx[b]]
                          for a, b in d["antonyms"]], axis=0))
    v_time = unit(np.mean([X_sem[idx[f]] - X_sem[idx[p]]
                           for p, f in TENSE], axis=0))

    excl = {w for pair in d["antonyms"] for w in pair} | set(flex)
    base_idx = [i for i, w in enumerate(words) if w not in excl]
    words_b = [words[i] for i in base_idx]
    Xb = X_sem[base_idx]
    Xc = Xb - Xb.mean(axis=0)
    _, Sv, Vt = np.linalg.svd(Xc, full_matrices=False)
    eig = Sv ** 2

    def top_frac(v, k=10):
        c = Vt @ v
        return float(np.sum(c[:k] ** 2))

    rng = np.random.default_rng(136)
    null = []
    for _ in range(500):
        pairs = rng.choice(len(words), size=(12, 2))
        dv = np.mean([X_sem[a] - X_sem[b] for a, b in pairs], axis=0)
        null.append(top_frac(unit(dv)))
    null = np.array(null)
    thr = float(np.percentile(null, 95))
    fi, ft = top_frac(v_int), top_frac(v_time)

    print(f"itens {len(words)} · PCA de {len(base_idx)} verbos neutros · "
          f"dims {X_sem.shape[1]}")
    print("\nG1 — os eixos são modos naturais? (fração da norma² nos 10 PCs de topo)")
    print(f"  intenção {fi:.3f} · tempo {ft:.3f}")
    print(f"  null (pares aleatórios): média {null.mean():.3f} · p95 {thr:.3f} "
          f"· direção pura ~ {10/X_sem.shape[1]:.3f}")
    print(f"  intenção > p95 e >= 0.40: "
          f"{'PASSA' if fi > thr and fi >= 0.40 else 'FALHA'}"
          f"  ·  tempo > p95 e >= 0.40: "
          f"{'PASSA' if ft > thr and ft >= 0.40 else 'FALHA'}")

    ci, ct = Vt @ v_int, Vt @ v_time
    print(f"  intenção mais parece PC{int(np.argmax(ci**2))+1} "
          f"(cos {ci[np.argmax(ci**2)]:+.2f}) · "
          f"tempo mais parece PC{int(np.argmax(ct**2))+1} "
          f"(cos {ct[np.argmax(ct**2)]:+.2f})")

    k = min(80, len(eig))
    x, y = np.log(np.arange(1, k + 1)), np.log(eig[:k])
    slope, inter = np.polyfit(x, y, 1)
    r2 = 1 - np.sum((y - (slope * x + inter)) ** 2) / np.sum((y - y.mean()) ** 2)
    print(f"\nG2 — espectro (PCs 1..{k}, EXPLORATÓRIO): expoente {-slope:.2f} · "
          f"R² {r2:.3f}  (referência córtex/Stringer ~1)")

    print("\nG3 — os modos próprios do espaço, lidos (extremos):")
    for pc in range(3):
        proj = Xc @ Vt[pc]
        order = np.argsort(-proj)
        pos = ", ".join(words_b[j] for j in order[:6])
        neg = ", ".join(words_b[j] for j in order[-6:][::-1])
        print(f"  PC{pc+1} ⊕ {pos}")
        print(f"       ⊖ {neg}")

    json.dump({"frac_int": fi, "frac_time": ft, "null_mean": float(null.mean()),
               "null_p95": thr, "slope": float(-slope), "r2": float(r2),
               "pc_int": int(np.argmax(ci ** 2)) + 1,
               "pc_time": int(np.argmax(ct ** 2)) + 1},
              open(os.path.join(DIR, "results8.json"), "w"), indent=1)
    print("\nresults8.json gravado.")


if __name__ == "__main__":
    main()
