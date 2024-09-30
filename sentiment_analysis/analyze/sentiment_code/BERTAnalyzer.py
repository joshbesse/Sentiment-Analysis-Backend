from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os 
from .SentimentResult import SentimentResult
from sentiment_analysis.utils import download_file_from_s3
import logging 

logger = logging.getLogger(__name__)

class BERTAnalyzer:
    def __init__(self):
        model_dir = os.path.join('models', 'BERT')

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        required_files = [
            'config.json',
            'model.safetensors',
            'tokenizer_config.json',
            'vocab.txt',
            'special_tokens_map.json'
        ]

        for file in required_files:
            local_file_path = os.path.join(model_dir, file)
            if not os.path.exists(local_file_path):
                logger.info(f"{file} not found locally. Downloading from S3...")
                s3_key = file
                download_file_from_s3(s3_key, local_file_path)
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        self.current_text = None 
        self.current_result = None 

    def analyze_sentiment(self, text):
        self.current_text = text

        inputs = self.tokenizer(text, return_tensors='pt', truncation=True, padding=True)
        outputs = self.model(**inputs)
        logits = outputs.logits
        prediction = logits.argmax(dim=1).item()

        if prediction == 0:
            prediction_label = "negative"
        elif prediction == 2:
            prediction_label = "positive"
        else:
            prediction_label = "neutral"

        self.current_result = SentimentResult(prediction_label, prediction)
        return self.current_result