import joblib
from .SentimentResult import SentimentResult

class RandomForestAnalyzer:
    def __init__(self):
        self.vectorizer = joblib.load('../ML models/Random Forest/tfidf_vectorizer.pkl')
        self.label_encoder = joblib.load('../ML models/Random Forest/label_encoder.pkl')
        self.model = joblib.load('../ML models/Random Forest/rand_for_model.pkl')
        self.current_text = None
        self.current_result = None 

    def analyze_sentiment(self, text):
        self.current_text = text

        text_vectorization = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vectorization)
        decoded_prediction = self.label_encoder.inverse_transform(prediction)[0]

        self.current_result = SentimentResult(decoded_prediction, prediction)
        return self.current_result