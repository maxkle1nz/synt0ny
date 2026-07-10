#!/usr/bin/env python3
"""paneld — admin panel local da espinha (127.0.0.1:1341).

Serve o dashboard e /api/status com: saúde do Ollama, pulso do shadowd,
dials certificados, progresso da Fase 2, coleta e últimos eventos.
Read-only sobre tudo; nenhuma ação disponível pela interface (a lei).
"""
import glob
import json
import os
import subprocess
import sys
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOME = os.path.expanduser("~")
ROOT = os.path.join(HOME, ".m1nd", "synt0ny")
DIALS = os.path.join(HOME, "synt0ny", "dials")
HERE = os.path.dirname(os.path.abspath(__file__))
MARCO_FASE2 = "2026-07-10T21:50:00"
PORT = 1341


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
    novos = [e for e in envs if e.get("ts", "") > MARCO_FASE2]
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


def main():
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    if "--open" in sys.argv:
        subprocess.Popen(["open", f"http://localhost:{PORT}"])
    srv.serve_forever()


if __name__ == "__main__":
    main()
