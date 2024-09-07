import sys
import json

if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    exit()

fn = sys.argv[1]
data = json.load(open(fn))

LOOKUP = [
    "➓➊➋➌➍➎➏➐➑➒",
    "➉➀➁➂➃➄➅➆➇➈"
]

def make_line(data):
    # ~ print(data)
    res = '\n'
    fn = lambda x, v: str(v)
    for r, i in enumerate(data):
        for c, j in enumerate(i):
            l = 1 if ((r % 2) + (c % 2)) % 2 == 0 else 0
            res += LOOKUP[l][j]
        res += '✂\n'
    # ~ print(res)
    # ~ exit()
    return res

print('Train:')
for i, d in enumerate(data['train']):
    print(f" Question {i}: ")
    print(make_line(d['input']))
    print(f" Answer {i}:")
    print(make_line(d['output']))
print('Test:')
for d in data['test']:
    print(" Question: ")
    print(make_line(d['input']))
    print(" Answer:")
    print(make_line(d['output']))
