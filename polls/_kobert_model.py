import pandas as pd
import numpy as np
import json
import os
import re
import pickle 
# import dill # for saving a function as a file(.pkl)
import logging # for changing the tf's logging level
import urllib.request
from tqdm import tqdm

from sklearn import model_selection
from sklearn.metrics import accuracy_score

import tensorflow as tf
import tensorflow_addons as tfa # for using Rectified-Adam optimizer (instead of Adam optimizer) 
from tensorflow.keras import layers, initializers, losses, optimizers, metrics, callbacks 

import transformers
from transformers import TFBertModel # BertTokenizer 제외

import sentencepiece as spm # 이번 실습에서 추가되었습니다

from tokenization_kobert import KoBertTokenizer 

# 1. dataframe 준비
path = './down_3.0_data.json'
with open(path, 'r',encoding="UTF-8") as f:
    json_data = json.load(f)

review_data = []
name_data = []

for store in json_data:
    for j in range(len(json_data[store]['reviews'])):
        name_data.append(store)
        review_data.append(json_data[store]['reviews'][j])

df = pd.DataFrame({'store' :name_data, 'review': review_data})
SEQ_LEN = df['review'].str.len().sort_values(ascending=False)[:1][1]

# 2. kobert 모델링
tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')