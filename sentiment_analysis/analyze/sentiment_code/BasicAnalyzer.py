import re

from .Read import Read 
from .AnalyzerContext import AnalyzerContext
from .InitializationState import InitializationState
from .SentimentResult import SentimentResult
from .SentimentMemento import SentimentMemento

class BasicAnalyzer:
    def __init__(self):
        # setting positive and negative words lists
        self.reader = Read()
        self.positive_words = self.reader.file_to_list("positive.txt")
        self.negative_words = self.reader.file_to_list("negative.txt")
        self.state = AnalyzerContext(InitializationState())
        self.current_text = None
        self.current_result = None 
    
    def analyze_sentiment(self, text):
        # setting text and sentiment score
        self.current_text = text
        score = 0 

        # initialization state 
        self.state.perform_action()
        print("analyzer: basic")
        tokens = re.sub(r'[^a-zA-Z ]', '', text.lower()).split()
        print("tokenization:", tokens)
        self.state.change_state()

        # processing state 
        positive_contained = []
        negative_contained = []
        self.state.perform_action()
        for token in tokens:
            if token in self.positive_words:
                score += 1
                positive_contained.append(token)
            elif token in self.negative_words:
                score -= 1
                negative_contained.append(token)

        print("positive:", positive_contained)
        print("negative:", negative_contained)
        self.state.change_state()

        # completed state
        self.state.perform_action()
        if score > 0:
            sentiment = "positive"
        elif score < 0:
            sentiment = "negative"
        else:
            sentiment = "neutral"

        self.current_result = SentimentResult(sentiment, score)
        return self.current_result
    
    def save_state(self):
        return SentimentMemento(self.current_text, self.current_result)
    
    def restore_state(self, memento):
        self.current_text = memento.get_saved_text()
        self.current_result = memento.get_saved_result()