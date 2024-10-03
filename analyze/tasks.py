from celery import shared_task
from .models import Analyze
from .sentiment_code.SentimentAnalysisFacade import SentimentAnalysisFacade
import logging

logger = logging.getLogger(__name__)

@shared_task
def analyze_text_task(analyzer_type, text):
    try:
        facade = SentimentAnalysisFacade()
        facade.select_analyzer(analyzer_type)
        result = facade.analyze_text(text)

        if result is not None:
            try:
                analysis_result = Analyze.objects.create(
                    analyzer=analyzer_type,
                    text=text,
                    sentiment=result.get_sentiment(),
                    score=int(result.get_score())  # Ensure 'score' is a standard int
                )
                return {
                    'sentiment': result.get_sentiment(),
                    'score': int(result.get_score())  # Convert to standard int
                }
            except Exception as db_error:
                logger.error(f"Error saving to database: {db_error}")
                return {'status': 'FAILURE', 'error': 'Database save failed'}
        else:
            return {'status': 'FAILURE', 'error': 'Analyzer failed to process the text.'}
    except Exception as e:
        logger.error(f"Error in analyze_text_task: {e}")
        return {'status': 'FAILURE', 'error': str(e)}