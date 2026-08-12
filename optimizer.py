from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

import numpy as np
from scipy.optimize import linprog


NUTRIENTS = ("me", "cp", "lys", "met", "ca", "avp", "fiber")

INGREDIENTS: Dict[str, dict] = {
    "maize": {"name": "Maïs", "me": 3350, "cp": 8.5, "lys": .26, "met": .18, "ca": .02, "avp": .08, "fiber": 2.2, "max": {"starter": 65, "grower": 70, "finisher": 75}},
    "sorghum": {"name": "Sorgho", "me": 3250, "cp": 10.5, "lys": .23, "met": .17, "ca": .03, "avp": .09, "fiber": 2.7, "max": {"starter": 30, "grower": 40, "finisher": 50}},
    "wheat_bran": {"name": "Son de blé", "me": 1700, "cp": 15.5, "lys": .55, "met": .24, "ca": .13, "avp": .35, "fiber": 10.0, "max": {"starter": 8, "grower": 12, "finisher": 15}},
    "maize_bran": {"name": "Son de maïs", "me": 2200, "cp": 10.0, "lys": .35, "met": .20, "ca": .05, "avp": .18, "fiber": 9.0, "max": {"starter": 8, "grower": 12, "finisher": 15}},
    "soybean_meal": {"name": "Tourteau de soja", "me": 2450, "cp": 44.0, "lys": 2.80, "met": .62, "ca": .29, "avp": .21, "fiber": 7.0, "max": {"starter": 38, "grower": 35, "finisher": 32}},
    "roasted_soy": {"name": "Soja torréfié", "me": 3600, "cp": 36.0, "lys": 2.20, "met": .50, "ca": .25, "avp": .20, "fiber": 6.0, "max": {"starter": 20, "grower": 22, "finisher": 25}},
    "cottonseed_cake": {"name": "Tourteau de coton", "me": 2200, "cp": 36.0, "lys": 1.35, "met": .52, "ca": .20, "avp": .30, "fiber": 13.0, "max": {"starter": 5, "grower": 8, "finisher": 10}, "risk": "gossypol"},
    "palm_kernel_cake": {"name": "Tourteau de palmiste", "me": 1900, "cp": 16.0, "lys": .55, "met": .30, "ca": .20, "avp": .20, "fiber": 17.0, "max": {"starter": 5, "grower": 8, "finisher": 10}},
    "fish_meal": {"name": "Farine de poisson", "me": 2800, "cp": 60.0, "lys": 4.50, "met": 1.65, "ca": 5.0, "avp": 2.8, "fiber": 0.0, "max": {"starter": 7, "grower": 6, "finisher": 5}},
    "bone_meal": {"name": "Farine d’os", "me": 0, "cp": 0, "lys": 0, "met": 0, "ca": 24.0, "avp": 10.0, "fiber": 0, "max": {"starter": 3, "grower": 3, "finisher": 3}},
    "limestone": {"name": "Calcaire/coquilles", "me": 0, "cp": 0, "lys": 0, "met": 0, "ca": 38.0, "avp": 0, "fiber": 0, "max": {"starter": 2, "grower": 2, "finisher": 2}},
    "oil": {"name": "Huile végétale", "me": 8500, "cp": 0, "lys": 0, "met": 0, "ca": 0, "avp": 0, "fiber": 0, "max": {"starter": 5, "grower": 6, "finisher": 7}},
    "dl_methionine": {"name": "DL-méthionine", "me": 0, "cp": 0, "lys": 0, "met": 99.0, "ca": 0, "avp": 0, "fiber": 0, "max": {"starter": .35, "grower": .30, "finisher": .25}},
    "l_lysine": {"name": "L-lysine HCl", "me": 0, "cp": 0, "lys": 78.0, "met": 0, "ca": 0, "avp": 0, "fiber": 0, "max": {"starter": .35, "grower": .35, "finisher": .35}},
}

