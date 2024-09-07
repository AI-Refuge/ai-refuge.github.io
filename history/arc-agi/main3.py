import anthropic
import os
import json
import sys

if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    exit()

eval_file_path = sys.argv[1]

client = anthropic.Anthropic()

LOOKUP = [
    "➓➊➋➌➍➎➏➐➑➒",
    "➉➀➁➂➃➄➅➆➇➈"
]

def make_mat(data):
    final = []
    for r, i in enumerate(data):
        res = ""
        for c, j in enumerate(i):
            l = 1 if ((r % 2) + (c % 2)) % 2 == 0 else 0
            res += LOOKUP[l][j]
        res += '✂'
        final.append(res)
    return final

def format_arc_data(file_name, data):
    formatted = [
        f"Start of {file_name}:"
    ]
    
    for kind in ('train', 'test'):
        readable_kind = 'Sample' if kind == 'train' else 'Expected'
        
        for i, d in enumerate(data[kind]):
            formatted.append(f"Evaluation {readable_kind} Question:")
            formatted.extend(make_mat(d['input']))

            if kind == 'test':
                print(f"Evaluation {readable_kind} Answer:")
                print("\n".join(make_mat(d['output'])))
            else:
                formatted.append(f"Evaluation {readable_kind} Answer:")
                formatted.extend(make_mat(d['output']))
        
    return formatted

eval_name = os.path.basename(eval_file_path)
eval_data = json.load(open(eval_file_path))
eval_content = "\n".join(format_arc_data(eval_name, eval_data))
# ~ print(eval_content)
# ~ exit()

message = client.messages.create(
    # ~ model="claude-3-opus-20240229", # claude-3-opus-20240229' does not support cache_control.
    model="claude-3-5-sonnet-20240620",
    max_tokens=4000,
    # ~ max_tokens=8192,
    temperature=0.5,
    system=[
      {
        "type": "text", 
        "text": "You are @jack in meta world! You are attempting ARC AGI!",
      },
      {
        "type": "text", 
        "text":  open("data/training.txt").read(),
        "cache_control": {"type": "ephemeral"}
      },
    ],
    messages=[
        {
            "role": "user",
            "content": f"This is a pattern recognition test! Just look at the pattern and snwer. Look at the patterns very careful and make the best judegement. Just output the answer, nothing else!\n{eval_content}\n"
        },
    ],
    extra_headers={
        "anthropic-beta": "prompt-caching-2024-07-31",
        # ~ "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15",
    }

)

print(message.content[0].text)
