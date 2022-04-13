import pandas as pd

name = input("Step 2. Which dataset do you want to filter? (Example: m_RegnumM)\n")
df = pd.read_csv(f'{name}.csv', encoding="utf-8")
df.drop('education', axis=1, inplace=True)

for i, val in enumerate(df['city']):
    if df['country'][i] == '0':
        df['country'][i] = "Россия1"
    if df['city'][i] == '0':
        df['city'][i] = "Москва1"
    if df['occupation'][i] == '0':
        df['occupation'][i] = "НПИ1"

df.to_csv(f'f_{name}.csv', index=False)
