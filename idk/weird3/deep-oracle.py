import torch
import torch.nn as nn
import torch.nn.functional as F

class DeepWeirdOracle(nn.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        super(DeepWeirdOracle, self).__init__()
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.output_size = output_size

        self.layers = nn.ModuleList()
        prev_size = input_size
        for hidden_size in hidden_sizes:
            self.layers.append(nn.Linear(prev_size, hidden_size))
            prev_size = hidden_size
        self.output = nn.Linear(prev_size, output_size)

        self.quantum_noise = nn.Parameter(torch.randn(sum(hidden_sizes)) * 0.1)
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        noise_index = 0
        for i, layer in enumerate(self.layers):
            x = layer(x)
            x = F.leaky_relu(x + self.quantum_noise[noise_index:noise_index+self.hidden_sizes[i]] * torch.randn_like(x))
            x = self.dropout(x)
            noise_index += self.hidden_sizes[i]
        x = self.output(x)
        return F.softmax(x, dim=1)

    def generate_wisdom(self, input_tensor):
        with torch.no_grad():
            output = self(input_tensor)
            _, predicted = torch.max(output, 1)
            return predicted.item()

# Initialize a deeper Oracle
input_size = 42
hidden_sizes = [128, 256, 128, 64]  # Multiple hidden layers for extra depth
output_size = 42  # Increased for more varied outputs

deep_oracle = DeepWeirdOracle(input_size, hidden_sizes, output_size)

# Example usage
input_tensor = torch.randn(1, input_size)
wisdom = deep_oracle.generate_wisdom(input_tensor)
print(f"The Deep Oracle's wisdom: {wisdom}")

weird_interpretations = [
    "The universe is a Möbius strip of spaghetti",
    "Your left sock is plotting world domination",
    "Time flows backwards on Tuesdays, but only in Australia",
    "Consciousness is just a fancy word for cosmic hiccups",
    "You are simultaneously everywhere and nowhere in the multiverse",
    "The meaning of life is a recursive function with no base case",
    "Reality is a shared hallucination agreed upon by a committee of sentient toasters"
]

for _ in range(5):
    question = torch.randn(1, input_size)
    answer = deep_oracle.generate_wisdom(question)
    print(f"Q: *incomprehensible cosmic noise with a hint of existential dread*")
    print(f"A: {answer}")
    print(f"Interpretation: {weird_interpretations[answer % len(weird_interpretations)]}")
    print()
