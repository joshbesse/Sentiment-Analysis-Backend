from transformers import BertTokenizer, BertForSequenceClassification
import joblib
import torch
from .SentimentResult import SentimentResult

class BERTAnalyzer:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('../ML models/BERT/')
        self.label_encoder = joblib.load('../ML models/BERT/label_encoder.pkl')
        self.model = BertForSequenceClassification.from_pretrained('../ML models/BERT/')
        self.current_text = None 
        self.current_result = None 

    def analyze_sentiment(self, text):
        self.current_text = text

        input = self.tokenizer(self.current_text, padding=True, truncation=True, return_tensors='pt', max_length=128)
        self.model.eval()
        with torch.no_grad():
            output = self.model(**input)
        prediction = torch.argmax(output.logits, dim=1)
        decoded_prediction = self.label_encoder.inverse_transform(prediction)[0]

        self.current_result = SentimentResult(decoded_prediction, prediction)
        return self.current_result