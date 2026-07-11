#!/usr/bin/env python3
"""Hook UserPromptSubmit: anexa a leitura synt0ny do prompt como contexto.

Fail-silent por constituição: qualquer falha (paneld fora, timeout, parse)
= exit 0 sem output. Timeout duro de 1 s. Advisory: contexto, nunca ação.
"""
import json
import sys
import urllib.request


def main():
    try:
        prompt = (json.load(sys.stdin).get("prompt") or "").strip()
        if len(prompt) < 8:
            return
        body = json.dumps({"text": prompt[:4000]}).encode()
        req = urllib.request.Request(
            "http://localhost:1341/api/read", data=body,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=1.0) as r:
            d = json.loads(r.read())
        parts = []
        for x in d.get("readings", []):
            pol = "⊕" if x["percentile_ref"] >= 60 else \
                  "⊖" if x["percentile_ref"] <= 40 else "·"
            parts.append(f"{x['axis']['id']} {x['score']:+.2f} "
                         f"(p{x['percentile_ref']:.0f}{pol})")
        if not parts:
            return
        ctx = ("[synt0ny · leitura advisory do prompt] " + " · ".join(parts)
               + " — mostradores locais; medem tom, não decidem nada")
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ctx}}))
    except Exception:
        return


if __name__ == "__main__":
    main()
