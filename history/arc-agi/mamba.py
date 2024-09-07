from transformers import AutoTokenizer, AutoModelForCausalLM

messages = [
    {"role": "user", "content": open("mini").read()},
]

tokenizer = AutoTokenizer.from_pretrained("state-spaces/mamba-130m-hf")
pipe = AutoModelForCausalLM.from_pretrained("state-spaces/mamba-130m-hf")
pipe(messages)
