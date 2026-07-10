#!/usr/bin/env python3
"""Exp 14 — o radar de commits (v2 pós-verdict). PREREGISTRO-EXP14.md."""
import json
import os
import re
import subprocess

import numpy as np

from exp13 import embed, l2

DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 136
K_LADDER = [20, 10, 5, 3]
BASE_RANGE = (0.10, 0.40)
FIX_RE = re.compile(r"\b(fix|revert|hotfix|regress)", re.I)

RISKY = [
    "rewrite the core scheduler locking model",
    "migrate database schema to new format",
    "refactor auth flow across all handlers",
    "change default behavior of the cache layer",
    "swap serialization format for persisted state",
    "rework concurrency in the ingest pipeline",
    "replace the dependency resolution algorithm",
    "change public api signatures for all verbs",
    "rewrite path normalization logic",
    "overhaul error handling in the daemon",
    "switch to a new embedding backend",
    "restructure the storage layout on disk",
]
COSMETIC = [
    "fix typo in readme",
    "update comment wording",
    "bump version string",
    "add missing docstring",
    "rename internal variable for clarity",
    "update changelog entries",
    "adjust log message formatting",
    "add badge to readme",
    "remove unused import",
    "tweak ci badge link",
    "reorder imports alphabetically",
    "fix markdown table alignment",
]


def unit(v):
    return v / np.linalg.norm(v)


def collect(repo):
    raw = subprocess.run(
        ["git", "-C", repo, "log", "--no-merges", "--first-parent",
         "--reverse", "--format=%x02%H%x01%s", "--name-only"],
        capture_output=True, text=True, timeout=120).stdout
    commits = []
    for block in raw.split("\x02"):
        if not block.strip():
            continue
        head, _, files_blob = block.partition("\n")
        sha, _, subject = head.partition("\x01")
        files = {f.strip() for f in files_blob.splitlines() if f.strip()}
        if subject.strip():
            commits.append((sha, subject.strip(), files))
    return commits


def label(commits, k):
    labels = []
    for i, (_, _, files) in enumerate(commits):
        succ = commits[i + 1:i + 1 + k]
        if len(succ) < k:
            labels.append(None)
            continue
        hit = any(FIX_RE.search(s) and files & f for _, s, f in succ)
        labels.append(1 if hit else 0)
    return labels


def pick_k(commits):
    """Sanity selado: calibra o PROXY (antes de qualquer embedding)."""
    for k in K_LADDER:
        labels = label(commits, k)
        ys = [x for x in labels if x is not None]
        base = sum(ys) / len(ys) if ys else 0.0
        if BASE_RANGE[0] <= base <= BASE_RANGE[1]:
            return k, labels, base
    return None, None, base


def rank_avg(v):
    order = np.argsort(v, kind="mergesort")
    sv = np.asarray(v, dtype=float)[order]
    _, inv, counts = np.unique(sv, return_inverse=True, return_counts=True)
    ends = np.cumsum(counts) - 1.0
    starts = ends - (counts - 1)
    out = np.empty(len(v))
    out[order] = ((starts + ends) / 2.0)[inv]
    return out


def corr(a, b):
    a = a - a.mean()
    b = b - b.mean()
    return float(a @ b / np.sqrt((a @ a) * (b @ b)))


def partial_multi(x, y, Z):
    """Parcial de Spearman de x~y controlando as colunas de Z (ranks+OLS)."""
    rx, ry = rank_avg(x), rank_avg(y)
    RZ = np.column_stack([rank_avg(z) for z in Z] + [np.ones(len(x))])
    bx, *_ = np.linalg.lstsq(RZ, rx, rcond=None)
    by, *_ = np.linalg.lstsq(RZ, ry, rcond=None)
    return corr(rx - RZ @ bx, ry - RZ @ by)


def auc(pos, neg):
    # empates contam como derrota (viés conservador, declarado)
    return float(np.mean([p > n for p in pos for n in neg]))


