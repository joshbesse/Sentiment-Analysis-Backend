import joblib
import os
from .SentimentResult import SentimentResult
from ...sentiment_analysis.utils import download_file_from_s3
import logging

logger = logging.getLogger(__name__)

class RandomForestAnalyzer:
    def __init__(self):
        model_dir = os.path.join('models', 'Random Forest')
        vectorizer_path = os.path.join(model_dir, 'tfidf_vectorizer.pkl')
        model_path = os.path.join(model_dir, 'rand_for_model.pkl')

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if not os.path.exists(vectorizer_path):
            logger.info("Vectorizer file not found locally. Downloading from S3...")
            s3_key = 'Random Forest/tfidf_vectorizer.pkl'
            download_file_from_s3(s3_key, vectorizer_path)
        
        if not os.path.exists(model_path):
            logger.info("Model file not found locally. Downloading from S3...")
            s3_key = 'Random Forest/rand_for_model.pkl'
            download_file_from_s3(s3_key, model_path)

        self.vectorizer = joblib.load(vectorizer_path)
        self.model = joblib.load(model_path)
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