# ALLO NUTRI Feed Formulator — ADTC 2026

ALLO NUTRI is an offline-first poultry-feed formulation prototype designed for smallholder farmers in Benin.

It combines:

- a deterministic least-cost feed optimizer;
- poultry nutritional and ingredient-safety constraints;
- a compact local GGUF language model;
- offline explanations in French, English and Hausa.

The language model explains verified optimizer results. It does not calculate or modify ingredient quantities.

## Submission information

- Project ID: `allo-nutri-feed-formulator`
- Domain: Agriculture
- Runtime: `llama.cpp`
- Model: Qwen2.5 1.5B Instruct
- Quantization: GGUF Q4_K_M
- Operation: 100% offline after model download

## Repository structure

```text
.
├── web/
│   └── index.html
├── app.py
├── optimizer.py
├── benchmark.py
├── download_model.sh
├── setup_model.sh
├── metadata.json
├── REPORT.md
├── EVALUATION_PROMPTS.md
├── requirements.txt
├── test_optimizer.py
└── validate_submission.py
```

The `model/` directory is created automatically by `download_model.sh`. Model weights are not committed to Git.

## System requirements

Recommended target environment:

- Ubuntu 22.04 or later
- 4 CPU cores
- 8 GB RAM
- Python 3.10 or later
- `curl`
- `git`
- `cmake`
- a C/C++ compiler

## Install Python dependencies

```bash
python3 -m pip install -r requirements.txt
```

## Download the model

Run:

```bash
bash download_model.sh
```

The script downloads the public GGUF model to:

```text
model/allo-nutri-qwen2.5-1.5b-q4_k_m.gguf
```

The script:

- requires no private credentials;
- creates the `model/` directory automatically;
- supports resumed downloads;
- verifies the GGUF file header;
- avoids downloading the model again when a valid file already exists.

## Install llama.cpp

For automatic local setup, run:

```bash
bash setup_model.sh
```

Then apply the environment variables displayed by the script, or define them manually:

```bash
export LLAMA_CLI="$PWD/llama.cpp/build/bin/llama-cli"
export ALLO_NUTRI_MODEL="$PWD/model/allo-nutri-qwen2.5-1.5b-q4_k_m.gguf"
```

## Run the application

```bash
python3 app.py
```

Open:

```text
http://127.0.0.1:8080
```

The application is served locally on `127.0.0.1` and does not require a cloud API.

## Run automated tests

```bash
python3 -m unittest -v test_optimizer.py
```

The tests verify:

- nutritional formulation feasibility;
- mass balance;
- ration-weight scaling;
- invalid ingredient-selection handling;
- Hausa localisation availability.

## Run repository preflight validation

```bash
python3 validate_submission.py
```

A valid repository should display:

```text
Submission preflight: PASS
```

## Run the official ADTC profiler

After downloading the model and installing the required profiler, run:

```bash
adtc-profiler run --submission . --mode participant --output submission.json --skip-accuracy
```

A valid profiling result must indicate:

```json
"measured_on": "participant_laptop"
```

The generated `submission.json` is excluded from Git.

## Safety notice

The prototype uses auditable numerical constraints, phase-specific ingredient limits and antinutritional-factor warnings.

Ingredient composition values must be calibrated with reliable local data or laboratory analyses before commercial field deployment. Final feeding decisions should remain under qualified animal-nutrition supervision.
