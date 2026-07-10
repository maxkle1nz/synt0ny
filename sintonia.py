#!/usr/bin/env python3
"""sintonia — busca semântica por ressonância + eixo da intenção (pt-BR).

Consolidação dos Experimentos 1-6 (ver lab/): espectros bge-m3, espaço
purificado de forma (firmamento, k=50) e eixo da intenção (12 antônimos).
Uso:
  sintonia.py buscar <verbo>      vizinhos por ressonância (zero-shot)
  sintonia.py intencao <verbo>... posição no eixo da intenção
  sintonia.py eixo                extremos do eixo no banco
"""
import json
import os
import sys
import urllib.request

import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(DIR, "cache.npz")
OLLAMA = "http://localhost:11434/api/embed"
MODEL = "bge-m3"
K_FORM = 50

DIM = "\033[2m"
BOLD = "\033[1m"
TEAL = "\033[38;5;72m"
CORAL = "\033[38;5;173m"
R = "\033[0m"


def embed(texts):
    out = []
    for i in range(0, len(texts), 50):
        body = json.dumps({"model": MODEL, "input": texts[i:i + 50]}).encode()
        req = urllib.request.Request(OLLAMA, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            out.extend(json.loads(r.read())["embeddings"])
    return np.array(out, dtype=np.float64)


def l2(X):
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def trigrams(w):
    s = f"^{w}$"
    return [s[i:i + 3] for i in range(len(s) - 2)]


def build():
    print(f"{DIM}primeira execução: construindo os espectros…{R}")
    with open(os.path.join(DIR, "lab", "dataset.json")) as f:
        d = json.load(f)
    words = set(d["distractors"]) | set(d["polysemous"]) | set(d["specific"])
    for key in ("syn_distinct", "syn_shared", "antonyms", "paronyms"):
        for a, b in d[key]:
            words.add(a)
            words.add(b)
    words = sorted(words)
    X = l2(embed(words))
    mean_x = X.mean(axis=0)
    vocab = sorted({t for w in words for t in trigrams(w)})
    tix = {t: j for j, t in enumerate(vocab)}
    F = np.zeros((len(words), len(vocab)))
    for i, w in enumerate(words):
        for t in trigrams(w):
            F[i, tix[t]] += 1
    f_mean = F.mean(axis=0)
    _, _, Vt = np.linalg.svd(F - f_mean, full_matrices=False)
    V50 = Vt[:K_FORM].T
    F50 = (F - f_mean) @ V50
    Xc = X - mean_x
    B, *_ = np.linalg.lstsq(F50, Xc, rcond=None)
    X_sem = l2(Xc - F50 @ B)
    idx = {w: i for i, w in enumerate(words)}
    v_int = X_sem[[idx[a] for a, _ in d["antonyms"]]].mean(axis=0) \
        - X_sem[[idx[b] for _, b in d["antonyms"]]].mean(axis=0)
    v_int = v_int / np.linalg.norm(v_int)
    np.savez(CACHE, words=np.array(words), X_sem=X_sem, mean_x=mean_x,
             f_mean=f_mean, V50=V50, B=B, v_int=v_int,
             vocab=np.array(vocab), proj=X_sem @ v_int)
    print(f"{DIM}{len(words)} verbos · {X.shape[1]} dims · cache salvo{R}")


def load():
    if not os.path.exists(CACHE):
        build()
    z = np.load(CACHE, allow_pickle=False)
    return z


def spectrum(z, w):
    words = list(z["words"])
    if w in words:
        return z["X_sem"][words.index(w)], True
    x = l2(embed([w]))[0] - z["mean_x"]
    tix = {t: j for j, t in enumerate(list(z["vocab"]))}
    f = np.zeros(len(tix))
    for t in trigrams(w):
        if t in tix:
            f[tix[t]] += 1
    f50 = (f - z["f_mean"]) @ z["V50"]
    x = x - f50 @ z["B"]
    return x / np.linalg.norm(x), False


def bar(frac, width=22):
    n = round(max(0.0, min(1.0, frac)) * width)
    return "█" * n + f"{DIM}" + "░" * (width - n) + R


def cmd_buscar(w):
    z = load()
    q, known = spectrum(z, w)
    tag = "" if known else f" {DIM}(fora do banco — zero-shot){R}"
    print(f"\n{BOLD}{w}{R} ressoa com:{tag}")
    sims = z["X_sem"] @ q
    words = list(z["words"])
    if known:
        sims[words.index(w)] = -np.inf
    lo, hi = 0.0, float(np.max(sims))
    for j in np.argsort(-sims)[:10]:
        s = float(sims[j])
        print(f"  {TEAL}{bar((s - lo) / (hi - lo + 1e-9))}{R} "
              f"{s:+.3f}  {words[j]}")


def cmd_intencao(targets):
    z = load()
    lo, hi = float(z["proj"].min()), float(z["proj"].max())
    print(f"\n{DIM}eixo da intenção · ⊖ dissipação{'—' * 30}acréscimo ⊕{R}")
    for w in targets:
        q, known = spectrum(z, w)
        p = float(q @ z["v_int"])
        frac = (p - lo) / (hi - lo)
        pct = 100.0 * float((z["proj"] < p).mean())
        col = TEAL if frac >= 0.5 else CORAL
        star = "" if known else f" {DIM}·zero-shot{R}"
        print(f"  {col}{bar(frac, 30)}{R} {p:+.3f} "
              f"{DIM}(percentil {pct:.0f}){R}  {BOLD}{w}{R}{star}")


def cmd_eixo():
    z = load()
    words, proj = list(z["words"]), z["proj"]
    order = np.argsort(-proj)
    print(f"\n{BOLD}⊕ acréscimo{R}")
    for j in order[:8]:
        print(f"  {TEAL}{proj[j]:+.3f}{R}  {words[j]}")
    print(f"{BOLD}⊖ dissipação{R}")
    for j in order[-8:][::-1]:
        print(f"  {CORAL}{proj[j]:+.3f}{R}  {words[j]}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["buscar"] and len(args) == 2:
        cmd_buscar(args[1])
    elif args[:1] == ["intencao"] and len(args) >= 2:
        cmd_intencao(args[1:])
    elif args == ["eixo"]:
        cmd_eixo()
    else:
        print(__doc__)
