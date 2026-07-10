#!/usr/bin/env python3
"""shadowd — a espinha em modo sombra (T0).

Tail incremental das fontes do m1nd, projeção nos dials certificados,
um envelope v0 por evento em shadow.jsonl. ADVISORY: nunca toca arquivo
do m1nd, nunca age. Fail-quiet: qualquer erro vira 1 linha de log.
"""
import glob
import hashlib
import json
import os
import sys
import time
import urllib.request

import numpy as np

HOME = os.path.expanduser("~")
SYNT = os.path.join(HOME, "synt0ny")
ROOT = os.path.join(HOME, ".m1nd", "synt0ny")
SOURCES = [os.path.join(HOME, ".m1nd", "field-reports.jsonl"),
           os.path.join(HOME, ".m1nd", "inbox.jsonl")]
STATE = os.path.join(ROOT, "state.json")
SHADOW = os.path.join(ROOT, "shadow.jsonl")
SPECTRA = os.path.join(ROOT, "spectra")
LOG = os.path.join(ROOT, "shadowd.log")
PID = os.path.join(ROOT, "shadowd.pid")
OLLAMA = "http://localhost:11434"
ENCODER = "bge-m3"
TEXT_FIELDS = ("what", "text", "message", "body", "summary")


def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}\n")


def embed(texts):
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
    dials = []
    for mpath in glob.glob(os.path.join(SYNT, "dials", "*", "manifest.json")):
        with open(mpath) as f:
            m = json.load(f)
        v = np.load(os.path.join(os.path.dirname(mpath), "axis.npz"))["v"]
        dials.append((m, v))
    return dials


def spectrum(text):
    h = hashlib.sha256(f"{ENCODER}:{text}".encode()).hexdigest()
    path = os.path.join(SPECTRA, f"{h}.npy")
    if os.path.exists(path):
        return np.load(path), h, True
    x = embed([text])[0]
    np.save(path, x)
    return x, h, False


def new_lines(path, state):
    if not os.path.exists(path):
        return []
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
    return [ln for ln in chunk.splitlines() if ln.strip()]


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
        dials = load_dials()
        if not dials:
            log("no dials found — nothing to do")
            return
        n_events = n_miss = 0
        t0 = time.perf_counter()
        with open(SHADOW, "a", encoding="utf-8") as out:
            for src in SOURCES:
                for ln in new_lines(src, state):
                    try:
                        d = json.loads(ln)
                    except json.JSONDecodeError:
                        continue
                    text = next((str(d[k]).strip() for k in TEXT_FIELDS
                                 if d.get(k)), "")
                    if not text:
                        continue
                    x, h, hit = spectrum(text)
                    n_events += 1
                    n_miss += (not hit)
                    for m, v in dials:
                        env = {
                            "ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
                            "source": os.path.basename(src),
                            "input_sha256": h,
                            "declared_class": d.get("class"),
                            "axis": {"id": m["id"],
                                     "version": m["version"]},
                            "score": round(float(x @ v), 4),
                            "riders": [{"code": "SINGLE_ENCODER",
                                        "severity": "reverify"},
                                       {"code": "SHADOW_MODE",
                                        "severity": "info"}],
                            "governance": m["governance"],
                        }
                        out.write(json.dumps(env, ensure_ascii=False) + "\n")
        json.dump(state, open(STATE, "w"))
        dt = (time.perf_counter() - t0) * 1e3
        if n_events:
            log(f"tick ok: {n_events} events ({n_miss} embedded, "
                f"{n_events - n_miss} cached) · {len(dials)} dial(s) · "
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
