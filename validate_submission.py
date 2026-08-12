from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
errors = []

required = ["metadata.json", "download_model.sh", "REPORT.md", ".gitignore", "model/.gitkeep"]
for filename in required:
    if not (ROOT / filename).exists():
        errors.append(f"Missing required file: {filename}")

try:
    metadata = json.loads((ROOT / "metadata.json").read_text(encoding="utf-8"))
except Exception as exc:
    metadata = {}
    errors.append(f"Invalid metadata.json: {exc}")

if metadata:
    if metadata.get("domain") != "agriculture": errors.append("domain must be agriculture")
    if metadata.get("budget_laptop_claim") is not True: errors.append("budget_laptop_claim must be true")
    if len(metadata.get("test_prompts", [])) != 2: errors.append("exactly two test prompts are required")
    if metadata.get("model", {}).get("runtime") != "llama.cpp": errors.append("runtime must be llama.cpp")
    if metadata.get("_runtime", {}).get("model_path") != "model/allo-nutri-qwen2.5-1.5b-q4_k_m.gguf": errors.append("model path mismatch")
    text = json.dumps(metadata)
    if "REQUIRED_" in text:
        errors.append("DevPost Team ID, email, and GitHub handle still need to be filled")

gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8") if (ROOT / ".gitignore").exists() else ""
if "*.gguf" not in gitignore or "model/*" not in gitignore:
    errors.append(".gitignore must exclude GGUF weights and model directory contents")

if errors:
    print("Submission preflight: INCOMPLETE")
    for error in errors: print(f"- {error}")
    raise SystemExit(1)
print("Submission preflight: PASS")
