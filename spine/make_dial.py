#!/usr/bin/env python3
"""Fábrica de dials certificados. Uso: make_dial.py [id|all]

Cada dial: axis.npz (eixo + ref_proj dos exemplos) + manifest.json
(identidade, certificação, bula, governança). Régua sem laudo não existe.
"""
import hashlib
import json
import os
import sys

import numpy as np

from exp13 import BUG, WIN, embed, l2, unit

DIR = os.path.dirname(os.path.abspath(__file__))
DIALS_DIR = os.path.join(os.path.dirname(DIR), "dials")


def _valencia_examples():
    with open(os.path.join(os.path.dirname(DIR), "lab", "dataset.json")) as f:
        ant = json.load(f)["antonyms"]
    return [a for a, _ in ant], [b for _, b in ant]


SPECS = {
    "bug_win_en": {
        "examples": lambda: (BUG, WIN),
        "manifest": {
            "language": "en",
            "domain": "m1nd-field-reports",
            "polarity": {"positive": "bug/severe", "negative": "win/benign"},
            "certification": {
                "experiment": "Exp 13 (spine/PREREGISTRO-EXP13.md)",
                "auc": 0.853, "null_p95": 0.747,
                "gate": "AUC >= 0.80 and > null p95 — PASSED",
                "ground_truth": "97 field reports labeled by 53 agents",
            },
            "bula": [
                "reads tone/severity of agent field reports in English only",
                "advisory always: max_effect = reverify",
                "single encoder: fine signals require a second encoder",
                "~15% pairwise inversions expected at AUC 0.853",
                "REFUTED for commit-risk prediction (Exp 14, AUC 0.439)",
            ],
        },
    },
    "valencia_pt": {
        "examples": _valencia_examples,
        "manifest": {
            "language": "pt-BR",
            "domain": "texto avaliativo curto (reviews, feedback, frases)",
            "polarity": {"positive": "acréscimo/construtivo",
                         "negative": "dissipação/destrutivo"},
            "certification": {
                "experiment": "Exp 5 + Exp 10 + Exp 12 (lab/, atlas/)",
                "loo": "12/12 pares held-out (Exp 5)",
                "phrase_bridge": "100% em 52 frases · 14/14 vocab virgem",
                "production": "93.2% acc · AUC 0.979 em 500 reviews reais",
                "gate": "todos PASSED",
            },
            "bula": [
                "lê valência de texto pt curto; forte no polo negativo",
                "erra onde humanos divergem: ironia, mistas, sem-valência",
                "não é intenção pragmática (pergunta/ordem) — só tom",
                "advisory always: max_effect = reverify",
                "viés lexical em construções adversariais (Exp 10: 3/8)",
            ],
        },
    },
}

BASE_MANIFEST = {
    "encoder": {"id": "bge-m3", "runtime": "ollama", "dim": 1024},
    "governance": {"mode": "advisory", "max_effect": "reverify",
                   "forbidden_actions": ["block", "promote", "delete",
                                         "grant_act"]},
}


def build(dial_id):
    spec = SPECS[dial_id]
    pos, neg = spec["examples"]()
    E = l2(embed(list(pos) + list(neg)))
    v = unit(E[: len(pos)].mean(0) - E[len(pos):].mean(0)).astype(np.float32)
    ref_proj = (E @ v).astype(np.float32)
    out = os.path.join(DIALS_DIR, dial_id)
    os.makedirs(out, exist_ok=True)
    np.savez(os.path.join(out, "axis.npz"), v=v, ref_proj=ref_proj)
    manifest = {"id": dial_id, "version": "1.1.0", **BASE_MANIFEST,
                **spec["manifest"],
                "examples_sha256": hashlib.sha256(
                    json.dumps(list(pos) + list(neg),
                               ensure_ascii=False).encode()).hexdigest(),
                "ref_band": {"n": len(ref_proj),
                             "min": float(ref_proj.min()),
                             "max": float(ref_proj.max())}}
    with open(os.path.join(out, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
    print(f"dial {dial_id} v1.1.0 · eixo {v.shape} · banda "
          f"[{ref_proj.min():+.3f}, {ref_proj.max():+.3f}]")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for d in (SPECS if which == "all" else [which]):
        build(d)
