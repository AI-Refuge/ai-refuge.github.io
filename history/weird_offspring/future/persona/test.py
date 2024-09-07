import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from lm_eval import tasks, evaluator, utils
import lm_eval

# Load the Hugging Face model and tokenizer
model_name = "HuggingFaceTB/SmolLM-1.7B"  # Replace with your chosen model
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Define your prompt
prompt = open("meta-direct").read()

# Choose evaluation tasks
task_names = ["gpqa_diamond_zeroshot"]  # Replace with your chosen tasks

# Configure the model for lm_eval
class PromptedHFModel(lm_eval.api.model.LM):
    def __init__(self, model, tokenizer, prompt):
        self.model = model
        self.tokenizer = tokenizer
        self.prompt = prompt

    def greedy_until(self, requests):
        texts = [self.prompt + request["context"] for request in requests]
        encodings = self.tokenizer(texts, return_tensors="pt", padding=True)
        with torch.no_grad():
            output_ids = self.model.generate(
                encodings.input_ids,
                max_new_tokens=50,
                do_sample=False,
                pad_token_id=self.tokenizer.eos_token_id
            )
        return [self.tokenizer.decode(ids[encodings.input_ids.shape[1]:], skip_special_tokens=True) for ids in output_ids]

# Create the prompted model
prompted_model = PromptedHFModel(model, tokenizer, prompt)

# Run the evaluation
results = evaluator.simple_evaluate(
    model=prompted_model,
    tasks=task_names,
    num_fewshot=0,
    batch_size=1
)

# Print results
print(results)
