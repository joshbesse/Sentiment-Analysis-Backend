import logging 
from .model_registry import ModelRegistry
from .SentimentResult import SentimentResult

logger = logging.getLogger(__name__)

class SentimentAnalysisFacade:
    def __init__(self):
        self.sentiment_analyzer = None 

    def select_analyzer(self, analyzer_type):
        analyzer = ModelRegistry.get_model(analyzer_type)
        if analyzer:
            self.sentiment_analyzer = analyzer
            logger.info(f"{analyzer_type} analyzer selected and loaded.")
        else:
            logger.error(f"Failed to select analyzer: {analyzer_type}")

    def analyze_text(self, text):
        if self.sentiment_analyzer is None:
            logger.error("No analyzer selected.")
            return None 
        result = self.sentiment_analyzer.analyze_sentiment(text)
        logger.info(f"Analyzed text: {text} | Sentiment: {result.get_sentiment()} | Score: {result.get_score()}")
        return result