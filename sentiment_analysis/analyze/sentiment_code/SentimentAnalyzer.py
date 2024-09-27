from abc import ABC, abstractmethod

class SentimentAnalyzer(ABC):
    @abstractmethod
    def analyze_sentiment(self, text):
        pass 

    @abstractmethod
    def save_state(self):
        pass

    @abstractmethod
    def restore_state(self, memento):
        pass 