from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Analyze
from .sentiment_code.SentimentAnalysisFacade import SentimentAnalysisFacade
from .serializers import AnalysisSerializer
import logging

logger = logging.getLogger(__name__)

facade = SentimentAnalysisFacade()

@api_view(["POST"])
def analyze_text(request):
    try:
        text = request.data.get("text")
        analyzer_type = request.data.get("analyzer_type", "basic")

        if not text:
            logger.warning("No text provided in request.")
            return Response({"error": "Text field is required."}, status=400)

        logger.info(f"Received analysis request with analyzer_type: {analyzer_type}")

        facade.select_analyzer(analyzer_type)
        if facade.sentiment_analyzer is None:
            return Response({"error": f"Analyzer '{analyzer_type}' not found or failed to load."}, status=400)

        result = facade.analyze_text(text)

        if result is None:
            logger.error("Analyzer failed to process the text.")
            return Response({"error": "Analyzer failed to process the text."}, status=500)

        analysis_result = Analyze.objects.create(
            analyzer=analyzer_type,
            text=text,
            sentiment=result.get_sentiment(),
            score=result.get_score()
        )

        logger.info(f"Analysis result saved: {analysis_result}")

        return Response({
            'sentiment': result.get_sentiment(),
            'score': result.get_score()
        }, status=200)

    except Exception as e:
        logger.error(f"Error in analyze_text view: {e}")
        return Response({"error": "Internal Server Error"}, status=500)

@api_view(["GET"])
def get_analysis_history(request):
    try:
        history = Analyze.objects.all().order_by("-date")[:10]
        serializer = AnalysisSerializer(history, many=True)
        logger.info("Fetched analysis history.")
        return Response(serializer.data, status=200)
    except Exception as e:
        logger.error(f"Error in get_analysis_history view: {e}")
        return Response({"error": "Internal Server Error"}, status=500)