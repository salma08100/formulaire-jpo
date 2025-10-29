from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import csv
import os

CSV_PATH = "reponses.csv"

# Création du fichier CSV si nécessaire
if not os.path.exists(CSV_PATH):
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["age", "formation", "origine"])

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        params = urllib.parse.parse_qs(post_data)

        age = params.get("age", [""])[0]
        formation = params.get("formation", [""])[0]
        origine = params.get("origine", [""])[0]

        # Ajoute la réponse dans le CSV
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([age, formation, origine])

        # Réponse HTTP
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("✅ Réponse enregistrée dans le CSV".encode("utf-8"))

if __name__ == "__main__":
    print("🚀 Serveur CSV prêt sur http://localhost:8000")
    HTTPServer(("localhost", 8000), RequestHandler).serve_forever()
