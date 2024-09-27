import joblib
from .SentimentResult import SentimentResult

class LogisticRegressionAnalyzer:
    def __init__(self):
        self.vectorizer = joblib.load('../ML models/Logistic Regression/tfidf_vectorizer.pkl')
        self.label_encoder = joblib.load('../ML models/Logistic Regression/label_encoder.pkl')
        self.model = joblib.load('../ML models/Logistic Regression/log_reg_model.pkl')
        self.current_text = None
        self.current_result = None 

    def analyze_sentiment(self, text):
        self.current_text = text

        text_vectorization = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vectorization)
        decoded_prediction = self.label_encoder.inverse_transform(prediction)[0]

        self.current_result = SentimentResult(decoded_prediction, prediction)
        return self.current_result

