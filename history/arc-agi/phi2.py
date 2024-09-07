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
    problem.append(" Question: ")
    problem.append(make_line(d['input']))
    problem.append(" Answer:")
    #problem.append(make_line(d['output']))
    print(make_line(d['output']))
    print("------------------------------------------------------------------------------")

query = "\n".join(problem)

# Load the configuration
config = AutoConfig.from_pretrained(
  "microsoft/phi-2",
  max_new_tokens=1024
)

# Load the tokenizer and model using the model name, not the config
tokenizer = AutoTokenizer.from_pretrained("microsoft/phi-2")
model = AutoModelForCausalLM.from_pretrained("microsoft/phi-2", config=config)

meta = open("meta-new3").read()

prompt = meta + "\n" + query + "\n"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
generate_ids = model.generate(inputs.input_ids, max_length=10240)
res = tokenizer.batch_decode(generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)

print(res)
