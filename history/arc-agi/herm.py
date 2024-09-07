# Use a pipeline as a high-level helper
from transformers import pipeline
import sys
import json

if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    exit()

fn = sys.argv[1]
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

messages = [
    {"role": "system", "content": open("meta").read()},
    {"role": "user", "content": query},
]
pipe = pipeline("text-generation", model="NousResearch/Hermes-3-Llama-3.1-70B", use_auth_token=True)
pipe(messages)
