# ALLO NUTRI — ADTC 2026 Gate 1 Report (draft)

## Problem

Smallholder poultry farmers in Benin face volatile feed prices, unreliable connectivity, and limited access to nutritionists. Fixed recipes do not adapt to locally available ingredients and may ignore nutritional or antinutritional constraints.

## Solution

ALLO NUTRI is an offline-first least-cost feed formulator. Farmers select available ingredients, local prices, quantities, and the birds' growth phase. A deterministic linear optimizer produces a nutritionally constrained formula. A compact local language model explains the result in accessible language; it never determines ingredient quantities.

## Cross-disciplinary integration

The system combines poultry nutrition, operations research, local agricultural data, and on-device language-model inference. This separation improves safety: numerical constraints are auditable, while the LLM handles interaction and explanation.

## Constraints and design decisions

- Runs locally with no cloud API.
- Browser interface served only on `127.0.0.1`.
- Linear programming through SciPy/HiGHS.
- Optional GGUF model through `llama.cpp`.
- Target: Ubuntu 22.04, 4 CPU cores, 8 GB RAM, integrated graphics.
- LLM target must remain below the challenge's 7 GB inference ceiling.

## Current prototype

- Broiler starter, grower, and finisher profiles.
- Fourteen locally relevant ingredient categories, including amino-acid supplements.
- Price and availability inputs.
- Energy, protein, lysine, methionine, calcium, available phosphorus, and fibre constraints.
- Phase-specific inclusion limits and cottonseed/gossypol safety warning.
- French, English, and meaningful Hausa offline explanations.
- Public evaluation prompts for nutritional safety, gossypol, and localisation.

## Validation status

Automated tests verify mass balance, nutrient minima, calcium ceiling, invalid selection handling, and ration scaling. Ingredient composition values remain provisional and must be replaced or calibrated with laboratory and locally sourced data before field use.

## Gate 1 work remaining

1. Download the documented Qwen2.5 1.5B Instruct Q4_K_M candidate and reconfirm its current licence.
2. Run the official ADTC profiler on Ubuntu target hardware.
3. Record throughput, peak RAM, and thermal results.
4. Add screenshots and record the prepared two-minute demonstration.

## Model candidate

Qwen2.5 1.5B Instruct, Q4_K_M GGUF, was selected as the preflight candidate because it is compact, multilingual and supported by `llama.cpp`. The model weights are not redistributed with the source package. Final submission metadata must include the exact upstream revision, file hash and current licence after download.

## Reproducibility package

The repository follows the official Gate 1 structure: `metadata.json` declares the agriculture domain, exactly two public prompts, three language codes, the `llama.cpp` runtime, Q4_K_M quantization and the expected model path. `download_model.sh` is credential-free, resumable, idempotent and checks the GGUF magic header before publishing the downloaded file. Large weights and profiler outputs are excluded from version control.
