from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os 
from .SentimentResult import SentimentResult
from sentiment_analysis.utils import download_file_from_s3
import logging 
import torch 

logger = logging.getLogger(__name__)

class BERTAnalyzer:
    def __init__(self):
        self.model_dir = os.path.join('models', 'BERT')
        self.tokenizer = None 
        self.model = None 
        self.load_models()

    def load_models(self):
        required_files = [
            'config.json',
            'model.safetensors',
            'tokenizer_config.json',
            'vocab.txt',
            'special_tokens_map.json'
        ]

        os.makedirs(self.model_dir, exist_ok=True)

        for file in required_files:
            local_file_path = os.path.join(self.model_dir, file)
            if not os.path.exists(local_file_path):
                logger.info(f"{file} not found locally. Downloading from S3...")
                s3_key = file
                download_file_from_s3(s3_key, local_file_path)

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_dir)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_dir,
                torch_dtype=torch.float16,
                device_map='auto'
            )
            logger.info("BERT models loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading BERT model: {e}")
            self.tokenizer = None 
            self.model = None 
    
    def analyze_sentiment(self, text):
            inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True).to(self.model.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            logits = outputs.logits
            prediction = logits.argmax(dim=1).item()

            if prediction == 0:
                prediction_label = "negative"
            elif prediction == 2:
                prediction_label = "positive"
            else:
                prediction_label = "neutral"

            return SentimentResult(prediction_label, prediction)

