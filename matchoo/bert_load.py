import os
import pickle
import logging
import numpy as np

import tensorflow as tf
from tensorflow.keras import layers, initializers, losses, optimizers, metrics, callbacks
import transformers
from transformers import TFBertModel
import sentencepiece as spm

from .bert_tokenizer import KoBertTokenizer


tf.random.set_seed(1234)
np.random.seed(1234)

transformers.logging.set_verbosity(transformers.logging.ERROR)
tf.get_logger().setLevel(logging.ERROR)


def create_bert_model(max_length=128):
    bert_base_model = TFBertModel.from_pretrained('monologg/kobert', from_pt=True)

    input_token_ids = layers.Input((max_length,), dtype=tf.int32, name='input_token_ids')
    input_masks     = layers.Input((max_length,), dtype=tf.int32, name='input_masks')
    input_segments  = layers.Input((max_length,), dtype=tf.int32, name='input_segments')

    bert_outputs = bert_base_model([input_token_ids, input_masks, input_segments])
    bert_outputs = bert_outputs[1] # "[CLS]" token의 embedding layer에서 내어주는 768개의 숫자
    bert_outputs = layers.Dropout(0.2)(bert_outputs)

    final_output = layers.Dense(units=2,
                                activation='softmax',
                                kernel_initializer=initializers.TruncatedNormal(stddev=0.02),
                                name='classifier')(bert_outputs)

    model = tf.keras.Model(inputs=[input_token_ids, input_masks, input_segments],
                           outputs=final_output)

    model.compile(optimizer=optimizers.Adam(learning_rate=1e-5),
                  loss=losses.SparseCategoricalCrossentropy(),
                  metrics=[metrics.SparseCategoricalAccuracy()])

    model.load_weights(filepath='./models/best_kobert_weights.h5')

    return model


def load_bert_tokenizer():

    tokenizer = KoBertTokenizer.from_pretrained('monologg/kobert')

    return tokenizer
