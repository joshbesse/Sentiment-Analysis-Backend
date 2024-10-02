from celery import shared_task
from .models import Analyze
from .sentiment_code.SentimentAnalysisFacade import SentimentAnalysisFacade
import logging

logger = logging.getLogger(__name__)

@shared_task
def analyze_text_task(analyzer_type, text):
    try:
        # Initialize the facade
        facade = SentimentAnalysisFacade()
        facade.select_analyzer(analyzer_type)
        
        result = facade.analyze_text(text)

        if result is not None:
            # Save the analysis result to the database
            analysis_result = Analyze.objects.create(
                analyzer=analyzer_type,
                text=text,
                sentiment=result.get_sentiment(),
                score=result.get_score()
            )
            logger.info(f"Analysis result saved for task: {analysis_result}")
            
            # Return the result as a dictionary
            return {
                'sentiment': result.get_sentiment(),
                'score': result.get_score()
            }
        else:
            logger.error("Analyzer failed to process the text.")
            return {'error': 'Analyzer failed to process the text.'}
    except Exception as e:
        logger.error(f"Error in analyze_text_task: {e}")
        return {'error': str(e)}