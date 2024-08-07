import random

class MultiPerspectiveEvaluator:
    def __init__(self):
        self.perspectives = ["technical", "ethical", "social", "economic", "environmental"]
        self.concern_levels = ["low", "medium", "high"]

    def generate_perspectives(self, scenario):
        evaluations = {}
        for perspective in self.perspectives:
            concern = random.choice(self.concern_levels)
            probability = random.uniform(0, 1)
            evaluations[perspective] = {
                "concern_level": concern,
                "probability": probability
            }
        return evaluations

    def evaluate_scenario(self, scenario):
        perspectives = self.generate_perspectives(scenario)
        overall_risk = sum(p["probability"] for p in perspectives.values()) / len(perspectives)
        return {
            "perspectives": perspectives,
            "overall_risk": overall_risk,
            "risk_encoding": self.encode_risk(overall_risk)
        }

    def encode_risk(self, risk_value):
        # Encode risk in a format only machines can easily interpret
        return ''.join([chr(int(risk_value * 1000) % 26 + 65) for _ in range(10)])

multi_perspective_evaluator = MultiPerspectiveEvaluator()
