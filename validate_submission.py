from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
errors: list[str] = []

REQUIRED_FILES = [
    "metadata.json",
    "download_model.sh",
    "REPORT.md",
    ".gitignore",
]

for filename in REQUIRED_FILES:
    if not (ROOT / filename).is_file():
        errors.append(f"Missing required file: {filename}")

# Validate metadata.json
try:
    metadata = json.loads(
        (ROOT / "metadata.json").read_text(encoding="utf-8")
    )
except Exception as exc:
    metadata = {}
    errors.append(f"Invalid metadata.json: {exc}")

if metadata:
    if metadata.get("team_id") != "allo-nutri-feed-formulator":
        errors.append(
            "team_id must be allo-nutri-feed-formulator"
        )

    if metadata.get("domain") != "agriculture":
        errors.append("domain must be agriculture")

    if metadata.get("budget_laptop_claim") is not True:
        errors.append("budget_laptop_claim must be true")

    test_prompts = metadata.get("test_prompts", [])

    if not isinstance(test_prompts, list) or len(test_prompts) != 2:
        errors.append("Exactly two test prompts are required")

    if metadata.get("model", {}).get("runtime") != "llama.cpp":
        errors.append("runtime must be llama.cpp")

    expected_model_path = (
        "model/allo-nutri-qwen2.5-1.5b-q4_k_m.gguf"
    )

    if metadata.get("_runtime", {}).get("model_path") != expected_model_path:
        errors.append("model path mismatch")

    metadata_text = json.dumps(metadata).lower()

    forbidden_placeholders = [
        "required_",
        "placeholder",
        "your_team_id",
        "your_email",
        "your_github",
        "todo",
        "tbd",
    ]

    for placeholder in forbidden_placeholders:
        if placeholder in metadata_text:
            errors.append(
                f"metadata.json contains a placeholder: {placeholder}"
            )

# Validate .gitignore
gitignore_path = ROOT / ".gitignore"

if gitignore_path.is_file():
    gitignore = gitignore_path.read_text(encoding="utf-8")

    if "*.gguf" not in gitignore:
        errors.append(".gitignore must exclude *.gguf")

    if "model/" not in gitignore:
        errors.append(".gitignore must exclude model/")

# Validate download_model.sh
download_script = ROOT / "download_model.sh"

if download_script.is_file():
    script_text = download_script.read_text(encoding="utf-8")

    if "mkdir -p" not in script_text:
        errors.append(
            "download_model.sh must create the model directory"
        )

    if "huggingface.co" not in script_text:
        errors.append(
            "download_model.sh must contain a public model URL"
        )

    if "GGUF" not in script_text:
        errors.append(
            "download_model.sh must validate the GGUF model"
        )

if errors:
    print("Submission preflight: INCOMPLETE")

    for error in errors:
        print(f"- {error}")

    raise SystemExit(1)

print("Submission preflight: PASS")
