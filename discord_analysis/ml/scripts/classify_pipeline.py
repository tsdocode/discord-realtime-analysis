from joblib import dump, load
import sklearn
from sklearn.pipeline import Pipeline
from dotenv import load_dotenv
import os

load_dotenv()


class ClassificationPipeline():
    def __init__(self):
        self.class_names = ["Normal", "Offensive", "Hate"]
        self.count_vector = load(os.getenv("COUNT_VECTOR_PATH"))
        self.tfidf = load(os.getenv("TDIDF_PATH"))
        self.naive = load(os.getenv("NAIVE_PATH"))

        self.pipeline = Pipeline([
            ("vect", self.count_vector),
            ("tdidf", self.tfidf),
            ("clf", self.naive)
        ])

    def __call__(self, text):
        predicts = self.pipeline.predict([text])

        return self.class_names[predicts[0]]
        
        