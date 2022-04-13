import pandas as pd

name = input("Step 3. Which dataset do you want to split? (Example: f_m_RegnumM)\n")

# sample_submission
df = pd.read_csv(f'{name}.csv', encoding="utf-8", nrows=200, usecols=['Toxic'])
df['id'] = df.index = range(0, len(df))
df.set_index('id', inplace=True)
df.rename(columns={'Toxic': 'target'}, inplace=True)
df.to_csv(f'./lama_{name}/sample_submission.csv', index=False)

# train
train = pd.read_csv(f'{name}.csv', encoding="utf-8")
train.rename(columns={'Toxic': 'target'}, inplace=True)
train['id'] = train.index = range(0, len(train))
train.set_index('id', inplace=True)
train.to_csv(f'./lama_{name}/train.csv', index=False)

# test
test = pd.read_csv(f'{name}.csv', encoding="utf-8", nrows=200)
test.drop('Toxic', axis=1, inplace=True)
test['id'] = test.index = range(0, len(df))
test.set_index('id', inplace=True)
test.to_csv(f'./lama_{name}/test.csv', index=False)