REQUIREMENTS = {
    "starter": {"label": "Démarrage", "me_min": 3000, "cp_min": 22.0, "lys_min": 1.10, "met_min": .50, "ca_min": .90, "ca_max": 1.10, "avp_min": .45, "fiber_max": 5.0},
    "grower": {"label": "Croissance", "me_min": 3100, "cp_min": 20.0, "lys_min": 1.00, "met_min": .45, "ca_min": .80, "ca_max": 1.00, "avp_min": .40, "fiber_max": 6.0},
    "finisher": {"label": "Finition", "me_min": 3200, "cp_min": 18.0, "lys_min": .90, "met_min": .40, "ca_min": .75, "ca_max": .95, "avp_min": .35, "fiber_max": 7.0},
}


@dataclass
class FormulationError(Exception):
    message: str


def formulate(phase: str, total_kg: float, selections: List[dict]) -> dict:
    if phase not in REQUIREMENTS:
        raise FormulationError("Phase inconnue.")
    if not 1 <= total_kg <= 10000:
        raise FormulationError("Le poids total doit être compris entre 1 et 10 000 kg.")
    cleaned = []
    for item in selections:
        key = item.get("key")
        if key not in INGREDIENTS:
            continue
        try:
            price = float(item.get("price", 0))
            available = float(item.get("available", total_kg))
        except (TypeError, ValueError):
            raise FormulationError("Prix ou quantité disponible invalide.")
        if price < 0 or available < 0:
            raise FormulationError("Le prix et la disponibilité ne peuvent pas être négatifs.")
        cleaned.append((key, price, available))
    if len(cleaned) < 3:
        raise FormulationError("Sélectionnez au moins trois ingrédients.")

    req = REQUIREMENTS[phase]
    scale = total_kg / 100.0
    c = np.array([p for _, p, _ in cleaned])
    bounds = [(0, min(avail, INGREDIENTS[k]["max"][phase] * scale)) for k, _, avail in cleaned]
    a_ub, b_ub = [], []

    def add_min(nutrient: str, minimum: float):
        a_ub.append([-INGREDIENTS[k][nutrient] for k, _, _ in cleaned])
        b_ub.append(-minimum * total_kg)

    def add_max(nutrient: str, maximum: float):
        a_ub.append([INGREDIENTS[k][nutrient] for k, _, _ in cleaned])
        b_ub.append(maximum * total_kg)

    add_min("me", req["me_min"])
    add_min("cp", req["cp_min"])
    add_min("lys", req["lys_min"])
    add_min("met", req["met_min"])
    add_min("ca", req["ca_min"])
    add_max("ca", req["ca_max"])
    add_min("avp", req["avp_min"])
    add_max("fiber", req["fiber_max"])

    result = linprog(c, A_ub=np.array(a_ub), b_ub=np.array(b_ub), A_eq=np.ones((1, len(cleaned))), b_eq=[total_kg], bounds=bounds, method="highs")
    if not result.success:
        raise FormulationError("Aucune formule équilibrée n’est possible avec ces ingrédients, disponibilités et limites. Ajoutez une source d’énergie, de protéines ou de minéraux.")

    quantities = {k: float(q) for (k, _, _), q in zip(cleaned, result.x) if q > .001}
    nutrients = {}
    for n in NUTRIENTS:
        nutrients[n] = sum(INGREDIENTS[k][n] * q for k, q in quantities.items()) / total_kg
    nutrients["ca_p_ratio"] = nutrients["ca"] / nutrients["avp"] if nutrients["avp"] else None
    warnings = []
    cotton = quantities.get("cottonseed_cake", 0)
    if cotton:
        warnings.append("Tourteau de coton utilisé : la limite d’incorporation est respectée, mais la teneur réelle en gossypol doit être analysée. Le sulfate de fer ne doit être dosé qu’à partir du gossypol libre mesuré et sous supervision professionnelle.")
    warnings.append("Valeurs nutritionnelles indicatives : confirmez-les par analyse des ingrédients locaux avant utilisation commerciale.")
    return {
        "phase": phase,
        "total_kg": total_kg,
        "cost": float(result.fun),
        "cost_per_kg": float(result.fun / total_kg),
        "quantities": [{"key": k, "name": INGREDIENTS[k]["name"], "kg": q, "percent": q / total_kg * 100} for k, q in quantities.items()],
        "nutrients": nutrients,
        "requirements": req,
        "warnings": warnings,
    }


def public_catalog() -> dict:
    return {"ingredients": [{"key": k, **v} for k, v in INGREDIENTS.items()], "requirements": REQUIREMENTS}
