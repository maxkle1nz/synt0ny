#!/usr/bin/env python3
"""shadowd v1.2 — a espinha em modo sombra, multi-frente.

Streams separados por fonte, dials adequados por domínio, e leituras
fora-de-domínio marcadas com DOMAIN_SHIFT (coleta honesta, nunca medição
fingida). A janela da Fase 2 segue julgando SÓ os streams originais.
ADVISORY: nunca toca arquivo do m1nd. Fail-quiet.
"""
import glob
import hashlib
import json
import os
import sys
import time
import urllib.request

HOME = os.path.expanduser("~")
SYNT = os.path.join(HOME, "synt0ny")
ROOT = os.path.join(HOME, ".m1nd", "synt0ny")
STATE = os.path.join(ROOT, "state.json")
SHADOW = os.path.join(ROOT, "shadow.jsonl")
SPECTRA = os.path.join(ROOT, "spectra")
LOG = os.path.join(ROOT, "shadowd.log")
PID = os.path.join(ROOT, "shadowd.pid")
OLLAMA = "http://localhost:11434"
ENCODER = "bge-m3"
TEXT_FIELDS = ("what", "text", "message", "body", "summary", "title",
               "detail")

SOURCES = [
    {"path": os.path.join(HOME, ".m1nd", "field-reports.jsonl"),
     "stream": "field-reports", "mode": "jsonl", "dials": None,
     "riders": []},
    {"path": os.path.join(HOME, ".m1nd", "inbox.jsonl"),
     "stream": "inbox", "mode": "jsonl", "dials": None, "riders": []},
    {"path": os.path.join(HOME, ".m1nd", "bridge",
                          "h4nd-to-orchestrator.jsonl"),
     "stream": "bridge", "mode": "jsonl", "dials": ["valencia_pt"],
     "riders": [{"code": "DOMAIN_SHIFT", "severity": "info",
                 "note": "correio de agente pt; dial selado p/ avaliativo"}]},
    {"path": os.path.join(HOME, ".m1nd", "bridge",
                          "orchestrator-to-h4nd.jsonl"),
     "stream": "bridge", "mode": "jsonl", "dials": ["valencia_pt"],
     "riders": [{"code": "DOMAIN_SHIFT", "severity": "info",
                 "note": "correio de agente pt; dial selado p/ avaliativo"}]},
    {"path": os.path.join(HOME, ".m1nd", "runtimes", "claude",
                          "daemon_alerts.json"),
     "stream": "daemon-alerts", "mode": "json_array",
     "dials": ["bug_win_en"],
     "riders": [{"code": "DOMAIN_SHIFT", "severity": "info",
                 "note": "alerts do daemon; dial selado p/ field-reports"}]},
    {"path": "gh:/users/maxkle1nz/events",
     "stream": "github", "mode": "github_events",
     "dials": ["bug_win_en"],
     "riders": [{"code": "DOMAIN_SHIFT", "severity": "info",
                 "note": "commits do perfil; leitura de tom agregável, "
                         "NUNCA previsão de risco (Exp 14 refutou)"}]},
]
GH = "/opt/homebrew/bin/gh"


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")


def embed(texts):
    import numpy as np
    out = []
    for i in range(0, len(texts), 50):
        body = json.dumps({"model": ENCODER,
                           "input": texts[i:i + 50]}).encode()
        req = urllib.request.Request(f"{OLLAMA}/api/embed", data=body,
                                     headers={"Content-Type":
                                              "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            out.extend(json.loads(r.read())["embeddings"])
    X = np.array(out, dtype=np.float32)
    return X / np.linalg.norm(X, axis=-1, keepdims=True)


def load_dials():
    import numpy as np
    dials = {}
    for mpath in glob.glob(os.path.join(SYNT, "dials", "*", "manifest.json")):
        try:
            m = json.load(open(mpath))
            v = np.load(os.path.join(os.path.dirname(mpath), "axis.npz"))["v"]
            dials[m["id"]] = (m, v)
        except Exception:
            continue
    return dials


def spectrum(text):
    import numpy as np
    h = hashlib.sha256(f"{ENCODER}:{text}".encode()).hexdigest()
    path = os.path.join(SPECTRA, f"{h}.npy")
    if os.path.exists(path):
        return np.load(path), h, True
    x = embed([text])[0]
    np.save(path, x)
    return x, h, False


def extract_text(d):
    return next((str(d[k]).strip() for k in TEXT_FIELDS if d.get(k)), "")


def _gh(path):
    import subprocess
    raw = subprocess.run([GH, "api", path], capture_output=True,
                         text=True, timeout=30).stdout
    return json.loads(raw)


def github_events(spec, state):
    """Colhe commits novos por-repo (a API de events censura payloads
    privados). 1 chamada de listagem + 1 por repo ativo desde o último tick."""
    # 1 listagem de repos por tick estourava o G-F2b (tick <= 1 s) e o
    # rate-limit à toa; commits não giram em 300 s — sonda a cada 30 min
    throttle_key = f"throttle:{spec['path']}"
    if time.time() < state.get(throttle_key, 0):
        return []
    state[throttle_key] = time.time() + 1800
    seen_key = f"seen:{spec['path']}"
    since_key = f"since:{spec['path']}"
    seen_list = list(state.get(seen_key, []))
    seen = set(seen_list)
    since = state.get(since_key) or time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 48 * 3600))
    now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    fresh = []
    try:
        repos = _gh("/user/repos?sort=pushed&per_page=15"
                    "&affiliation=owner,organization_member")
        for r in repos if isinstance(repos, list) else []:
            if (r.get("pushed_at") or "") < since:
                continue
            full = r["full_name"]
            try:
                commits = _gh(f"/repos/{full}/commits?since={since}"
                              "&per_page=50")
            except Exception:
                continue
            for c in commits if isinstance(commits, list) else []:
                sha = c.get("sha", "")
                if not sha or sha in seen:
                    continue
                seen.add(sha)
                seen_list.append(sha)
                msg = (c.get("commit", {}).get("message", "")
                       .split("\n")[0])
                author = (c.get("author") or {}).get("login") or \
                    c.get("commit", {}).get("author", {}).get("name", "")
                fresh.append({"text": msg, "repo": full,
                              "sha": sha[:12], "author": author})
    except Exception:
        return []
    state[seen_key] = seen_list[-3000:]
    state[since_key] = now_iso
    return fresh


