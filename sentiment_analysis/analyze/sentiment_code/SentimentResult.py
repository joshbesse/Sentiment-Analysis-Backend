class SentimentResult:
    def __init__(self, sentiment, score):
        self.sentiment = sentiment
        self.score = score
    
    def get_sentiment(self):
        return self.sentiment
    
    def get_score(self):
        return self.score 