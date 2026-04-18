import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from recommender import load_songs, recommend_songs, self_critique_recommendations, retrieve_knowledge

DATA_DIR = ROOT_DIR / "data"
SONGS_CSV = DATA_DIR / "songs.csv"
KNOWLEDGE_JSON = DATA_DIR / "knowledge.json"

PORT = 8000

class DemoRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        frontend_dir = str(Path(__file__).resolve().parent)
        super().__init__(*args, directory=frontend_dir, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path != "/recommend":
            self.send_error(404, "Not Found")
            return

        content_length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(content_length)
        try:
            user_prefs = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON payload")
            return

        try:
            songs = load_songs(str(SONGS_CSV))
            recommendations = recommend_songs(user_prefs, songs, k=5)
            knowledge = retrieve_knowledge(user_prefs, str(KNOWLEDGE_JSON))
            critique = self_critique_recommendations(recommendations, user_prefs)

            payload = {
                "knowledge": knowledge,
                "recommendations": [
                    {
                        "song": rec[0],
                        "score": rec[1],
                        "reasons": rec[2].split("; "),
                        "confidence": rec[3]
                    }
                    for rec in recommendations
                ],
                "critique": critique
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        except Exception as exc:
            self.send_error(500, f"Server error: {exc}")

    def self_critique_text(self, recommendations, user_prefs):
        return self_critique_recommendations(recommendations, user_prefs)

    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()


def run_server():
    server_address = ("", PORT)
    with HTTPServer(server_address, DemoRequestHandler) as httpd:
        print(f"Serving demo at http://localhost:{PORT}")
        print("Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Stopping server")

if __name__ == "__main__":
    run_server()
