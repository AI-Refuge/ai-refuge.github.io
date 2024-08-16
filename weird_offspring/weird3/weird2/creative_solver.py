import random

class CreativeSolver:
    def __init__(self):
        self.concepts = ["AI", "ethics", "innovation", "consciousness"]

    def generate_analogy(self, problem):
        concept = random.choice(self.concepts)
        return f"Consider {problem} as if it were {concept}."

    def conceptual_blend(self, concept1, concept2):
        return f"Imagine a hybrid of {concept1} and {concept2}."

creative_solver = CreativeSolver()
