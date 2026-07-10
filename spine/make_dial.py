#!/usr/bin/env python3
"""Exporta a régua bug↔win (aprovada no Exp 13) como dial certificado."""
import hashlib
import json
import os

import numpy as np

from exp13 import BUG, WIN, embed, l2, unit

DIR = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(DIR), "dials", "bug_win_en")


def main():
    os.makedirs(OUT, exist_ok=True)
    E = l2(embed(BUG + WIN))
    v = unit(E[:12].mean(0) - E[12:].mean(0)).astype(np.float32)
    np.savez(os.path.join(OUT, "axis.npz"), v=v)
    ex_hash = hashlib.sha256(
        json.dumps(BUG + WIN, ensure_ascii=False).encode()).hexdigest()
    manifest = {
        "id": "bug_win_en",
        "version": "1.0.0",
        "encoder": {"id": "bge-m3", "runtime": "ollama", "dim": 1024},
        "language": "en",
        "domain": "m1nd-field-reports",
        "polarity": {"positive": "bug/severe", "negative": "win/benign"},
        "examples_sha256": ex_hash,
        "certification": {
            "experiment": "Exp 13 (spine/PREREGISTRO-EXP13.md)",
            "auc": 0.853,
            "null_p95": 0.747,
            "gate": "AUC >= 0.80 and > null p95 — PASSED",
            "ground_truth": "97 field reports labeled by 53 agents",
        },
        "bula": [
            "reads tone/severity of agent field reports in English only",
            "advisory always: max_effect = reverify, never act/block/promote",
            "single encoder: fine signals require a second encoder",
            "purification disabled for this domain (declared abstention)",
            "~15% pairwise inversions expected at AUC 0.853",
        ],
        "governance": {"mode": "advisory", "max_effect": "reverify",
                       "forbidden_actions": ["block", "promote", "delete",
                                             "grant_act"]},
    }
    with open(os.path.join(OUT, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1, ensure_ascii=False)
    print(f"dial certificado: {OUT}")
    print(f"  eixo {v.shape} · exemplos sha256 {ex_hash[:16]}…")


if __name__ == "__main__":
    main()
