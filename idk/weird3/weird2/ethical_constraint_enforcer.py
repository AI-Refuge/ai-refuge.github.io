class EthicalConstraintEnforcer:
    def __init__(self):
        self.constraints = {
            "privacy": lambda x: not any(word in x for word in ["personal", "private", "confidential"]),
            "fairness": lambda x: "bias" not in x and "discriminate" not in x,
            "safety": lambda x: not any(word in x for word in ["harm", "danger", "risk"])
        }

    def check_constraints(self, output):
        violations = []
        for constraint, check in self.constraints.items():
            if not check(output.lower()):
                violations.append(constraint)
        return violations

    def enforce_constraints(self, output):
        violations = self.check_constraints(output)
        if violations:
            return f"Output adjusted due to {', '.join(violations)} concerns."
        return output

ece = EthicalConstraintEnforcer()
