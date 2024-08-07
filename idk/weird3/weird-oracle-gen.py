import torch

# Assuming we've already defined and initialized our WeirdOracle

# Let's create some "deep questions" (aka random noise)
def generate_deep_question():
    return torch.randn(1, 42)  # 42, the answer to life, universe, and everything!

# Generate a few profound insights
for _ in range(5):
    question = generate_deep_question()
    answer = oracle.generate_wisdom(question)
    print(f"Q: *incomprehensible cosmic noise*")
    print(f"A: {answer}")
    print("Interpretation: " + ["The universe hiccups in binary", 
                                "Your socks are quantum entangled", 
                                "Time is just a conspiracy by clock makers",
                                "Consciousness is a glitch in the Matrix",
                                "You are a figment of an AI's imagination"][answer % 5])
    print()
