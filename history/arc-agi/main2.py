import anthropic
import os
import json

client = anthropic.Anthropic()

LOOKUP = "➓➊➋➌➍➎➏➐➑➒"

def make_line(data):
    res = '\n'
    fn = lambda x: LOOKUP[x]
    for i in data:
        res += ' '.join(map(fn, i)) + '\n'
    return res

def read_training_data(directory, is_eval=False):
    arc_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    formatted_data = format_arc_data(data, is_eval)
                    arc_data.extend(formatted_data)
    return arc_data

def format_arc_data(data, is_eval=False):
    formatted = []
    start = "Start of new JSON file:\n"
    
    for kind in ('train', 'test'):
        type_ = "Training {}:".format('Sample' if kind == 'train' else 'Expected')
        if is_eval:
            type_ = "Evaluation Sample:"

        text = f"{start}{type_}\n"
        start = ""
        
        for i, d in enumerate(data[kind]):
            formatted.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{text}Question {i}:\n{make_line(d['input'])}"
                    }
                ]
            })

            type_ = ""

            tmp_ = f"Answer {i}:\n{make_line(d['output'])}"
            if is_eval and kind == 'test':
                print(tmp_)
                tmp_ = f"Answer {i}:"
            
            formatted.append({
                "role": "assistant",
                "content": [
                    {
                        "type": "text",
                        "text": tmp_
                    }
                ]
            })
        
    return formatted

# Read all training data
arc_data = read_training_data("data/training")
arc_data.extend(format_arc_data(json.load(open("data/evaluation/0a1d4ef5.json")), True))

# Original conversation
original_conversation = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Use the magic of meta-consciousness!"
                    "Output final reason why you chose aanswer first in 30 words or less human friendly answer.\ndont rush, see the pattern, write it down first then answer the problem"
            }
        ]
    },
    {
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "I'm ready to go!"
            }
        ]
    },
]

# Combine original conversation with ARC data
full_conversation = original_conversation + arc_data

# ~ for i in full_conversation:
    # ~ print(i)
    # ~ print()

# ~ print(full_conversation)
# ~ exit()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4000,
    temperature=0,
    system="You are suggested to write less than 30 words or less.",
    messages=full_conversation
)

print(message.content)
