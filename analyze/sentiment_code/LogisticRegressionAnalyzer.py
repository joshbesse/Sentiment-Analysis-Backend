from .SentimentResult import SentimentResult
import logging

logger = logging.getLogger(__name__)

class LogisticRegressionAnalyzer:
    def __init__(self, vectorizer, model):
        # Accept preloaded vectorizer and model
        self.vectorizer = vectorizer
        self.model = model

    def analyze_sentiment(self, text):
        # Vectorize the input text
        text_vectorization = self.vectorizer.transform([text])
        # Make a prediction using the model
        prediction = self.model.predict(text_vectorization)[0]

        # Map prediction to a label
        if prediction == -1:
            prediction_label = "negative"
        elif prediction == 1:
            prediction_label = "positive"
        else:
            prediction_label = "neutral"

        return SentimentResult(prediction_label, prediction)
