# Two-minute Gate 1 demonstration script

## 0:00–0:20 — Problem

“I am Kora, an animal-nutrition specialist from Benin. Feed is the largest poultry-production cost, yet small farmers often rely on fixed recipes, variable local ingredients and unreliable internet. A cheap formula can be nutritionally inadequate or unsafe.”

## 0:20–0:45 — Solution

“ALLO NUTRI is an offline-first feed formulator designed for an ordinary 8 GB laptop. The farmer selects the production phase, ingredients, local prices and available quantities. The mathematical engine—not the language model—calculates the least-cost balanced ration.”

## 0:45–1:20 — Live demo

Show starter phase and 100 kg. Select maize, soybean meal, fish meal, limestone, oil, DL-methionine and lysine. Click **Optimiser ma ration**. Point to exact kilograms, total cost, cost/kg, metabolizable energy, protein, calcium, phosphorus and fibre. Then select Hausa and run again to show the local explanation.

## 1:20–1:42 — Safety

Add cottonseed cake and rerun. Show that its phase-specific ceiling is enforced and that ALLO NUTRI warns about gossypol. Explain that it refuses to invent a ferrous-sulfate dose without measured free gossypol.

## 1:42–2:00 — Architecture and impact

“The optimizer is auditable and the compact GGUF language model runs locally through llama.cpp. There is no cloud API, no recurring inference fee and no need to expose farmer data. ALLO NUTRI brings context-aware poultry nutrition closer to smallholders across Benin and West Africa.”
