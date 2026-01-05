import math
import torch
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

def ai_likelihood(text):
    if not text or len(text.strip()) < 30:
        return "Low"

    enc = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    with torch.no_grad():
        loss = model(**enc, labels=enc["input_ids"]).loss

    perplexity = math.exp(loss.item())

    if perplexity < 40:
        return "High"
    elif perplexity < 70:
        return "Moderate"
    else:
        return "Low"
