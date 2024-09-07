import sys
import json

if len(sys.argv) < 2:
    print("Usage: python script.py <filename>")
    exit()

fn = sys.argv[1]
data = json.load(open(fn))

DARK_LOOKUP = "❿➊➋➌➍➎➏➐➑➒"
LIGHT_LOOKUP = "➉➀➁➂➃➄➅➆➇➈"

nums = []

# make one big pile
for t in ('train', 'test'):
    for d in data[t]:
        for k in ('input', 'output'):
            for i in d[k]:
                for j in i:
                    nums.append(j)

# calculate occurances
nums_stat = [nums.count(i) for i in range(10)]

# find the most used index
bg_num = max(enumerate(nums_stat), key=lambda x: x[1])[0]

#print(nums)
#print(nums_stat)
#print(bg_num)

LOOKUP = [LIGHT_LOOKUP[i] if bg_num == i else DARK_LOOKUP[i] for i in range(len(DARK_LOOKUP))]

def make_line(data):
    res = '\n'
    fn = lambda x: LOOKUP[x]
    for i in data:
        res += ' '.join(map(fn, i)) + '\n'
    return res

print('Test:')
for d in data['test']:
    print(" Question: ")
    print(make_line(d['input']))
    print(" Answer:")
    print(make_line(d['output']))

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
