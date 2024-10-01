import joblib
import os 
from .SentimentResult import SentimentResult
from sentiment_analysis.utils import download_file_from_s3
import logging

logger = logging.getLogger(__name__)

class LogisticRegressionAnalyzer:
    def __init__(self):
        self.vectorizer = None 
        self.model = None 
        self.load_models()

    def load_models(self):
        model_dir = os.path.join('models', 'Logistic Regression')
        vectorizer_path = os.path.join(model_dir, 'log_reg_tfidf_vectorizer.pkl')
        model_path = os.path.join(model_dir, 'log_reg_model.pkl')

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if not os.path.exists(vectorizer_path):
            logger.info("Vectorizer file not found locally. Downloading from S3...")
            s3_key = 'log_reg_tfidf_vectorizer.pkl'
            download_file_from_s3(s3_key, vectorizer_path)

        if not os.path.exists(model_path):
            logger.info("Model file not found locally. Downloading from S3...")
            s3_key = 'log_reg_model.pkl'
            download_file_from_s3(s3_key, model_path)

        self.vectorizer = joblib.load(vectorizer_path)
        self.model = joblib.load(model_path)
        logger.info("Logistic Regression models loaded successfully.")

    def analyze_text(self, text):
        text_vectorization = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vectorization)[0]

        if prediction == -1:
            prediction_label = "negative"
        elif prediction == 1:
            prediction_label = "positive"
        else:
            prediction_label = "neutral"

        return SentimentResult(prediction_label, prediction)
