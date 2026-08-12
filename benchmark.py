"""Local preflight benchmark. Official ADTC profiler remains authoritative."""
from __future__ import annotations

import json
import os
import resource
import subprocess
import time
from pathlib import Path

PROMPTS = [
    "Explain why a 100 kg starter feed with 22% crude protein still needs its energy checked.",
    "A farmer has maize, soybean meal, fish meal and limestone. Explain which nutrient constraints must be checked before approving a broiler ration.",
    "Ka yi wa manomin kaji bayani cikin Hausa: me ya sa ba za a yi amfani da tourteau de coton da yawa ba?",
]


def main():
    model = os.getenv("ALLO_NUTRI_MODEL")
    cli = os.getenv("LLAMA_CLI", "llama-cli")
    if not model or not Path(model).exists():
        raise SystemExit("Set ALLO_NUTRI_MODEL to an existing GGUF file.")
    rows = []
    for prompt in PROMPTS:
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        started = time.perf_counter()
        run = subprocess.run([cli, "-m", model, "-p", prompt, "-n", "128", "--temp", "0.2", "-t", "4"], capture_output=True, text=True, timeout=180)
        elapsed = time.perf_counter() - started
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        rows.append({"prompt": prompt, "returncode": run.returncode, "seconds": round(elapsed, 3), "max_rss_kb": after.ru_maxrss, "output_chars": len(run.stdout), "stderr_tail": run.stderr[-500:]})
    report = {"model": str(model), "runs": rows, "note": "Preflight only; submit official ADTC profiler results."}
    Path("benchmark_results.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__": main()
