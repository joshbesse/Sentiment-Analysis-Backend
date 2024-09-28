import joblib
from .SentimentResult import SentimentResult

class RandomForestAnalyzer:
    def __init__(self):
        self.vectorizer = joblib.load('../models/Random Forest/tfidf_vectorizer.pkl')
        self.model = joblib.load('../models/Random Forest/rand_for_model.pkl')
        self.current_text = None
        self.current_result = None 

    def analyze_sentiment(self, text):
        self.current_text = text

        text_vectorization = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vectorization)

        if prediction == -1:
            prediction_label = "negative"
        elif prediction == 1: 
            prediction_label = "positive"
        else:
            prediction_label = "neutral"

        self.current_result = SentimentResult(prediction_label, prediction)
        return self.current_result