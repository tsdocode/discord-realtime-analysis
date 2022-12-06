from tensorflow import keras
import pickle
from keras.utils import pad_sequences
from keras.models import load_model
from dotenv import load_dotenv
import numpy as np
import os

load_dotenv()


with open(os.getenv('TOKENIZER_PATH'), 'rb') as handle:
    tokenizer = pickle.load(handle)


model = load_model(os.getenv('KERAS_MODEL_PATH'))

class_names = ["Normal", "Offensive", "Hate"]

def predict(text):
    pred = model.predict(pad_sequences(tokenizer.texts_to_sequences([text]), 150))

    idx = np.argmax(pred)

    return class_names[idx]
