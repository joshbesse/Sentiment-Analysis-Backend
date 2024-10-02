import joblib
import os 
from .SentimentResult import SentimentResult
from sentiment_analysis.utils import download_file_from_s3
import logging

logger = logging.getLogger(__name__)

class LogisticRegressionAnalyzer:
    def __init__(self):
        self.model_dir = os.path.join('models', 'Logistic Regression')
        self.vectorizer = None
        self.model = None
        self.load_models()
    
    def load_models(self):
        required_files = [
            'log_reg_tfidf_vectorizer.pkl',
            'log_reg_model.pkl'
        ]

        os.makedirs(self.model_dir, exist_ok=True)

        for file in required_files:
            local_file_path = os.path.join(self.model_dir, file)
            if not os.path.exists(local_file_path):
                logger.info(f"{file} not found locally. Downloading from S3...")
                s3_key = file
                try:
                    download_file_from_s3(s3_key, local_file_path)
                    logger.info(f"Downloaded {file} successfully.")
                except Exception as e:
                    logger.error(f"Failed to download {file} from S3: {e}")
                    continue

        try:
            self.vectorizer = joblib.load(os.path.join(self.model_dir, 'log_reg_tfidf_vectorizer.pkl'))
            self.model = joblib.load(os.path.join(self.model_dir, 'log_reg_model.pkl'))
            logger.info("Logistic Regression models loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading Logistic Regression models: {e}")
            self.vectorizer = None
            self.model = None

    def analyze_sentiment(self, text):
        text_vectorization = self.vectorizer.transform([text])
        prediction = self.model.predict(text_vectorization)[0]

        if prediction == -1:
            prediction_label = "negative"
        elif prediction == 1:
            prediction_label = "positive"
        else:
            prediction_label = "neutral"

        return SentimentResult(prediction_label, prediction)