def new_items(spec, state):
    path = spec["path"]
    if spec["mode"] == "github_events":
        return github_events(spec, state)
    if not os.path.exists(path):
        return []
    if spec["mode"] == "jsonl":
        off = state.get(path, 0)
        size = os.path.getsize(path)
        if size < off:
            off = 0
        if size == off:
            return []
        with open(path, encoding="utf-8", errors="replace") as f:
            f.seek(off)
            chunk = f.read()
            state[path] = f.tell()
        out = []
        for ln in chunk.splitlines():
            if not ln.strip():
                continue
            try:
                out.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
        return out
    # json_array: arquivo re-escrito inteiro a cada save. Dedupe pelo TEXTO
    # extraído — hash do item inteiro re-conta a cada campo mutante (foi a
    # inundação de 283k envelopes de 18-20/07) — e seen em ordem de
    # inserção: sorted()[-N:] cortava por ordem LEXICOGRÁFICA e vazava.
    seen_key = f"seen:{path}"
    seen_list = list(state.get(seen_key, []))
    seen = set(seen_list)
    try:
        data = json.load(open(path, encoding="utf-8", errors="replace"))
    except (json.JSONDecodeError, OSError):
        return []
    items = data if isinstance(data, list) else data.get("alerts", [])
    fresh = []
    for it in items:
        if not isinstance(it, dict):
            continue
        text = extract_text(it)
        if not text:
            continue
        h = hashlib.sha256(text.encode()).hexdigest()
        if h not in seen:
            seen.add(h)
            seen_list.append(h)
            fresh.append(it)
    state[seen_key] = seen_list[-5000:]
    return fresh


def main():
    os.makedirs(SPECTRA, exist_ok=True)
    if os.path.exists(PID):
        age = time.time() - os.path.getmtime(PID)
        if age < 240:
            return
        log(f"pid file stale ({age:.0f}s) — assuming crashed run, continuing")
    open(PID, "w").write(str(os.getpid()))
    try:
        state = json.load(open(STATE)) if os.path.exists(STATE) else {}
        t0 = time.perf_counter()
        # colhe ANTES de carregar dials: o no-op não pode pagar o import
        # do numpy (G-F2b sela tick incremental <= 1 s)
        harvest = []
        for spec in SOURCES:
            items = new_items(spec, state)
            if items:
                harvest.append((spec, items))
        if not harvest:
            json.dump(state, open(STATE, "w"))
            return
        dials = load_dials()
        if not dials:
            log("no dials found — nothing to do")
            return
        n_events = n_miss = 0
        with open(SHADOW, "a", encoding="utf-8") as out:
            for spec, items in harvest:
                which = spec["dials"] or list(dials)
                for d in items:
                    text = extract_text(d)
                    if not text:
                        continue
                    x, h, hit = spectrum(text)
                    n_events += 1
                    n_miss += (not hit)
                    for did in which:
                        if did not in dials:
                            continue
                        m, v = dials[did]
                        env = {
                            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            "stream": spec["stream"],
                            "source": os.path.basename(spec["path"]),
                            "input_sha256": h,
                            "declared_class": d.get("class"),
                            "meta": {k: d[k] for k in ("repo", "sha")
                                     if d.get(k)} or None,
                            "axis": {"id": m["id"],
                                     "version": m["version"]},
                            "score": round(float(x @ v), 4),
                            "riders": ([{"code": "SINGLE_ENCODER",
                                         "severity": "reverify"},
                                        {"code": "SHADOW_MODE",
                                         "severity": "info"}]
                                       + spec["riders"]),
                            "governance": m["governance"],
                        }
                        out.write(json.dumps(env, ensure_ascii=False) + "\n")
        json.dump(state, open(STATE, "w"))
        dt = (time.perf_counter() - t0) * 1e3
        if n_events:
            log(f"tick ok: {n_events} events ({n_miss} embedded, "
                f"{n_events - n_miss} cached) · {len(SOURCES)} fontes · "
                f"{dt:.0f} ms")
    except Exception as e:
        log(f"tick FAILED (quiet): {type(e).__name__}: {e}")
    finally:
        try:
            os.remove(PID)
        except OSError:
            pass


if __name__ == "__main__":
    sys.exit(main())
