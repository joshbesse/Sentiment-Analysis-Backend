import logging 
from .model_registry import ModelRegistry
from .SentimentResult import SentimentResult

logger = logging.getLogger(__name__)

class SentimentAnalysisFacade:
    def __init__(self):
        self.sentiment_analyzer = None 

    def select_analyzer(self, type):
        analyzer = ModelRegistry.get_model(type)
        if analyzer:
            self.select_analyzer = analyzer
            logger.info(f"{type} analyzer selected and loaded.")
        else:
            logger.error(f"Failed to select analyzer: {type}")

    def analyze_text(self, text):
        if self.select_analyzer is None:
            logger.error("No analyzer selected.")
            return None 
        result = self.sentiment_analyzer.analyze_sentiment(text)
        logger.info(f"Analyzed text: {text} | Sentiment: {result.get_sentiment()} | Score: {result.get_score()}")
        return result