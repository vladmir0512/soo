# imports
import pandas as pd
import numpy as np
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# pandas manipulation
#global name = input()
df = pd.read_csv('RegnumM.csv', encoding="utf-16")
df.drop('post_text', axis=1, inplace=True)

# Calculate toxicity
model_checkpoint = 'cointegrated/rubert-tiny-toxicity'
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
model = AutoModelForSequenceClassification.from_pretrained(model_checkpoint)


def text2toxicity(text, aggregate=True):
    """ Calculate toxicity of a text (if aggregate=True) or a vector of toxicity aspects (if aggregate=False)"""
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(model.device)
        proba = torch.sigmoid(model(**inputs).logits).cpu().numpy()
    if isinstance(text, str):
        proba = proba[0]
    if aggregate:
        return 1 - proba.T[0] * (1 - proba.T[-1])
    return proba


df.index = range(0, len(df))
s = df['comment']
sLength = len(s)
df['Toxic'] = pd.Series(np.random.randn(sLength), index=df.index)
for i, val in enumerate(s):
    df['Toxic'][i] = text2toxicity(val, True)
df.loc[(df['Toxic'] >= 0.5), 'Toxic'] = 1
df.loc[(df['Toxic'] < 0.5), 'Toxic'] = 0

df.to_csv('m_.csv', index=False)
