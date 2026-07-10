#!/usr/bin/env python3
"""Exp 9 — o paradigma dos irmãos (v2 pós-verdict fugu). PREREGISTRO-EXP9.md."""
import json
import os

import numpy as np

import resonance
from resonance import DIR, load_dataset, l2

resonance.MODEL = "bge-m3"
MARGIN = 0.001
N_NULL = 300

PARADIGM = {
    "amar": ["amo", "amei", "amava", "amarei", "amaria"],
    "comprar": ["compro", "comprei", "comprava", "comprarei", "compraria"],
    "ganhar": ["ganho", "ganhei", "ganhava", "ganharei", "ganharia"],
    "vender": ["vendo", "vendi", "vendia", "venderei", "venderia"],
    "comer": ["como", "comi", "comia", "comerei", "comeria"],
    "escrever": ["escrevo", "escrevi", "escrevia", "escreverei", "escreveria"],
    "perder": ["perco", "perdi", "perdia", "perderei", "perderia"],
    "subir": ["subo", "subi", "subia", "subirei", "subiria"],
    "abrir": ["abro", "abri", "abria", "abrirei", "abriria"],
    "dormir": ["durmo", "dormi", "dormia", "dormirei", "dormiria"],
    "fazer": ["faço", "fiz", "fazia", "farei", "faria"],
    "ir": ["vou", "fui", "ia", "irei", "iria"],
}
PRES, PERF, IMPF, FUT, COND = range(5)
IRREG = ("fazer", "ir")


def unit(v):
    return v / np.linalg.norm(v)


def run_protocol(E, verbs, diffs, override_v=None):
    """Roda 24 trials; retorna (válidos_ida, válidos_volta, decoy, instáveis, rows)."""
    ida = volta = decoy = unstable = 0
    rows = {}
    for k, v in enumerate(verbs):
        rest = np.delete(diffs, k, axis=0)
        v_fold = unit(rest.mean(axis=0))
        s = float(np.mean(rest @ v_fold))
        vt = v_fold if override_v is None else override_v
        for direction in ("ida", "volta"):
            if direction == "ida":
                q = unit(E[v][PERF] + s * vt)
                ids, tgt = (PRES, IMPF, FUT, COND), FUT
            else:
                q = unit(E[v][FUT] - s * vt)
                ids, tgt = (PRES, PERF, IMPF, COND), PERF
            sims = sorted(((float(q @ E[v][i]), i) for i in ids), reverse=True)
            top, second = sims[0], sims[1]
            stable = (top[0] - second[0]) >= MARGIN
            hit = top[1] == tgt and stable
            if not stable:
                unstable += 1
            if direction == "ida":
                ida += hit
                decoy += top[1] == COND
            else:
                volta += hit
            rows[(v, direction)] = (PARADIGM[v][top[1]], hit, stable)
    return ida, volta, decoy, unstable, rows


def main():
    _, base = load_dataset()
    flex = [w for fs in PARADIGM.values() for w in fs]
    words = base + [w for w in flex if w not in base]
    X = l2(resonance.embed(words))
    X = l2(X - X.mean(axis=0))
    idx = {w: i for i, w in enumerate(words)}
    verbs = list(PARADIGM)
    E = {v: [X[idx[f]] for f in PARADIGM[v]] for v in verbs}

    sib = [float(E[v][a] @ E[v][b]) for v in verbs
           for a in range(5) for b in range(a + 1, 5)]
    res = float(np.mean(sib))
    diffs = np.array([E[v][FUT] - E[v][PERF] for v in verbs])

    ida, volta, decoy, unstable, rows = run_protocol(E, verbs, diffs)
    total = ida + volta

    rng = np.random.default_rng(136)
    null_tot = []
    for _ in range(N_NULL):
        vr = unit(rng.standard_normal(X.shape[1]))
        ni, nv, _, _, _ = run_protocol(E, verbs, diffs, override_v=vr)
        null_tot.append(ni + nv)
    null_tot = np.array(null_tot)
    p95 = float(np.percentile(null_tot, 95))

    b_ida = b_volta = 0
    for v in verbs:
        s = sorted(((float(E[v][PERF] @ E[v][i]), i)
                    for i in (PRES, IMPF, FUT, COND)), reverse=True)
        b_ida += s[0][1] == FUT
        s = sorted(((float(E[v][FUT] @ E[v][i]), i)
                    for i in (PRES, PERF, IMPF, COND)), reverse=True)
        b_volta += s[0][1] == PERF

    irr = sum(rows[(v, d)][1] for v in IRREG for d in ("ida", "volta"))

    print(f"banco {len(words)} · resolução irmão-irmão {res:.4f} · "
          f"itens instáveis {unstable}/24")
    print(f"\nG1 transmutação : ida {ida}/12 · volta {volta}/12  (gate >= 9 e >= 9)")
    print(f"G2 null empírico: real {total}/24 vs null p95 {p95:.0f} "
          f"(média {null_tot.mean():.1f}, máx {null_tot.max()})  "
          f"-> {'PASSA' if total > p95 else 'FALHA'}")
    print(f"    baseline sem transplante: ida {b_ida}/12 · volta {b_volta}/12")
    print(f"F1a decoy       : condicional venceu {decoy}/12 idas (falsifica >= 6)")
    print(f"F1b supletivos  : {irr}/4 acertos válidos em fazer+ir "
          f"(0 = geometria de sufixo · >=1 leitura temporal viva)")
    print(f"F2 teto         : resolução {res:.4f} <= 0.995 e instáveis "
          f"{unstable}/24 <= 12 -> {'ok' if res <= 0.995 and unstable <= 12 else 'ESTOURADO'}")
    print()
    for v in verbs:
        gi, hi, _ = rows[(v, "ida")]
        gv, hv, _ = rows[(v, "volta")]
        tag = "  [irregular]" if v in IRREG else ""
        print(f"  {v:9s} ida→{gi:11s}{'✓' if hi else '✗'}  "
              f"volta→{gv:9s}{'✓' if hv else '✗'}{tag}")

    json.dump({"resolution": res, "unstable": unstable, "ida": ida,
               "volta": volta, "total": total, "null_p95": p95,
               "null_mean": float(null_tot.mean()), "b_ida": b_ida,
               "b_volta": b_volta, "decoy": decoy, "irregular_hits": irr},
              open(os.path.join(DIR, "results9.json"), "w"), indent=1)
    print("\nresults9.json gravado.")


if __name__ == "__main__":
    main()