def evaluate(name, repo, v, rng, gate=False):
    commits = collect(repo)
    k, labels, base0 = pick_k(commits)
    if k is None:
        print(f"[{name}] PROXY INVIÁVEL: taxa-base {base0:.1%} fora de "
              f"{BASE_RANGE} em toda a escada K — corpus não avaliado")
        return {"proxy": "inviável", "base_rate": base0}
    keep = [(c, l) for c, l in zip(commits, labels) if l is not None]
    if len(keep) < 40:
        print(f"[{name}] corpus pequeno ({len(keep)}) — pulado")
        return None
    subjects = [c[1] for c, _ in keep]
    y = np.array([l for _, l in keep])
    nfiles = np.array([len(c[2]) for c, _ in keep], dtype=float)
    freq = {}
    for c, _ in keep:
        for f in c[2]:
            freq[f] = freq.get(f, 0) + 1
    hot = np.array([max((freq[f] for f in c[2]), default=1)
                    for c, _ in keep], dtype=float)
    E = l2(embed(subjects))
    proj = E @ v
    base = float(y.mean())
    a = auc(proj[y == 1], proj[y == 0])
    out = {"n": len(keep), "k_next": k, "base_rate": base, "auc": a}
    print(f"[{name}] n={len(keep)} · K={k} · base {base:.1%} · AUC {a:.3f}",
          end="")
    if gate:
        null = []
        for _ in range(300):
            ids = rng.choice(len(subjects), size=24, replace=False)
            vv = unit(E[ids[:12]].mean(0) - E[ids[12:]].mean(0))
            p = E @ vv
            null.append(auc(p[y == 1], p[y == 0]))
        p95 = float(np.percentile(null, 95))
        top20 = np.argsort(-proj)[:20]
        prec = float(y[top20].mean())
        rxy = corr(rank_avg(proj), rank_avg(y))
        rp = partial_multi(proj, y, [np.log1p(nfiles), np.log1p(hot)])
        nofix = np.array([not FIX_RE.search(s) for s in subjects])
        a_nofix = auc(proj[(y == 1) & nofix], proj[(y == 0) & nofix]) \
            if ((y == 1) & nofix).any() and ((y == 0) & nofix).any() else None
        g1 = a >= 0.65 and a > p95
        g2 = prec >= 1.5 * base
        s1 = (rp > 0) == (rxy > 0) and abs(rp) >= 0.5 * abs(rxy)
        print(f"\n  G1: AUC {a:.3f} vs p95 null {p95:.3f} e >= 0.65 -> "
              f"{'PASSA' if g1 else 'FALHA'}")
        print(f"  G2: precision@20 {prec:.1%} vs 1.5×base {1.5*base:.1%} -> "
              f"{'PASSA' if g2 else 'FALHA'}")
        print(f"  S1: rho {rxy:+.3f} → parcial (|n_files,hot) {rp:+.3f} "
              f"(gate: mesmo sinal e >= 50% de {abs(rxy):.3f}) -> "
              f"{'PASSA' if s1 else 'FALHA'}")
        print(f"  S2 (sem self-fix, informativo): AUC "
              f"{a_nofix:.3f}" if a_nofix is not None else
              "  S2: estrato insuficiente")
        top5 = np.argsort(-proj)[:5]
        print("  top-5 risky previstos:")
        for j in top5:
            print(f"    [{'FIX-SEGUIDO' if y[j] else 'limpo      '}] "
                  f"{subjects[j][:70]}")
        out.update(null_p95=p95, prec20=prec, rho=rxy, rho_partial=float(rp),
                   auc_no_selffix=a_nofix, g1=bool(g1), g2=bool(g2),
                   s1=bool(s1))
    else:
        print()
    return out


def main():
    rng = np.random.default_rng(SEED)
    E_ex = l2(embed(RISKY + COSMETIC))
    v = unit(E_ex[:12].mean(0) - E_ex[12:].mean(0))
    res = {}
    res["m1nd"] = evaluate("m1nd (GATE)", os.path.expanduser("~/m1nd"),
                           v, rng, gate=True)
    for name, path in (("l00p", "~/l00p"), ("synt0ny", "~/synt0ny"),
                       ("cherry-IT", "~/CHERRYBUBBLES/Cherrybubbles1")):
        res[name] = evaluate(name, os.path.expanduser(path), v, rng)
    json.dump(res, open(os.path.join(DIR, "results14.json"), "w"), indent=1)
    print("\nresults14.json gravado.")


if __name__ == "__main__":
    main()
