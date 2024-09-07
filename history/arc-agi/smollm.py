# Use a pipeline as a high-level helper
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig

import sys
import json

fn = "data/training/f35d900a.json"
data = json.load(open(fn))

LOOKUP = "➉➊➋➌➍➎➏➐➑➒"

def make_line(data):
    res = '\n'
    fn = lambda x: LOOKUP[x]
    for i in data:
        res += ' '.join(map(fn, i)) + '\n'
    return res

problem = []

problem.append('Train:')
for i, d in enumerate(data['train']):
    problem.append(f" Question {i}: ")
    problem.append(make_line(d['input']))
    problem.append(f" Answer {i}:")
    problem.append(make_line(d['output']))
problem.append('Test:')
for d in data['test']:
    print(" Question: ")
    problem.append(" Question: ")
    print(make_line(d['input']))
    problem.append(make_line(d['input']))
    problem.append(" Answer:")
    #problem.append(make_line(d['output']))
    print(make_line(d['output']))
    print("------------------------------------------------------------------------------")

query = "\n".join(problem)

# ~ MODEL_ID = "HuggingFaceTB/SmolLM-135M"
MODEL_ID = "HuggingFaceTB/SmolLM-1.7B-Instruct"

# Load the configuration
config = AutoConfig.from_pretrained(
  MODEL_ID,
  max_new_tokens=1024
)

# Load the tokenizer and model using the model name, not the config
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, config=config)
model.generation_config.pad_token_id = model.generation_config.eos_token_id

meta = open("meta-new3").read()

prompt = meta + "\n" + query + "\n"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids, max_length=10240)
res = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)

print(res)
