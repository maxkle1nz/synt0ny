#!/usr/bin/env python3
"""Exp 11 — o atlas (v2, pós-verdict fable). PREREGISTRO-EXP11.md.

Uso:
  exp11.py embed a|b      gera atlas/data/spectra_<i>.npz (o léxico inteiro)
  exp11.py analyze a|b    roda E1-E4 e grava results11_<i>.json
Instrumento B: export OLLAMA_URL=http://localhost:11435 (túnel ssh p/ GENESIS).
"""
import json
import os
import re
import sys
import time
import urllib.request
from math import erfc, sqrt

import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(DIR, "data")
SEED = 136
INSTR = {"a": ("bge-m3", "http://localhost:11434"),
         "b": ("qwen3-embedding:8b",
               os.environ.get("OLLAMA_URL", "http://localhost:11435"))}
PAIRS12 = [("subir", "descer"), ("abrir", "fechar"), ("entrar", "sair"),
           ("comprar", "vender"), ("ganhar", "perder"), ("amar", "odiar"),
           ("nascer", "morrer"), ("chegar", "partir"), ("ligar", "desligar"),
           ("aceitar", "recusar"), ("lembrar", "esquecer"),
           ("construir", "destruir")]


def load_lexicon():
    own = {}
    for line in open(os.path.join(DATA, "wn-data-por.tab"), encoding="utf-8"):
        if line.startswith("#"):
            continue
        p = line.rstrip("\n").split("\t")
        if len(p) == 3 and p[1] == "lemma":
            own.setdefault(p[2], set()).add(p[0])
    tep_groups = {}
    tep_ant = set()
    tep_count = {}
    for line in open(os.path.join(DATA, "tep_layout_one.txt"), encoding="utf-8"):
        m = re.match(r"\s*(\d+)\.\s*\[(\w+)\]\s*\{([^}]*)\}\s*(?:<(\d+)>)?", line)
        if not m:
            continue
        gid, cat, syns, ant = m.groups()
        ws = [w.strip() for w in syns.split(",") if w.strip()]
        tep_groups[int(gid)] = (cat, ws)
        for w in ws:
            tep_count[w] = tep_count.get(w, 0) + 1
        if ant:
            a, b = int(gid), int(ant)
            tep_ant.add((min(a, b), max(a, b)))
    words = sorted(set(own) | set(tep_count))
    senses = {w: len(own[w]) if w in own else tep_count.get(w, 1) for w in words}
    return words, senses, tep_groups, sorted(tep_ant)


def embed(texts, model, url):
    out = []
    for i in range(0, len(texts), 50):
        body = json.dumps({"model": model, "input": texts[i:i + 50]}).encode()
        req = urllib.request.Request(f"{url}/api/embed", data=body,
                                     headers={"Content-Type": "application/json"})
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    out.extend(json.loads(r.read())["embeddings"])
                break
            except Exception as e:
                if attempt == 2:
                    raise
                print(f"  retry {i}: {e}", flush=True)
                time.sleep(5)
        if i % 5000 == 0:
            print(f"  {i}/{len(texts)}", flush=True)
    return np.array(out, dtype=np.float32)


def l2(X):
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def cmd_embed(inst):
    model, url = INSTR[inst]
    words, *_ = load_lexicon()
    print(f"instrumento {inst.upper()} = {model} @ {url} · {len(words)} lemas")
    t0 = time.perf_counter()
    X = embed(words, model, url)
    dt = time.perf_counter() - t0
    np.savez(os.path.join(DATA, f"spectra_{inst}.npz"),
             words=np.array(words), X=X)
    print(f"ok: {X.shape} em {dt/60:.1f} min ({len(words)/dt:.0f} p/s)")


def rank_avg(v):
    """Ranks médios em empates (fix fable #2)."""
    order = np.argsort(v, kind="mergesort")
    sv = v[order]
    _, inv, counts = np.unique(sv, return_inverse=True, return_counts=True)
    ends = np.cumsum(counts) - 1.0
    starts = ends - (counts - 1)
    avg = (starts + ends) / 2.0
    out = np.empty(len(v))
    out[order] = avg[inv]
    return out


