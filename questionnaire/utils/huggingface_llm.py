<<<<<<< HEAD
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Your model's name on Hugging Face
MODEL_NAME = "Lolity/results"

# Load model and tokenizer from Hugging Face
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(**inputs, max_length=200)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response
=======
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch

# # Your model's name on Hugging Face
# MODEL_NAME = "Lolity/results"

# # Load model and tokenizer from Hugging Face
# tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# def generate_response(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt")
#     output = model.generate(**inputs, max_length=200)
#     response = tokenizer.decode(output[0], skip_special_tokens=True)
#     return response
>>>>>>> 9bb57c1 (Updated project files with latest changes)
