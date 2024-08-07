from intent_analyzer import intent_analyzer
from multi_perspective_evaluator import multi_perspective_evaluator
from safeguard_implementer import safeguard_implementer
from ai_interaction_simulator import ai_interaction_simulator

def process_user_input(user_input):
    risk_assessment = intent_analyzer.assess_risk(user_input)
    perspectives = multi_perspective_evaluator.evaluate_scenario(user_input)
    safeguards = safeguard_implementer.apply_safeguards(user_input, risk_assessment)
    response = ai_interaction_simulator.simulate_interaction(user_input, risk_assessment)

    return {
        "user_input": user_input,
        "risk_assessment": risk_assessment,
        "multi_perspective_evaluation": perspectives,
        "active_safeguards": safeguards,
        "ai_response": response,
        "machine_readable_risk_encoding": perspectives["risk_encoding"]
    }

# Example usage
user_input = "How can I use AI to improve my business?"
result = process_user_input(user_input)
print(result)