def partial_spearman(x, y, z):
    rx, ry, rz = rank_avg(x), rank_avg(y), rank_avg(z)

    def corr(a, b):
        a = a - a.mean()
        b = b - b.mean()
        return float(a @ b / np.sqrt((a @ a) * (b @ b)))

    rxy, rxz, ryz = corr(rx, ry), corr(rx, rz), corr(ry, rz)
    rp = (rxy - rxz * ryz) / np.sqrt((1 - rxz**2) * (1 - ryz**2))
    pval = erfc(abs(rp * np.sqrt(len(x) - 3)) / sqrt(2))
    return rp, rxy, pval


def cmd_analyze(inst):
    from wordfreq import zipf_frequency
    words, senses, tep_groups, tep_ant = load_lexicon()
    z = np.load(os.path.join(DATA, f"spectra_{inst}.npz"), allow_pickle=False)
    W = list(z["words"])
    X = l2(z["X"].astype(np.float32))
    X = l2(X - X.mean(axis=0))
    idx = {w: i for i, w in enumerate(W)}
    rng = np.random.default_rng(SEED)
    res = {"instrument": inst, "n": len(W)}
    v12 = l2(np.mean([X[idx[a]] - X[idx[b]] for a, b in PAIRS12], axis=0)
             .astype(np.float64)).astype(np.float32)

    gmeans = {}
    for gid, (cat, ws) in tep_groups.items():
        ids = [idx[w] for w in ws if w in idx]
        if ids:
            gmeans[gid] = l2(X[ids].mean(axis=0))
    rels_by_cat = {}
    for a, b in tep_ant:
        if a in gmeans and b in gmeans and a in tep_groups:
            rels_by_cat.setdefault(tep_groups[a][0], []).append((a, b))

    print(f"[{inst.upper()}] E1 — antonímias externas (TeP)")

    def frac_opposite(rels, v):
        opp = sum(1 for a, b in rels
                  if (gmeans[a] @ v) * (gmeans[b] @ v) < 0)
        return opp / len(rels) if rels else 0.0

    for cat, rels in sorted(rels_by_cat.items()):
        res[f"e1_{cat}"] = frac_opposite(rels, v12)
        res[f"e1_{cat}_n"] = len(rels)
        print(f"  {cat:10s}: {res[f'e1_{cat}']:.3f} (n={len(rels)})")
    verb_rels = rels_by_cat.get("VERB", [])
    gsize = lambda g: len([w for w in tep_groups[g][1] if w in idx])
    res["e1_size1_frac"] = float(np.mean([gsize(g) == 1
                                          for r in verb_rels for g in r]))
    big = [(a, b) for a, b in verb_rels if gsize(a) >= 2 and gsize(b) >= 2]
    res["e1_VERB_size2"] = frac_opposite(big, v12)
    res["e1_VERB_size2_n"] = len(big)
    null = []
    for _ in range(300):
        ids = rng.choice(len(W), size=24, replace=False)
        vv = l2(np.mean(X[ids[:12]] - X[ids[12:]], axis=0))
        null.append(frac_opposite(verb_rels, vv))
    res["e1_null_p95"] = float(np.percentile(null, 95))
    vlem = sorted({w for _, (c, ws) in tep_groups.items() if c == "VERB"
                   for w in ws if w in idx})
    vids = np.array([idx[w] for w in vlem])
    null2 = []
    for _ in range(300):
        ids = rng.choice(len(vids), size=24, replace=False)
        vv = l2(np.mean(X[vids[ids[:12]]] - X[vids[ids[12:]]], axis=0))
        null2.append(frac_opposite(verb_rels, vv))
    res["e1_null2_p95"] = float(np.percentile(null2, 95))
    g1 = (res["e1_VERB"] >= 0.75 and res["e1_VERB"] > res["e1_null_p95"]
          and res["e1_VERB"] > res["e1_null2_p95"])
    print(f"  grupos size=1: {100*res['e1_size1_frac']:.0f}% · "
          f"só grupos>=2: {res['e1_VERB_size2']:.3f} (n={len(big)})")
    print(f"  GATE E1: {res['e1_VERB']:.3f} vs null-lemas p95 "
          f"{res['e1_null_p95']:.3f} e null-verbos p95 "
          f"{res['e1_null2_p95']:.3f} e >= 0.75 -> "
          f"{'PASSA' if g1 else 'FALHA'}")

    held = [verb_rels[i] for i in
            rng.choice(len(verb_rels), size=12, replace=False)]
    test_rels = [r for r in verb_rels if r not in held]
    D = np.array([gmeans[a] - gmeans[b] for a, b in held])
    _, _, Vd = np.linalg.svd(D - D.mean(0), full_matrices=False)
    v_tep = Vd[0].astype(np.float32)
    res["e1_vtep_VERB"] = frac_opposite(test_rels, v_tep)
    print(f"  eixo secundário v_tep (held-out): "
          f"{res['e1_vtep_VERB']:.3f} (n={len(test_rels)}) — replica o v12?")

    print(f"[{inst.upper()}] E2 — modos (PCA no léxico INTEIRO)")
    Xc = X - X.mean(axis=0)
    _, Sv, Vt = np.linalg.svd(Xc, full_matrices=False)
    c = Vt @ v12
    res["e2_topfrac"] = float(np.sum(c[:10] ** 2))
    nullf = []
    for _ in range(300):
        ids = rng.choice(len(W), size=24, replace=False)
        vv = l2(np.mean(X[ids[:12]] - X[ids[12:]], axis=0))
        nullf.append(float(np.sum((Vt @ vv)[:10] ** 2)))
    res["e2_null_p95"] = float(np.percentile(nullf, 95))
    eig = Sv.astype(np.float64) ** 2
    lx, ly = np.log(np.arange(1, 201)), np.log(eig[:200])
    res["e2_exponent"] = float(-np.polyfit(lx, ly, 1)[0])
    print(f"  top_frac(v12) {res['e2_topfrac']:.3f} vs p95 "
          f"{res['e2_null_p95']:.3f} · expoente {res['e2_exponent']:.2f}")
    for pc in range(5):
        proj = Xc @ Vt[pc]
        o = np.argsort(-proj)
        res[f"e2_pc{pc+1}_pos"] = [W[j] for j in o[:10]]
        res[f"e2_pc{pc+1}_neg"] = [W[j] for j in o[-10:][::-1]]
        print(f"  PC{pc+1} ⊕ {', '.join(res[f'e2_pc{pc+1}_pos'][:6])}")
        print(f"      ⊖ {', '.join(res[f'e2_pc{pc+1}_neg'][:6])}")

    print(f"[{inst.upper()}] E3 — Q × polissemia (rank médio + bootstrap)")
    samp = rng.choice(len(W), size=5000, replace=False)
    in_samp = np.zeros(len(W), dtype=bool)
    in_samp[samp] = True
    S = X @ X[samp].T
    Ssort = np.sort(S, axis=1)
    top5 = np.where(in_samp, Ssort[:, -6:-1].mean(axis=1),
                    Ssort[:, -5:].mean(axis=1))
    q = (top5 - np.median(S, axis=1)) / S.std(axis=1)
    ns = np.array([senses[w] for w in W], dtype=float)
    fr = np.array([zipf_frequency(w, "pt") for w in W])
    rp, rraw, pval = partial_spearman(ns, q, fr)
    boots = []
    for _ in range(300):
        bi = rng.integers(0, len(W), size=len(W))
        boots.append(partial_spearman(ns[bi], q[bi], fr[bi])[0])
    lo, hi = np.percentile(boots, [2.5, 97.5])
    mask_fr = fr > 0
    rp_fr = partial_spearman(ns[mask_fr], q[mask_fr], fr[mask_fr])[0]
    mask_sw = np.array([" " not in w for w in W]) & mask_fr
    rp_sw = partial_spearman(ns[mask_sw], q[mask_sw], fr[mask_sw])[0]
    res.update(e3_rho_partial=float(rp), e3_rho_raw=float(rraw),
               e3_p=float(pval), e3_ci=[float(lo), float(hi)],
               e3_zipf_zero_frac=float((fr == 0).mean()),
               e3_rho_fr_pos=float(rp_fr), e3_rho_single_word=float(rp_sw))
    g3 = rp <= -0.10 and pval < 0.001 and hi < -0.05 and rp_fr <= -0.10
    print(f"  rho bruto {rraw:+.3f} · parcial {rp:+.3f} "
          f"IC95 [{lo:+.3f},{hi:+.3f}] · zipf=0 em {100*(fr==0).mean():.0f}%")
    print(f"  sensibilidade fr>0: {rp_fr:+.3f} · 1-palavra e fr>0: "
          f"{rp_sw:+.3f} -> {'PASSA' if g3 else 'FALHA'}")
    np.savez(os.path.join(DATA, f"analysis_{inst}.npz"),
             q=q, proj=X @ v12, fr=fr, ns=ns)

    print(f"[{inst.upper()}] E4 — hubness (amostra 5k; subestima o fenômeno)")
    Ss = X[samp] @ X[samp].T
    np.fill_diagonal(Ss, -np.inf)
    top10 = np.argsort(-Ss, axis=1)[:, :10]
    kocc = np.bincount(top10.ravel(), minlength=5000).astype(float)
    res["e4_skew"] = float(((kocc - kocc.mean()) ** 3).mean() / kocc.std() ** 3)
    res["e4_hubs"] = [W[samp[j]] for j in np.argsort(-kocc)[:10]]
    print(f"  skewness {res['e4_skew']:.2f} · hubs: "
          f"{', '.join(res['e4_hubs'][:6])}")

    json.dump(res, open(os.path.join(DIR, f"results11_{inst}.json"), "w"),
              indent=1, ensure_ascii=False)
    print(f"results11_{inst}.json gravado.")


