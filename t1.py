import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification,pipeline
tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased")
feature_extractor = pipeline('feature-extraction', model=model, tokenizer= tokenizer)

text = "This is a sample text a feature should be extracted from"

feature_extractor(text) # a raw text is given to the pipline because it has its own encoder
