from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Analyze
from .sentiment_code.SentimentAnalysisFacade import SentimentAnalysisFacade
from .serializers import AnalysisSerializer
import logging

logger = logging.getLogger(__name__)

# Create your views here.
facade = SentimentAnalysisFacade()

@api_view(["GET", "POST"])
def analyze_text(request):
    try:
        text = request.data.get("text")
        analyzer_type = request.data.get("analyzer_type", "basic")
        
        if not text:
            return Response({"error": "Text field is required."}, status=400)
        
        logger.info(f"Analyzer Type: {analyzer_type}")

        facade.select_analyzer(analyzer_type)
        result = facade.analyze_text(text)

        if result is None:
            return Response({"error": "Analyzer not selected or failed to analyze."}, status=500)
        
        analysis_result = Analyze.objects.create(
            analyzer=analyzer_type,
            text=text,
            sentiment=result.get_sentiment(),
            score=result.get_score()
        )

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
        return Response(serializer.data, status=200)
    except Exception as e:
        logger.error(f"Error in get_analysis_history view: {e}")
        return Response({"error": "Internal Server Error"}, status=500)