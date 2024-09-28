from transformers import BertTokenizer, BertForSequenceClassification
import torch
from .SentimentResult import SentimentResult

class BERTAnalyzer:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('../models/BERT/')
        self.model = BertForSequenceClassification.from_pretrained('../models/BERT/')
        self.current_text = None 
        self.current_result = None 

    def analyze_sentiment(self, text):
        self.current_text = text

        input = self.tokenizer(self.current_text, padding=True, truncation=True, return_tensors='pt', max_length=128)
        self.model.eval()
        with torch.no_grad():
            output = self.model(**input)
        prediction = torch.argmax(output.logits, dim=1)

        if prediction == 0:
            prediction_label = "negative"
        elif prediction == 2:
            prediction_label = "positive"
        else:
            prediction_label = "neutral"

        self.current_result = SentimentResult(prediction_label, prediction)
        return self.current_result