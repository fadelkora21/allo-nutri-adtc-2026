from __future__ import annotations

import json
import os
import subprocess
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from optimizer import FormulationError, formulate, public_catalog

ROOT = Path(__file__).resolve().parent


def offline_advice(result: dict, language: str = "fr") -> str:
    n = result["nutrients"]
    ingredients = ", ".join(f'{x["name"]} ({x["kg"]:.2f} kg)' for x in result["quantities"])
    if language == "ha":
        return (
            f"Wannan haɗin abincin mai araha ya ƙunshi {ingredients}. "
            f"Yana bayar da kusan {n['me']:.0f} kcal/kg na makamashi, "
            f"furotin {n['cp']:.2f}%, calcium {n['ca']:.2f}% da phosphorus mai amfani {n['avp']:.2f}%. "
            "Haɗin ya cika ƙa’idojin gina abincin kaji na wannan mataki. A tabbatar da sinadaran gida a dakin gwaje-gwaje."
        )
    if language == "en":
        return (
            f"The least-cost formula contains {ingredients}. It provides approximately "
            f"{n['me']:.0f} kcal/kg metabolizable energy, {n['cp']:.2f}% crude protein, "
            f"{n['ca']:.2f}% calcium and {n['avp']:.2f}% available phosphorus. "
            "All configured constraints for this growth phase are satisfied."
        )
    return (
        f"La formule la moins coûteuse contient {ingredients}. "
        f"Elle apporte environ {n['me']:.0f} kcal/kg d’énergie métabolisable, "
        f"{n['cp']:.2f} % de protéines brutes, {n['ca']:.2f} % de calcium et "
        f"{n['avp']:.2f} % de phosphore disponible. Les contraintes définies pour cette phase sont respectées."
    )


def llm_advice(result: dict, language: str = "fr") -> str:
    model = os.getenv("ALLO_NUTRI_MODEL")
    cli = os.getenv("LLAMA_CLI", "llama-cli")
    if not model or not Path(model).exists():
        return offline_advice(result, language)
    language_name = {"fr": "français simple", "ha": "hausa simple", "en": "clear English"}.get(language, "français simple")
    prompt = (
        "Tu es ALLO NUTRI, assistant prudent en alimentation des poulets. "
        f"Explique cette formule en {language_name}, sans modifier les chiffres ni prescrire un traitement. "
        "Réponds en 120 mots maximum. Données: " + json.dumps(result, ensure_ascii=False)
    )
    try:
        run = subprocess.run([cli, "-m", model, "-p", prompt, "-n", "180", "--temp", "0.2"], capture_output=True, text=True, timeout=90, check=True)
        return run.stdout.strip() or offline_advice(result, language)
    except (OSError, subprocess.SubprocessError):
        return offline_advice(result, language)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "web"), **kwargs)

    def log_message(self, fmt, *args):
        print(f"[ALLO NUTRI] {fmt % args}")

    def send_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/catalog":
            return self.send_json(public_catalog())
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/formulate":
            return self.send_json({"error": "Route inconnue"}, 404)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length) or b"{}")
            result = formulate(payload.get("phase", "starter"), float(payload.get("total_kg", 100)), payload.get("ingredients", []))
            language = payload.get("language", "fr")
            if language not in {"fr", "ha", "en"}:
                language = "fr"
            result["advice"] = llm_advice(result, language)
            return self.send_json(result)
        except (ValueError, json.JSONDecodeError):
            return self.send_json({"error": "Données invalides."}, 400)
        except FormulationError as exc:
            return self.send_json({"error": exc.message}, 422)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    print(f"ALLO NUTRI est disponible sur http://127.0.0.1:{port}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
