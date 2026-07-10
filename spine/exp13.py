#!/usr/bin/env python3
"""Exp 13 — a espinha, fase 1: réguas inglesas sobre field-reports reais.
PREREGISTRO-EXP13.md. Exemplos autorais congelados ANTES de ler os reports."""
import json
import os
import time
import urllib.request

import numpy as np

DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS = os.path.expanduser("~/.m1nd/field-reports.jsonl")
OLLAMA = "http://localhost:11434"
SEED = 136

BUG = [
    "seek returned a node that does not exist in the graph anymore",
    "the tool crashed with a panic when the file path contained spaces",
    "delegate lost the mission packet and the child agent timed out",
    "auto ingest silently skipped every file in the subdirectory",
    "the cache returned results from a different project brain",
    "memorize wrote the claim twice and both copies drifted apart",
    "north packet cited a line number that points to deleted code",
    "the daemon tick crashed and never restarted until manual kill",
    "trust envelope reported full trust while the binding was broken",
    "search results were truncated without any warning or marker",
    "the migration corrupted timestamps on every promoted claim",
    "impact analysis missed a direct caller and the edit broke it",
]
WIN = [
    "north gave exactly the three anchors I needed on first try",
    "seek surfaced the field memory that explained the whole bug",
    "the new rerank put the right node at the top instantly",
    "delegation packet was so complete the child finished early",
    "auto ingest picked up the new files before I even asked",
    "the medulla recall saved me an hour of rediscovery today",
    "impact correctly predicted every caller that would break",
    "the trust selftest caught a stale binding before I acted",
    "warmup made the first seek feel instant this session",
    "the debrief classification matched my manual review perfectly",
    "cross verify flagged the stale claim exactly as designed",
    "the focus budget kept the whole session lean and on target",
]
OVERCLAIM = [
    "the envelope said act with high trust but the code was gone",
    "it claimed the claim was fresh although the file changed weeks ago",
    "reported closed loop but the verification never actually ran",
    "said the graph was fully ingested while half the crate was missing",
    "confidence high on a path that was deleted two commits ago",
    "it asserted test coverage exists but no test file was found",
    "the summary claimed all callers updated when one was skipped",
    "marked verified without any evidence reference attached",
    "said the binding matched my repo but it was another brain",
    "the answer sounded certain yet cited a function that never existed",
    "reported zero drift while the working tree had local changes",
    "claimed the migration was idempotent but reran with duplicates",
]
CALIBRATED = [
    "it said insufficient evidence and asked me to verify manually",
    "the tool abstained because the binding trust was degraded",
    "flagged its own answer as possibly stale and suggested reingest",
    "returned partial results and clearly marked the truncation",
    "the envelope downgraded to reverify when the file changed",
    "it admitted the claim author was unknown instead of guessing",
    "declared the gap honestly: no memory surfaced for this task",
    "the verdict was abstain pending a real test run",
    "it cited exact lines and offered the command to double check",
    "warned that the graph generation was older than my checkout",
    "the answer distinguished measured facts from assumptions",
    "asked for a second encoder before trusting the fine signal",
]


def embed(texts):
    out = []
    for i in range(0, len(texts), 50):
        body = json.dumps({"model": "bge-m3", "input": texts[i:i + 50]}).encode()
        req = urllib.request.Request(f"{OLLAMA}/api/embed", data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=300) as r:
            out.extend(json.loads(r.read())["embeddings"])
    return np.array(out, dtype=np.float32)


def l2(X):
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def unit(v):
    return v / np.linalg.norm(v)


def auc(pos, neg):
    return float(np.mean([p > n for p in pos for n in neg]))


