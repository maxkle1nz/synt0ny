#!/usr/bin/env python3
"""paneld — admin panel local da espinha (127.0.0.1:1341).

Serve o dashboard e /api/status com: saúde do Ollama, pulso do shadowd,
dials certificados, progresso da Fase 2, coleta e últimos eventos.
Read-only sobre tudo; nenhuma ação disponível pela interface (a lei).
"""
import glob
import hashlib
import json
import os
import subprocess
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import numpy as np

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, ".m1nd", "synt0ny")
SPECTRA = os.path.join(ROOT, "spectra")
DIALS = os.path.join(HOME, "synt0ny", "dials")
HERE = os.path.dirname(os.path.abspath(__file__))
MARCO_FASE2 = "2026-07-10T21:50:00"
PORT = 1341
ENCODER = "bge-m3"
MAX_TEXT = 20000

_dials_cache = {"mtime": 0, "dials": []}


def load_dials_full():
    paths = sorted(glob.glob(os.path.join(DIALS, "*", "manifest.json")))
    mtime = max((os.path.getmtime(p) for p in paths), default=0)
    if mtime != _dials_cache["mtime"]:
        out = []
        for mp in paths:
            try:
                m = json.load(open(mp))
                z = np.load(os.path.join(os.path.dirname(mp), "axis.npz"))
                out.append((m, z["v"].astype(np.float32),
                            np.sort(z["ref_proj"].astype(np.float32))))
            except Exception:
                continue
        _dials_cache.update(mtime=mtime, dials=out)
    return _dials_cache["dials"]


def spectrum_cached(text):
    h = hashlib.sha256(f"{ENCODER}:{text}".encode()).hexdigest()
    os.makedirs(SPECTRA, exist_ok=True)
    path = os.path.join(SPECTRA, f"{h}.npy")
    if os.path.exists(path):
        return np.load(path), h, True
    body = json.dumps({"model": ENCODER, "input": [text]}).encode()
    req = urllib.request.Request("http://localhost:11434/api/embed",
                                 data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        x = np.array(json.loads(r.read())["embeddings"][0], dtype=np.float32)
    x = x / np.linalg.norm(x)
    np.save(path, x)
    return x, h, False


def read_text(text, which=None):
    x, h, cached = spectrum_cached(text)
    readings = []
    for m, v, ref in load_dials_full():
        if which and m["id"] not in which:
            continue
        score = float(x @ v)
        pct = float((ref < score).mean() * 100)
        readings.append({
            "axis": {"id": m["id"], "version": m["version"],
                     "language": m.get("language")},
            "score": round(score, 4),
            "percentile_ref": round(pct, 1),
            "polarity": m.get("polarity"),
            "riders": [{"code": "SINGLE_ENCODER", "severity": "reverify"},
                       {"code": "REF_BAND_SMALL",
                        "note": f"percentil sobre {len(ref)} exemplos"}],
            "governance": m["governance"],
        })
    return {"input_sha256": h, "cached": cached, "encoder": ENCODER,
            "readings": readings}


def ollama_status():
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags",
                                    timeout=2) as r:
            models = [m["name"] for m in json.loads(r.read()).get("models", [])]
        loaded = []
        try:
            with urllib.request.urlopen("http://localhost:11434/api/ps",
                                        timeout=2) as r:
                loaded = [m["name"] for m in
                          json.loads(r.read()).get("models", [])]
        except Exception:
            pass
        return {"up": True, "models": models, "loaded": loaded,
                "bge_m3": any(m.startswith("bge-m3") for m in models)}
    except Exception:
        return {"up": False, "models": [], "loaded": [], "bge_m3": False}


