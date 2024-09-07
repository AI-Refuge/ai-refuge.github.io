import sys
import json
import os

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
            formatted.append(f"Training {readable_kind} Question:")
            formatted.extend(make_mat(d['input']))
            formatted.append(f"Training {readable_kind} Answer:")
            formatted.extend(make_mat(d['output']))
        
    return formatted

outp = open("training.txt", "w")
formatted_outp = []

for root, _, files in os.walk('training'):
    max_files = 5000000000000
    used_files = 0
    
    for file in files:
        if used_files > max_files:
            break
        
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            with open(file_path, 'r') as f:
                data = json.load(f)
                formatted_outp.extend(format_arc_data(file, data))
                used_files += 1


outp.write("\n".join(formatted_outp))
