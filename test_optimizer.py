import unittest

from app import offline_advice
from optimizer import FormulationError, formulate


class OptimizerTests(unittest.TestCase):
    def test_balanced_starter_formula(self):
        selections = [{"key": k, "price": p, "available": 100} for k, p in {
            "maize": 250, "soybean_meal": 520, "fish_meal": 900,
            "limestone": 100, "bone_meal": 200, "oil": 800,
            "dl_methionine": 3500, "l_lysine": 3000,
        }.items()]
        result = formulate("starter", 100, selections)
        self.assertAlmostEqual(sum(x["kg"] for x in result["quantities"]), 100, places=5)
        self.assertGreaterEqual(result["nutrients"]["cp"], 22)
        self.assertGreaterEqual(result["nutrients"]["me"], 3000)
        self.assertLessEqual(result["nutrients"]["ca"], 1.10 + 1e-6)

    def test_insufficient_ingredients(self):
        with self.assertRaises(FormulationError):
            formulate("starter", 100, [{"key": "maize", "price": 1, "available": 100}])

    def test_scales_to_50kg(self):
        selections = [{"key": k, "price": 1, "available": 100} for k in ["maize", "soybean_meal", "fish_meal", "limestone", "bone_meal", "oil", "dl_methionine", "l_lysine"]]
        result = formulate("grower", 50, selections)
        self.assertAlmostEqual(sum(x["kg"] for x in result["quantities"]), 50, places=5)

    def test_hausa_localisation(self):
        result = {"nutrients": {"me": 3000, "cp": 22, "ca": .9, "avp": .45}, "quantities": [{"name": "Maïs", "kg": 60}]}
        text = offline_advice(result, "ha")
        self.assertIn("Wannan haɗin", text)
        self.assertIn("3000", text)


if __name__ == "__main__": unittest.main()