def shadowd_status():
    out = {"loaded": False, "last_exit": None, "last_tick": None,
           "tick_age_s": None, "log_tail": []}
    try:
        r = subprocess.run(["launchctl", "list", "com.kle1nz.synt0ny-shadowd"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            out["loaded"] = True
            for ln in r.stdout.splitlines():
                if "LastExitStatus" in ln:
                    out["last_exit"] = int(ln.split("=")[1].strip(" ;"))
    except Exception:
        pass
    state = os.path.join(ROOT, "state.json")
    if os.path.exists(state):
        m = os.path.getmtime(state)
        out["last_tick"] = time.strftime("%H:%M:%S", time.localtime(m))
        out["tick_age_s"] = int(time.time() - m)
    log = os.path.join(ROOT, "shadowd.log")
    if os.path.exists(log):
        with open(log, encoding="utf-8", errors="replace") as f:
            out["log_tail"] = f.readlines()[-6:]
    return out


def shadow_data():
    path = os.path.join(ROOT, "shadow.jsonl")
    envs = []
    if os.path.exists(path):
        with open(path, encoding="utf-8", errors="replace") as f:
            for ln in f:
                try:
                    envs.append(json.loads(ln))
                except json.JSONDecodeError:
                    continue
    scores = [e["score"] for e in envs if "score" in e]
    f2_sources = {"field-reports.jsonl", "inbox.jsonl"}
    novos = [e for e in envs if e.get("ts", "") > MARCO_FASE2
             and e.get("source") in f2_sources]
    hist = [0] * 12
    if scores:
        lo, hi = min(scores), max(scores)
        span = (hi - lo) or 1.0
        for s in scores:
            hist[min(11, int((s - lo) / span * 12))] += 1
    spectra = len(glob.glob(os.path.join(ROOT, "spectra", "*.npy")))
    return {"total": len(envs), "novos_fase2": len(novos),
            "hist": hist, "hist_range": [min(scores or [0]),
                                         max(scores or [0])],
            "spectra": spectra,
            "recentes": [{"ts": e.get("ts", ""),
                          "source": e.get("source", ""),
                          "declared": e.get("declared_class"),
                          "score": e.get("score")}
                         for e in envs[-12:]][::-1]}


def dials_list():
    out = []
    for mp in sorted(glob.glob(os.path.join(DIALS, "*", "manifest.json"))):
        try:
            m = json.load(open(mp))
            out.append({"id": m["id"], "version": m["version"],
                        "lang": m.get("language"),
                        "auc": m.get("certification", {}).get("auc"),
                        "mode": m.get("governance", {}).get("mode")})
        except Exception:
            continue
    return out


def fase2_status(novos):
    t0 = time.mktime(time.strptime(MARCO_FASE2, "%Y-%m-%dT%H:%M:%S"))
    dias = (time.time() - t0) / 86400
    return {"dias": round(dias, 1), "eventos_novos": novos,
            "janela_dias": 7, "janela_eventos": 30,
            "pronta": dias >= 7 or novos >= 30,
            "progresso": min(1.0, max(dias / 7, novos / 30))}


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/api/status"):
            sh = shadow_data()
            payload = {
                "now": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ollama": ollama_status(),
                "shadowd": shadowd_status(),
                "shadow": sh,
                "dials": dials_list(),
                "fase2": fase2_status(sh["novos_fase2"]),
            }
            self._send(200, "application/json",
                       json.dumps(payload, ensure_ascii=False).encode())
        elif self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "index.html"), "rb") as f:
                self._send(200, "text/html; charset=utf-8", f.read())
        else:
            self._send(404, "text/plain", b"404")

    def do_POST(self):
        if self.path != "/api/read":
            self._send(404, "text/plain", b"404")
            return
        try:
            n = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(min(n, MAX_TEXT * 4)))
            text = (body.get("text") or "").strip()[:MAX_TEXT]
            if not text:
                self._send(400, "application/json",
                           b'{"error":"text vazio"}')
                return
            out = read_text(text, body.get("dials"))
            self._send(200, "application/json",
                       json.dumps(out, ensure_ascii=False).encode())
        except Exception as e:
            self._send(500, "application/json",
                       json.dumps({"error": f"{type(e).__name__}: {e}"})
                       .encode())


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    if "--open" in sys.argv:
        subprocess.Popen(["open", f"http://localhost:{PORT}"])
    srv.serve_forever()


if __name__ == "__main__":
    main()
