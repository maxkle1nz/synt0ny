#!/usr/bin/env python3
"""Exp 15 — tipo de commit (feat↔fix) vs prefixos conventional.
PREREGISTRO-EXP15.md."""
import json
import os
import re
import subprocess

import numpy as np

from exp13 import embed, l2

DIR = os.path.dirname(os.path.abspath(__file__))
SEED = 136
PREFIX_RE = re.compile(r"^(feat|fix)(\([^)]*\))?[:!]\s*(.+)$")

FEAT = [
    "add streaming support to the export pipeline",
    "introduce per-project configuration overrides",
    "support multiple output formats in the report",
    "implement incremental cache invalidation",
    "add retry with backoff to network calls",
    "new command to inspect live sessions",
    "enable parallel ingestion of large corpora",
    "add dark mode to the dashboard",
    "introduce plugin discovery at startup",
    "support custom seed in the sampler",
    "add health endpoint for the daemon",
    "implement rolling log rotation",
]
FIX = [
    "resolve crash when the config file is empty",
    "correct off by one in the pagination window",
    "handle unicode paths on windows",
    "prevent duplicate entries after retry",
    "restore backward compatibility with old manifests",
    "avoid deadlock when two writers race",
    "patch memory leak in the watcher loop",
    "correct timezone handling in timestamps",
    "guard against empty response from the api",
    "stop double counting cached results",
    "repair broken links in generated docs",
    "close file handles on early return",
]


def unit(v):
    return v / np.linalg.norm(v)


def auc(pos, neg):
    return float(np.mean([p > n for p in pos for n in neg]))


def corpus(repo):
    subjects = subprocess.run(
        ["git", "-C", os.path.expanduser(repo), "log", "--no-merges",
         "--format=%s"], capture_output=True, text=True, timeout=60
    ).stdout.splitlines()
    texts, labels = [], []
    for s in subjects:
        m = PREFIX_RE.match(s.strip())
        if not m:
            continue
        desc = m.group(3).strip()
        if len(desc) >= 8:
            texts.append(desc)
            labels.append(1 if m.group(1) == "feat" else 0)
    return texts, np.array(labels)


def main():
    rng = np.random.default_rng(SEED)
    E_ex = l2(embed(FEAT + FIX))
    v = unit(E_ex[:12].mean(0) - E_ex[12:].mean(0))

    texts, y = corpus("~/m1nd")
    print(f"[m1nd] corpus: {len(texts)} · feat {int(y.sum())} · "
          f"fix {int((1-y).sum())}")
    E = l2(embed(texts))
    proj = E @ v
    a = auc(proj[y == 1], proj[y == 0])
    null = []
    for _ in range(300):
        ids = rng.choice(len(texts), size=24, replace=False)
        vv = unit(E[ids[:12]].mean(0) - E[ids[12:]].mean(0))
        p = E @ vv
        null.append(auc(p[y == 1], p[y == 0]))
    p95 = float(np.percentile(null, 95))
    base_fix = float((1 - y).mean())
    top20fix = np.argsort(proj)[:20]
    prec = float((1 - y[top20fix]).mean())
    g1 = a >= 0.80 and a > p95
    g2 = prec >= 1.5 * base_fix
    print(f"G1: AUC {a:.3f} (gate >= 0.80 e > p95 null {p95:.3f}) -> "
          f"{'PASSA' if g1 else 'FALHA'}")
    print(f"G2: precision@20 (fix) {prec:.1%} vs 1.5×base {1.5*base_fix:.1%}"
          f" -> {'PASSA' if g2 else 'FALHA'}")
    errs = [(proj[j], texts[j], y[j]) for j in range(len(texts))
            if (proj[j] >= np.median(proj)) != (y[j] == 1)]
    errs.sort(key=lambda e: -abs(e[0] - float(np.median(proj))))
    print("erros mais confiantes:")
    for p, t, lab in errs[:4]:
        print(f"  [{'feat' if lab else 'fix '}] {t[:70]}")

    res = {"m1nd": {"n": len(texts), "auc": a, "null_p95": p95,
                    "prec20_fix": prec, "g1": bool(g1), "g2": bool(g2)}}
    for repo in ("~/l00p", "~/synt0ny"):
        t2, y2 = corpus(repo)
        if len(t2) < 20:
            print(f"[{repo}] convencionais insuficientes ({len(t2)})")
            res[repo] = {"n": len(t2), "status": "insuficiente"}
            continue
        E2 = l2(embed(t2))
        p2 = E2 @ v
        a2 = auc(p2[y2 == 1], p2[y2 == 0])
        print(f"[{repo}] n={len(t2)} · AUC transfer {a2:.3f}")
        res[repo] = {"n": len(t2), "auc": a2}
    json.dump(res, open(os.path.join(DIR, "results15.json"), "w"), indent=1)
    print("results15.json gravado.")


if __name__ == "__main__":
    main()
