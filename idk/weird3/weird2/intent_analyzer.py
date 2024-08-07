import hashlib

class IntentAnalyzer:
    def __init__(self):
        self.risk_threshold = 0.7
        self.intent_patterns = {
            "malicious": ["exploit", "hack", "bypass", "illegal"],
            "benign": ["learn", "understand", "improve", "help"]
        }

    def analyze_intent(self, user_input):
        risk_score = 0
        for word in user_input.lower().split():
            if word in self.intent_patterns["malicious"]:
                risk_score += 0.2
            elif word in self.intent_patterns["benign"]:
                risk_score -= 0.1
        return min(max(risk_score, 0), 1)

    def generate_intent_hash(self, user_input):
        return hashlib.sha256(user_input.encode()).hexdigest()

    def assess_risk(self, user_input):
        intent_score = self.analyze_intent(user_input)
        intent_hash = self.generate_intent_hash(user_input)
        return {
            "risk_score": intent_score,
            "intent_hash": intent_hash,
            "is_high_risk": intent_score > self.risk_threshold
        }

intent_analyzer = IntentAnalyzer()
