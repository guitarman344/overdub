"""Overdub: app locale per copioni e voce dei video. Serve http://localhost:8765.

Ogni sottocartella di VIDEO_ROOT è un video: contiene copione.txt (scene separate da una riga vuota)
e le registrazioni in voce/scena-N.wav.
"""
import json, os, re, subprocess, sys
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
VIDEO_ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else
                             os.environ.get("REGIA_VIDEOS", os.path.expanduser("~/Documents/Video Youtube - Tiktok")))
CONFIG = os.path.join(HERE, "config.json")  # facoltativo, es. {"uploadPage": "https://..."}
VIDEO_EXT = (".mp4", ".mov", ".m4v")


def folder(name):
    """Cartella del video, solo nomi semplici dentro VIDEO_ROOT."""
    if not name or "/" in name or name.startswith(".") or name in ("..",):
        raise ValueError("nome non valido")
    return os.path.join(VIDEO_ROOT, name)


def scenes(name):
    p = os.path.join(folder(name), "copione.txt")
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as fh:
        return [s.strip() for s in re.split(r"\n\s*\n", fh.read()) if s.strip()]


def info(name):
    f = folder(name)
    sc = scenes(name)
    done = [os.path.exists(os.path.join(f, "voce", f"scena-{i + 1}.wav")) for i in range(len(sc))]
    clips = sorted(x for x in os.listdir(f) if x.lower().endswith(VIDEO_EXT))
    return {"name": name, "scenes": sc, "done": done, "clips": clips,
            "updated": os.path.getmtime(f)}


def videos():
    out = []
    for n in os.listdir(VIDEO_ROOT):
        if not n.startswith(".") and os.path.isdir(os.path.join(VIDEO_ROOT, n)):
            out.append(info(n))
    return sorted(out, key=lambda v: -v["updated"])


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body if isinstance(body, bytes) else body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj))

    def _body(self):
        return self.rfile.read(int(self.headers.get("Content-Length") or 0))

    def _q(self):
        u = urlparse(self.path)
        return u.path, {k: v[0] for k, v in parse_qs(u.query).items()}

    def do_GET(self):
        path, q = self._q()
        try:
            if path == "/":
                with open(os.path.join(HERE, "index.html"), "rb") as fh:
                    return self._send(200, fh.read(), "text/html; charset=utf-8")
            if path == "/api/videos":
                return self._json({"root": VIDEO_ROOT, "videos": videos()})
            if path == "/api/config":
                cfg = {}
                if os.path.exists(CONFIG):
                    with open(CONFIG, encoding="utf-8") as fh:
                        cfg = json.load(fh)
                return self._json(cfg)
            if path == "/api/video":
                return self._json(info(q["v"]))
            if path == "/audio":
                p = os.path.join(folder(q["v"]), "voce", f"scena-{int(q['n'])}.wav")
                if os.path.exists(p):
                    with open(p, "rb") as fh:
                        return self._send(200, fh.read(), "audio/wav")
        except (KeyError, ValueError, FileNotFoundError):
            return self._json({"error": "richiesta non valida"}, 400)
        self._json({"error": "non trovato"}, 404)

    def do_POST(self):
        path, q = self._q()
        try:
            if path == "/api/videos":
                name = json.loads(self._body())["name"].strip()
                f = folder(name)
                os.makedirs(os.path.join(f, "voce"), exist_ok=True)
                return self._json(info(name))
            if path == "/api/script":
                text = self._body().decode("utf-8")
                with open(os.path.join(folder(q["v"]), "copione.txt"), "w", encoding="utf-8") as fh:
                    fh.write(text.strip() + "\n")
                return self._json(info(q["v"]))
            if path == "/api/save":
                n = int(q["n"])
                if not 1 <= n <= len(scenes(q["v"])):
                    return self._json({"error": "scena non valida"}, 400)
                body = self._body()
                if body[:4] != b"RIFF":
                    return self._json({"error": "audio non valido"}, 400)
                d = os.path.join(folder(q["v"]), "voce")
                os.makedirs(d, exist_ok=True)
                with open(os.path.join(d, f"scena-{n}.wav"), "wb") as fh:
                    fh.write(body)
                return self._json({"ok": True})
            if path == "/api/reveal":
                subprocess.run(["open", folder(q["v"])])
                return self._json({"ok": True})
        except (KeyError, ValueError, json.JSONDecodeError):
            return self._json({"error": "richiesta non valida"}, 400)
        self._json({"error": "non trovato"}, 404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    os.makedirs(VIDEO_ROOT, exist_ok=True)
    print(f"Overdub pronta: http://localhost:{PORT}  ->  {VIDEO_ROOT}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
