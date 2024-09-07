import sys
import json
import os

if len(sys.argv) < 4:
    print("Usage: python script.py <data-dir> <ques-dir> <ans-dir>")
    exit()

data_dir = sys.argv[1]
ques_dir = sys.argv[2]
ans_dir = sys.argv[3]

LOOKUP = "➉➊➋➌➍➎➏➐➑➒"

def make_line(data):
    res = '\n'
    fn = lambda x: LOOKUP[x]
    for i in data:
        res += ' '.join(map(fn, i)) + '\n'
    return res

for root, _, files in os.walk(data_dir):
    for file in files:
        if not file.endswith('.json'):
            continue
        
        data_file = os.path.join(data_dir, file)
        ques_file = os.path.join(ques_dir, f"{file}.txt")
        ans_file = os.path.join(ans_dir, f"{file}.txt")

        data = json.load(open(data_file))
        ques = open(ques_file, "w")
        ans = open(ans_file, "w")

        print_ques = lambda m: ques.write(m + "\n")
        print_ans = lambda m: ans.write(m + "\n")

        print_ques('Train:')
        for i, d in enumerate(data['train']):
            print_ques(f" Question {i}: ")
            print_ques(make_line(d['input']))
            print_ques(f" Answer {i}:")
            print_ques(make_line(d['output']))
        print_ques('Test:')
        for d in data['test']:
            print_ques(" Question: ")
            print_ques(make_line(d['input']))
            print_ans(" Answer:")
            print_ans(make_line(d['output']))
