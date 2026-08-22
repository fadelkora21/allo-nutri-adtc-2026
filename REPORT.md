# ALLO NUTRI — ADTC 2026 Technical Report

**Team ID:** allo-nutri-feed-formulator  
**Domain:** Agriculture  
**Model:** Qwen2.5 1.5B Instruct Q4_K_M GGUF  
**Measured parameter count:** 1,777,088,000  
**Runtime:** llama.cpp  
**Target environment:** 4 CPU cores, 8 GB RAM, integrated graphics  

---

## 1. Problem

Smallholder poultry farmers in Benin and other West African countries face frequent changes in the price and availability of feed ingredients. Maize and soybean meal are particularly vulnerable to drought, irregular rainfall, seasonal shortages and market-price fluctuations.

Feed represents a major part of poultry-production costs. When conventional ingredients become expensive or unavailable, farmers often substitute cheaper local ingredients without knowing their safe inclusion limits or their effects on energy, protein, minerals and antinutritional factors.

Professional feed-formulation tools are often expensive, dependent on stable internet access or designed for nutrition specialists. Many smallholder farmers therefore continue using fixed recipes that do not adapt to locally available ingredients, current prices or production phases.

ALLO NUTRI addresses this problem by providing an offline-first, least-cost poultry-feed formulation and explanation system designed for constrained African environments.

Its initial target users are smallholder poultry farmers raising approximately 50 to 500 birds in Benin.

## 2. Solution

ALLO NUTRI allows the user to:

- select locally available feed ingredients;
- enter ingredient prices and availability;
- choose the poultry-production phase;
- define the required ration weight;
- calculate a nutritionally constrained least-cost formula;
- identify nutritional deficiencies and unsafe ingredient levels;
- receive a simple offline explanation in French, English or Hausa.

The prototype separates mathematical formulation from natural-language explanation.

A deterministic linear-programming optimizer calculates ingredient quantities and verifies nutritional constraints. The local language model explains the verified results but cannot independently change the calculated quantities.

This separation reduces the risk of hallucinated formulas and makes the numerical results auditable.

## 3. Cross-Disciplinary Integration

The system combines four disciplines:

1. **Poultry nutrition** for nutrient requirements, ingredient composition, phase-specific limits and antinutritional-factor warnings.
2. **Operations research** for least-cost linear optimization.
3. **Software engineering** for the offline application and local browser interface.
4. **On-device artificial intelligence** for multilingual explanations without a cloud API.

This integration is load-bearing because the language model alone cannot safely formulate poultry feed, while the optimizer alone cannot easily explain technical results to farmers in accessible language.

## 4. Design Decisions

### 4.1 Base Model

The prototype uses Qwen2.5 1.5B Instruct.

The GGUF metadata reports an actual parameter count of 1,777,088,000, represented as approximately 1.8B in the submission metadata.

The model was selected because it offers:

- a relatively small parameter count;
- multilingual instruction-following capability;
- compatibility with llama.cpp;
- availability in GGUF format;
- a memory profile appropriate for an 8 GB laptop;
- sufficient capability for short agricultural explanations.

### 4.2 Quantization

The selected weight file uses GGUF Q4_K_M quantization.

Q4_K_M was chosen as a practical balance between:

- model size;
- memory consumption;
- CPU inference speed;
- response quality.

Larger models and higher-precision quantizations were not selected for the Gate 1 prototype because they would increase memory use and inference latency on the target 8 GB laptop.

More aggressive quantization could reduce memory consumption further but may reduce the quality of multilingual and technical explanations.

### 4.3 Runtime

The model runs through llama.cpp.

The application does not call a cloud model or external inference API. After the model has been downloaded, inference can run without an internet connection.

### 4.4 Deterministic Optimizer

The optimizer uses linear programming through SciPy and HiGHS.

The optimization layer handles:

- ration mass balance;
- metabolizable energy;
- crude protein;
- lysine;
- methionine;
- calcium;
- available phosphorus;
- fibre;
- ingredient availability;
- phase-specific inclusion limits;
- least-cost selection.

The language model receives the optimizer’s verified result and produces a short explanation. It is instructed not to modify quantities or invent a new formula.

## 5. African Context

ALLO NUTRI was designed around conditions experienced by poultry farmers in Benin:

- unstable feed-ingredient prices;
- limited access to animal-nutrition specialists;
- inconsistent internet connectivity;
- use of locally available alternative ingredients;
- small and medium flock sizes;
- need for French and local-language explanations;
- reliance on affordable consumer laptops.

Hausa support is included because Hausa is used in commercial and agricultural exchanges across northern Benin and neighbouring West African areas.

The system’s offline architecture reduces dependence on internet connectivity and recurring cloud-AI fees.

## 6. Safety and Reliability

The prototype applies the following safeguards:

- the language model does not calculate ingredient quantities;
- optimizer results remain the numerical source of truth;
- nutritional constraints are checked before approval;
- phase-specific ingredient ceilings are enforced;
- cottonseed cake triggers a gossypol-related warning;
- ferrous-sulfate dosage is not guessed without measured free-gossypol data;
- invalid or infeasible ingredient selections generate an error;
- field deployment requires locally validated ingredient-composition data.

The current ingredient values are suitable for prototype evaluation. Commercial deployment will require calibration using reliable local feed tables and laboratory analyses.

## 7. Technical Constraints

The project was designed for:

- Ubuntu 22.04 or later;
- four CPU cores;
- 8 GB RAM;
- integrated graphics;
- CPU-based inference;
- intermittent internet access;
- complete offline operation during inference.

The model file is not stored in Git. The public `download_model.sh` script downloads it without credentials and verifies the GGUF header.

The application is served locally through `127.0.0.1` and does not expose the service to an external network by default.

## 8. Validation

The repository preflight validator checks:

- the required submission files;
- the Devpost Project ID;
- the agriculture domain;
- the two required test prompts;
- the llama.cpp runtime;
- the model path;
- placeholder values;
- the model exclusions in `.gitignore`;
- the model-download script.

The application’s automated tests verify:

- balanced starter-ration formulation;
- ration scaling to 50 kg;
- invalid ingredient-selection handling;
- Hausa localisation.

The current automated-test result is:

```text
Ran 4 tests
OK
