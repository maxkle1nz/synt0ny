#!/usr/bin/env python3
"""synt0ny MCP server — tool synt0ny_read sobre o /api/read local.

Stdio JSON-RPC (newline-delimited). Advisory por constituição: devolve
leituras com governança; nunca executa ação. Requer paneld em :1341.
"""
import json
import sys
import urllib.request

PANEL = "http://localhost:1341/api/read"
PANEL_QUEUE = "http://localhost:1341/api/queue"

TOOL = {
    "name": "synt0ny_read",
    "description": (
        "Mede um texto nos mostradores semânticos locais do synt0ny "
        "(réguas certificadas com laudo; advisory — leituras, nunca ações). "
        "Dials atuais: valencia_pt (tom construtivo/destrutivo, pt-BR, "
        "93,2% em produção) e bug_win_en (severidade de report de agente, "
        "en, AUC 0,853). Retorna score, percentil na banda de referência, "
        "riders de incerteza e governança. Custo ~15 ms local."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "text": {"type": "string",
                     "description": "Texto a medir (até 20k chars)"},
            "dials": {"type": "array", "items": {"type": "string"},
                      "description": "IDs dos dials (omitir = todos)"},
        },
        "required": ["text"],
    },
}

TOOL_QUEUE = {
    "name": "synt0ny_queue",
    "description": (
        "Fila de atenção advisory da espinha (T0.1, caso provado na "
        "auditoria cega F2: top-10 ranqueado 9/10 severos vs 7/10 da fila "
        "cronológica): field-reports + inbox do m1nd ranqueados por "
        "severidade (dial bug_win_en). Ordena a atenção, nunca decide; "
        "lê TOM, não verdade (flake dramático ranqueia alto). "
        "Retorna items com score, texto e riders."),
    "inputSchema": {
        "type": "object",
        "properties": {
            "days": {"type": "integer",
                     "description": "Janela em dias (default 7, máx 90)"},
            "top": {"type": "integer",
                    "description": "Quantos itens (default 10, máx 50)"},
        },
    },
}


def rpc(result=None, error=None, id_=None):
    msg = {"jsonrpc": "2.0", "id": id_}
    if error:
        msg["error"] = {"code": -32000, "message": error}
    else:
        msg["result"] = result
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def call_read(args):
    body = json.dumps({"text": args.get("text", ""),
                       "dials": args.get("dials")}).encode()
    req = urllib.request.Request(PANEL, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            m = json.loads(line)
        except json.JSONDecodeError:
            continue
        mid, method = m.get("id"), m.get("method", "")
        try:
            if method == "initialize":
                rpc({"protocolVersion": m["params"]["protocolVersion"],
                     "capabilities": {"tools": {}},
                     "serverInfo": {"name": "synt0ny",
                                    "version": "1.0.0"}}, id_=mid)
            elif method == "tools/list":
                rpc({"tools": [TOOL, TOOL_QUEUE]}, id_=mid)
            elif method == "tools/call":
                name = m["params"]["name"]
                args = m["params"].get("arguments", {})
                if name == "synt0ny_read":
                    out = call_read(args)
                elif name == "synt0ny_queue":
                    url = (f"{PANEL_QUEUE}?days={int(args.get('days', 7))}"
                           f"&top={int(args.get('top', 10))}")
                    with urllib.request.urlopen(url, timeout=30) as r:
                        out = json.loads(r.read())
                else:
                    rpc(error="tool desconhecida", id_=mid)
                    continue
                rpc({"content": [{"type": "text",
                                  "text": json.dumps(out, indent=1,
                                                     ensure_ascii=False)}]},
                    id_=mid)
            elif method == "ping":
                rpc({}, id_=mid)
            elif mid is not None:
                rpc(error=f"método não suportado: {method}", id_=mid)
        except Exception as e:
            if mid is not None:
                rpc(error=f"{type(e).__name__}: {e}", id_=mid)


if __name__ == "__main__":
    main()
