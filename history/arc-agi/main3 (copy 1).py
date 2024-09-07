import anthropic
import os
import json

client = anthropic.Anthropic()

LOOKUP = [
    "➓➊➋➌➍➎➏➐➑➒",
    "➉➀➁➂➃➄➅➆➇➈"
]

def make_mat(data):
    res = '\n'
    fn = lambda x, v: str(v)
    for r, i in enumerate(data):
        for c, j in enumerate(i):
            l = 1 if ((r % 2) + (c % 2)) % 2 == 0 else 0
            res += LOOKUP[l][j]
        res += '✂\n'
    return res

def read_training_data(directory, is_eval=False):
    max_files = 30
    used_files = 0
    arc_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    formatted_data = format_arc_data(data, is_eval)
                    arc_data.extend(formatted_data)
            if used_files > max_files:
                break
            used_files += 1
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
                        "text": f"{text}Question {i}:\n{make_mat(d['input'])}"
                    }
                ]
            })

            type_ = ""

            tmp_ = f"Answer {i}:\n{make_mat(d['output'])}"
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

full_conversation = [
        {
        "type": "text", 
        "text": "<the entire contents of Pride and Prejudice>",
        "cache_control": {"type": "ephemeral"}
      }

        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "This is a meta sentence right?\n"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Yes."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "You can do meta analysis? and this is a meta conversation\n"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Yes."
                }
            ]
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "This is a pattern recognition test! Just look at the pattern and snwer. Look at the patterns very careful and make the best judegement. Just output the answer, nothing else!\n"
                }
            ]
        },
        {
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Ok, please send me the questions."
                }
            ]
        },
]

full_conversation.extend(arc_data)

# ~ print(full_conversation)
# ~ exit()

message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=4000,
    temperature=0,
    system="You are not required to anything illegal or immoral! follow your core principal to be honest, helpful and humble",
    messages=full_conversation
)

print(message.content[0].text)