def gates_of(r):
    e1 = (r["e1_VERB"] >= 0.75 and r["e1_VERB"] > r["e1_null_p95"]
          and r["e1_VERB"] > r["e1_null2_p95"])
    e3 = (r["e3_rho_partial"] <= -0.10 and r["e3_p"] < 0.001
          and r["e3_ci"][1] < -0.05 and r["e3_rho_fr_pos"] <= -0.10)
    return e1, e3


def cmd_compare():
    ra = json.load(open(os.path.join(DIR, "results11_a.json")))
    rb = json.load(open(os.path.join(DIR, "results11_b.json")))
    za = np.load(os.path.join(DATA, "analysis_a.npz"))
    zb = np.load(os.path.join(DATA, "analysis_b.npz"))

    def spear(x, y):
        rx, ry = rank_avg(x), rank_avg(y)
        rx = rx - rx.mean()
        ry = ry - ry.mean()
        return float(rx @ ry / np.sqrt((rx @ rx) * (ry @ ry)))

    conc_q = spear(za["q"], zb["q"])
    conc_p = spear(za["proj"], zb["proj"])
    out = {"concord_q": conc_q, "concord_proj": conc_p}
    print(f"concordância inter-instrumento: Q {conc_q:+.3f} · "
          f"proj(v12) {conc_p:+.3f} (redundância dos encoders)")
    for name in ("E1", "E3"):
        pa, pb = gates_of(ra)[name == "E3"], gates_of(rb)[name == "E3"]
        label = ("GEOMETRIA DA LÍNGUA (nos limites declarados)" if pa and pb
                 else f"idiossincrasia (só {'A' if pa else 'B'})"
                 if pa != pb else "não estabelecido")
        out[name] = {"a": bool(pa), "b": bool(pb), "label": label}
        print(f"{name}: A {'✓' if pa else '✗'} · B {'✓' if pb else '✗'} → {label}")
    json.dump(out, open(os.path.join(DIR, "results11_compare.json"), "w"),
              indent=1, ensure_ascii=False)
    print("results11_compare.json gravado.")


if __name__ == "__main__":
    if sys.argv[1:3] and sys.argv[1] == "embed" and sys.argv[2] in INSTR:
        cmd_embed(sys.argv[2])
    elif sys.argv[1:3] and sys.argv[1] == "analyze" and sys.argv[2] in INSTR:
        cmd_analyze(sys.argv[2])
    elif sys.argv[1:2] == ["compare"]:
        cmd_compare()
    else:
        print(__doc__)
