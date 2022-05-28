import torch
from transformers import AutoTokenizer,AutoModelForSequenceClassification,pipeline
tokenizer = AutoTokenizer.from_pretrained("roberta-base")
model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased")


feature_extractor = pipeline('feature-extraction', model=model, tokenizer= tokenizer)



text = "This is a sample text a feature should be extracted from"
encoded = tokenizer.encode_plus(
    text=text, 
    add_special_tokens=True,
    max_length = 64, 
    pad_to_max_length=True,
    return_attention_mask = True,
    truncation=True, 
    return_tensors = 'pt',
)


feature_extractor(encoded) # Here encoded input is suplied to the pipeline 