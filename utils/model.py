# utils/model.py
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    # Mean pooling to obtain a fixed-size vector
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.numpy()[0]
