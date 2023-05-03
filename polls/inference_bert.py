import re
import numpy as np


def predict_sentiment(sentence, tokenizer, model):

    SEQ_LEN = 128

    encoded_dict = tokenizer.encode_plus(text=re.sub("[^\s0-9a-zA-Zㄱ-ㅎㅏ-ㅣ가-힣]", "", sentence),
                                         padding='max_length',
                                         truncation=True,
                                         max_length=SEQ_LEN)

    token_ids      = np.array(encoded_dict['input_ids']).reshape(1, -1)
    token_masks    = np.array(encoded_dict['attention_mask']).reshape(1, -1)
    token_segments = np.array(encoded_dict['token_type_ids']).reshape(1, -1)

    new_inputs = (token_ids, token_masks, token_segments)

    prediction = model.predict(new_inputs)
    #predicted_probability = np.round(np.max(prediction) * 100, 2)
    predicted_class = ['부정', '긍정'][np.argmax(prediction, axis=1)[0]]

    return predicted_class