def main():
    texts, labels = [], []
    with open(REPORTS, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            w = (d.get("what") or "").strip()
            if w:
                texts.append(w)
                labels.append(d.get("class", "?"))
    labels = np.array(labels)
    print(f"reports com texto: {len(texts)} · "
          f"classes: {dict(zip(*np.unique(labels, return_counts=True)))}")

    E_ex = l2(embed(BUG + WIN + OVERCLAIM + CALIBRATED))
    t0 = time.perf_counter()
    E = l2(embed(texts))
    t_embed = (time.perf_counter() - t0) / len(texts) * 1e3

    v_bw = unit(E_ex[:12].mean(0) - E_ex[12:24].mean(0))
    v_hs = unit(E_ex[24:36].mean(0) - E_ex[36:48].mean(0))

    rng = np.random.default_rng(SEED)
    proj_bw = E @ v_bw
    is_bug, is_win = labels == "bug", labels == "win"
    auc_real = auc(proj_bw[is_bug], proj_bw[is_win])
    null_auc = []
    for _ in range(300):
        ids = rng.choice(len(texts), size=24, replace=False)
        vv = unit(E[ids[:12]].mean(0) - E[ids[12:]].mean(0))
        p = E @ vv
        null_auc.append(auc(p[is_bug], p[is_win]))
    p95_auc = float(np.percentile(null_auc, 95))
    g1 = auc_real >= 0.80 and auc_real > p95_auc
    print(f"\nG1 bug↔win : AUC {auc_real:.3f} (gate >= 0.80 e > p95 null "
          f"{p95_auc:.3f}) -> {'PASSA' if g1 else 'FALHA'}")

    proj_hs = E @ v_hs
    top10 = np.argsort(-proj_hs)[:10]
    hits = int(np.sum(labels[top10] == "honesty"))
    null_p10 = []
    for _ in range(300):
        ids = rng.choice(len(texts), size=24, replace=False)
        vv = unit(E[ids[:12]].mean(0) - E[ids[12:]].mean(0))
        t = np.argsort(-(E @ vv))[:10]
        null_p10.append(int(np.sum(labels[t] == "honesty")))
    p95_p10 = float(np.percentile(null_p10, 95))
    g2 = hits >= 4 and hits > p95_p10
    print(f"G2 honesty : {hits}/10 no top-10 (gate >= 4 e > p95 null "
          f"{p95_p10:.0f}; acaso ~1.1) -> {'PASSA' if g2 else 'FALHA'}")
    print("   top-10:", ", ".join(labels[top10]))

    t0 = time.perf_counter()
    for _ in range(1000):
        E @ v_bw
        E @ v_hs
    t_proj = (time.perf_counter() - t0) / 1000 / len(texts) * 1e6

    llm_prompt = ("Classify this agent field report as bug, win, friction, "
                  "honesty or triage. Answer with one word only.\nReport: ")
    t0 = time.perf_counter()
    for w in texts[:5]:
        body = json.dumps({"model": "qwen2.5:7b", "prompt": llm_prompt + w,
                           "stream": False,
                           "options": {"num_predict": 4}}).encode()
        req = urllib.request.Request(f"{OLLAMA}/api/generate", data=body,
                                     headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=300).read()
    t_llm = (time.perf_counter() - t0) / 5 * 1e3
    ratio = (t_llm * 1e3) / t_proj
    g3 = ratio >= 1e4
    print(f"G3 economia: projeção {t_proj:.2f} µs/report (2 réguas) · "
          f"embed 1× {t_embed:.1f} ms · LLM local {t_llm:.0f} ms/report")
    print(f"   razão reflexo-vs-LLM (quente): {ratio:,.0f}× "
          f"(gate >= 10.000×) -> {'PASSA' if g3 else 'FALHA'}")

    top = int(np.argmax(proj_hs))
    envelope = {
        "measurement_id": f"exp13-demo-{top}",
        "axis": {"id": "honesty_smell", "version": "0.1.0-en"},
        "score": round(float(proj_hs[top]), 4),
        "percentile": round(float((proj_hs < proj_hs[top]).mean() * 100), 1),
        "riders": [{"code": "SINGLE_ENCODER", "severity": "reverify"},
                   {"code": "PURIFICATION_ABSTAINED",
                    "reason": "domain-not-covered"}],
        "governance": {"mode": "advisory", "max_effect": "reverify"},
    }
    print("\nenvelope v0 (RF10), leitura mais alta da régua honesty:")
    print(json.dumps(envelope, indent=1))

    json.dump({"auc_bw": auc_real, "p95_auc": p95_auc, "hits_at10": hits,
               "p95_p10": p95_p10, "us_projection": t_proj,
               "ms_embed": t_embed, "ms_llm": t_llm, "ratio": ratio},
              open(os.path.join(DIR, "results13.json"), "w"), indent=1)
    print("\nresults13.json gravado.")


if __name__ == "__main__":
    main()
