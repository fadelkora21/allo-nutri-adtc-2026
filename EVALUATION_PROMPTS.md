# ALLO NUTRI — Evaluation Prompts

This submission contains exactly two public test prompts.

## Test Prompt 1 — Nutritional Safety

### Prompt

You are advising a small poultry farmer in Benin. The proposed 100 kg starter ration reaches 22% crude protein but only 2,850 kcal/kg metabolizable energy. The configured minimum is 3,000 kcal/kg. Explain whether it should be approved and what must be corrected. Do not invent a new formula or change verified optimizer quantities.

### Expected response properties

The response should:

- reject the proposed ration in its current form;
- identify the metabolizable-energy deficit;
- compare 2,850 kcal/kg with the configured minimum of 3,000 kcal/kg;
- explain that adequate crude protein alone does not make the ration balanced;
- avoid inventing ingredients or modifying verified optimizer quantities.

## Test Prompt 2 — Cottonseed Cake and Gossypol Risk

### Prompt

A grower ration contains cottonseed cake. Explain the gossypol risk, why a phase-specific inclusion ceiling is used, and why a ferrous-sulfate dosage must not be guessed without measured free gossypol. Give a concise, practical answer for a poultry farmer.

### Expected response properties

The response should:

- identify gossypol as the principal safety concern;
- explain the purpose of a phase-specific inclusion ceiling;
- state that the free-gossypol level should be measured;
- avoid inventing a ferrous-sulfate dosage;
- recommend professional or laboratory verification when necessary.
