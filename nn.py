# Standard python libraries
import os
import time

# Installed libraries
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
import torch
import matplotlib.pyplot as plt

# Imports from our package
from lightautoml.automl.presets.text_presets import TabularNLPAutoML
from lightautoml.dataset.roles import DatetimeRole
from lightautoml.tasks import Task

N_THREADS = 4  # threads cnt for lgbm and linear models
RANDOM_STATE = 42  # fixed random state for various reasons
TEST_SIZE = 0.2  # Test size for metric check
TIMEOUT = 6 * 3600  # Time in seconds for automl run
TARGET_NAME = 'target'

name = input("Step 4. What is the name of your filtered file? (Example: f_m_RegnumM\nfor /lama_{name}/train.csv directory\n)")

train_data = pd.read_csv(f'./lama_{name}/train.csv')
train_data['id'] = train_data.index = range(0, len(train_data))
train_data.set_index('id', inplace=True)

test_data = pd.read_csv(f'./lama_{name}/test.csv')
test_data['id'] = test_data.index = range(0, len(test_data))
test_data.set_index('id', inplace=True)

submission = pd.read_csv(f'./lama_{name}/sample_submission.csv')
submission['id'] = submission.index = range(0, len(submission))
submission.set_index('id', inplace=True)

train_data['occupation'].value_counts(dropna=False)
train_data['city'].value_counts(dropna=False)
train_data['country'].value_counts(dropna=False)


def clean_text(text):
    return text


all_data = pd.concat([
    train_data.drop(TARGET_NAME, axis=1),
    test_data
]).reset_index(drop=True)

all_data['country'] = all_data['country'].astype(str)
all_data.loc[all_data['country'].value_counts()[all_data['country']].values < 5, 'country'] = "RARE_VALUE"
all_data.loc[all_data['country'] == 'nan', 'country'] = np.nan

all_data['city'] = all_data['city'].astype(str)
all_data.loc[all_data['city'].value_counts()[all_data['city']].values < 5, 'city'] = "RARE_VALUE"
all_data.loc[all_data['city'] == 'nan', 'city'] = np.nan

all_data['occupation'] = all_data['occupation'].astype(str)
all_data.loc[all_data['occupation'].value_counts()[all_data['occupation']].values < 5, 'occupation'] = "RARE_VALUE"
all_data.loc[all_data['occupation'] == 'nan', 'occupation'] = np.nan

all_data['comment'] = all_data['comment'].map(clean_text)

y_train = train_data.target.values
train_data = all_data[:len(train_data)]
train_data[TARGET_NAME] = y_train
test_data = all_data[len(train_data):]

# Step 1. Create Task


task = Task('binary', )

# Step 2. Setup columns roles


roles = {'target': TARGET_NAME,
         'text': ['comment'],
         'drop': ['id', 'post_number', 'first_name', 'second_name']}

# Step 3. Create AutoML from preset
# To create AutoML model here we use TabularNLPAutoML preset.

# All params we set above can be send inside preset to change its configuration:


automl = TabularNLPAutoML(task=task,
                          timeout=TIMEOUT,
                          cpu_limit=N_THREADS,
                          reader_params={'cv': 5},
                          general_params={'nested_cv': False, 'use_algos': [['linear_l2', 'lgb', 'nn']]},
                          text_params={'lang': 'ru'},
                          nn_params={'lang': 'ru',
                                     'bert_name': 'vinai/bertweet-base',
                                     'opt_params': {'lr': 1e-5},
                                     'max_length': 300, 'bs': 13,
                                     'n_epoch': 5
                                     },
                          )

oof_pred = automl.fit_predict(train_data, roles=roles)
print('oof_pred:\n{}\nShape = {}'.format(oof_pred, oof_pred.shape))

automl.collect_used_feats()

# Step 4. Predict to test data
test_pred = automl.predict(test_data)
print('Prediction for test data:\n{}\nShape = {}'.format(test_pred, test_pred.shape))


# Step 5. Select best threshold to optimize F1 score
def select_threshold_f1(y_true, y_pred):
    best_score = -1
    best_thr = None
    for thr in np.arange(0, 1.01, 0.01):
        score = f1_score(y_true, (y_pred > thr).astype(int))
        if score > best_score:
            best_score = score
            best_thr = thr

    print('Best score: {}\nBest selected threshold: {:.2f}'.format(best_score, best_thr))
    return best_thr


best_thr = select_threshold_f1(train_data[TARGET_NAME], oof_pred.data[:, 0])

# Step 6. Generate submission file
submission['target'] = (test_pred.data[:, 0] > best_thr).astype(int)
submission.to_csv(f'LightAutoML_preds_{name}.csv', index=False)
