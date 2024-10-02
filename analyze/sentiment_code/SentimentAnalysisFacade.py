import logging
from .model_registry import ModelRegistry
from .SentimentResult import SentimentResult

logger = logging.getLogger(__name__)

class SentimentAnalysisFacade:
    def __init__(self):
        self.sentiment_analyzer = None
        self.loaded_analyzer_type = None

    def select_analyzer(self, analyzer_type):
        # Avoid re-loading if the same analyzer is already loaded
        if self.sentiment_analyzer is not None and self.loaded_analyzer_type == analyzer_type:
            logger.info(f"{analyzer_type} analyzer is already loaded.")
            return
        
        # Attempt to load the requested analyzer
        analyzer = ModelRegistry.get_model(analyzer_type)
        if analyzer:
            self.sentiment_analyzer = analyzer
            self.loaded_analyzer_type = analyzer_type
            logger.info(f"{analyzer_type} analyzer selected and loaded.")
        else:
            logger.error(f"Failed to select analyzer: {analyzer_type}")
            self.sentiment_analyzer = None
            self.loaded_analyzer_type = None

    def analyze_text(self, text):
        if self.sentiment_analyzer is None:
            logger.error("No analyzer selected.")
            return None

        try:
            result = self.sentiment_analyzer.analyze_sentiment(text)
            if result:
                logger.info(f"Analyzed text: {text} | Sentiment: {result.get_sentiment()} | Score: {result.get_score()}")
                return result
        except Exception as e:
            logger.error(f"Error during text analysis: {e}")
            return None
        
        return None