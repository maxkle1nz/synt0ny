#!/usr/bin/env python3
"""Experimento pré-registrado: ressonância semântica de verbos. Ver PREREGISTRO.md."""
import json, math, os, random, time, urllib.request
import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
OLLAMA = "http://localhost:11434/api/embed"
MODEL = "bge-m3"
SEED = 136


def load_dataset():
    with open(os.path.join(DIR, "dataset.json")) as f:
        d = json.load(f)
    words = set(d["distractors"]) | set(d["polysemous"]) | set(d["specific"])
    for key in ("syn_distinct", "syn_shared", "antonyms", "paronyms"):
        for a, b in d[key]:
            words.add(a)
            words.add(b)
    return d, sorted(words)


def embed(texts):
    out = []
    for i in range(0, len(texts), 50):
        chunk = texts[i:i + 50]
        body = json.dumps({"model": MODEL, "input": chunk}).encode()
        req = urllib.request.Request(OLLAMA, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as r:
            out.extend(json.loads(r.read())["embeddings"])
    return np.array(out, dtype=np.float64)


def l2(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def trigrams(w):
    s = f"^{w}$"
    return [s[i:i + 3] for i in range(len(s) - 2)]


def char_sim(a, b):
    ta, tb = trigrams(a), trigrams(b)
    va = {}
    vb = {}
    for t in ta: va[t] = va.get(t, 0) + 1
    for t in tb: vb[t] = vb.get(t, 0) + 1
    dot = sum(va[t] * vb.get(t, 0) for t in va)
    na = math.sqrt(sum(v * v for v in va.values()))
    nb = math.sqrt(sum(v * v for v in vb.values()))
    return dot / (na * nb)


def cohens_d(x, y):
    nx, ny = len(x), len(y)
    sp = math.sqrt(((nx - 1) * np.var(x, ddof=1) + (ny - 1) * np.var(y, ddof=1)) / (nx + ny - 2))
    return (np.mean(x) - np.mean(y)) / sp


def perm_test(x, y, n=10000):
    rng = random.Random(SEED)
    obs = np.mean(x) - np.mean(y)
    pool = list(x) + list(y)
    k = len(x)
    hits = 0
    for _ in range(n):
        rng.shuffle(pool)
        if np.mean(pool[:k]) - np.mean(pool[k:]) >= obs:
            hits += 1
    return obs, (hits + 1) / (n + 1)


def hit_at_5(pairs, rank_fn):
    hits = total = 0
    for a, b in pairs:
        for q, t in ((a, b), (b, a)):
            total += 1
            if t in rank_fn(q)[:5]:
                hits += 1
    return hits / total


def main():
    d, words = load_dataset()
    idx = {w: i for i, w in enumerate(words)}
    n = len(words)
    print(f"banco: {n} verbos únicos")

    t0 = time.perf_counter()
    X = l2(embed(words))
    print(f"espectros: {X.shape[1]} dimensões por verbo, "
          f"gerados em {time.perf_counter()-t0:.1f}s")
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

    sim_syn = sims(d["syn_distinct"])
    sim_shared = sims(d["syn_shared"])
    sim_ant = sims(d["antonyms"])
    sim_par = sims(d["paronyms"])
    sim_rand = sims(rand_pairs)

    print("\n== H-R: separação (radical distinto vs aleatório) ==")
    obs, p = perm_test(sim_syn, sim_rand)
    d_eff = cohens_d(sim_syn, sim_rand)
    print(f"sinônimos {np.mean(sim_syn):.4f} vs aleatórios {np.mean(sim_rand):.4f}"
          f"  delta {obs:+.4f}  d = {d_eff:.2f}  p(perm) = {p:.5f}")
    print(f"estrato radical-compartilhado (informativo): {np.mean(sim_shared):.4f}")

    print("\n== H-B / C1' / C2: recuperação hit@5 (42 consultas) ==")
    order = np.argsort(-S, axis=1)

    def rank_emb(q):
        i = idx[q]
        return [words[j] for j in order[i] if j != i]

    ranks_char = {}

    def rank_char(q):
        if q not in ranks_char:
            ss = sorted(((char_sim(q, w), w) for w in words if w != q), reverse=True)
            ranks_char[q] = [w for _, w in ss]
        return ranks_char[q]

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
    chance = 5 / (n - 1)
    print(f"espectro completo : {100*h_emb:.1f}%")
    print(f"char-3gram (forma): {100*h_char:.1f}%")
    print(f"PCA-1 (1 freq.)   : {100*h_1d:.1f}%")
    print(f"acaso             : {100*chance:.1f}%")

    print("\n== H-F/PAR: parônimos (forma alta, sentido distante) ==")
    char_par = np.mean([char_sim(a, b) for a, b in d["paronyms"]])
    char_rand = np.mean([char_sim(a, b) for a, b in rand_pairs])
    print(f"forma (3gram): parônimos {char_par:.3f} vs aleatórios {char_rand:.3f}")
    print(f"ressonância  : parônimos {np.mean(sim_par):.4f} vs aleatórios "
          f"{np.mean(sim_rand):.4f}  (d = {cohens_d(sim_par, sim_rand):.2f})")

    print("\n== H-A: antônimos — dissonância ou afinação? ==")
    print(f"antônimos {np.mean(sim_ant):.4f} | sinônimos {np.mean(sim_syn):.4f} | "
          f"aleatórios {np.mean(sim_rand):.4f}")
    print(f"d(antônimos vs aleatórios) = {cohens_d(sim_ant, sim_rand):.2f}")

    print("\n== H-Q: fator Q (agudeza do pico de ressonância) ==")

    def q_factor(w):
        i = idx[w]
        s = np.delete(S[i], i)
        top5 = np.sort(s)[-5:]
        return (top5.mean() - np.median(s)) / s.std()

    q_spec = [q_factor(w) for w in d["specific"]]
    q_poly = [q_factor(w) for w in d["polysemous"]]
    u = sum(1.0 if a > b else 0.5 if a == b else 0.0 for a in q_spec for b in q_poly)
    mu, sg = 32.0, math.sqrt(64 * 17 / 12)
    z = (u - mu) / sg
    p_q = 0.5 * math.erfc(z / math.sqrt(2))
    print(f"Q específicos {np.mean(q_spec):.2f} vs polissêmicos {np.mean(q_poly):.2f}"
          f"  U = {u:.0f}  p = {p_q:.4f}")
    for w in sorted(d["specific"] + d["polysemous"], key=q_factor, reverse=True):
        tag = "esp" if w in d["specific"] else "poli"
        print(f"   Q = {q_factor(w):5.2f}  {w} ({tag})")

    print("\n== SANITY: determinismo e latência ==")
    X2 = l2(embed(words[:10]))
    dmax = float(np.max(np.abs(X2 - X[:10])))
    print(f"determinismo: max|delta| = {dmax:.2e} "
          f"({'OK' if dmax < 1e-6 else 'FALHOU'})")
    M = X.astype(np.float32)
    q = M[0]
    t0 = time.perf_counter()
    for _ in range(1000):
        M @ q
    t_mat = (time.perf_counter() - t0) / 1000 * 1e6
    L = [list(map(float, row)) for row in M]
    t0 = time.perf_counter()
    for row in L:
        sum(a * b for a, b in zip(row, q))
    t_ser = (time.perf_counter() - t0) * 1e3
    print(f"1 consulta × {n} verbos: matmul {t_mat:.0f} µs | serial {t_ser:.1f} ms "
          f"({t_ser*1000/t_mat:.0f}× mais lento)")

    json.dump({
        "n": n, "mean_syn": float(np.mean(sim_syn)),
        "mean_shared": float(np.mean(sim_shared)),
        "mean_ant": float(np.mean(sim_ant)), "mean_par": float(np.mean(sim_par)),
        "mean_rand": float(np.mean(sim_rand)), "d_syn": float(d_eff),
        "p_syn": p, "hit5_emb": h_emb, "hit5_char": h_char, "hit5_1d": h_1d,
        "chance": chance, "char_par": float(char_par), "char_rand": float(char_rand),
        "d_ant": float(cohens_d(sim_ant, sim_rand)),
        "q_spec": float(np.mean(q_spec)), "q_poly": float(np.mean(q_poly)),
        "p_q": p_q, "det_delta": dmax, "us_matmul": t_mat, "ms_serial": t_ser,
    }, open(os.path.join(DIR, "results3.json"), "w"), indent=1)
    print("\nresults3.json gravado.")


if __name__ == "__main__":
    main()
