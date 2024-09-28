from rest_framework.decorators import api_view
from rest_framework.response import Response 
from .models import Analyze
from .sentiment_code.SentimentAnalysisFacade import SentimentAnalysisFacade
from .serializers import AnalysisSerializer

# Create your views here.
facade = SentimentAnalysisFacade()

@api_view(["POST"])
def analyze_text(request):
    text = request.data.get("text")
    analyzer_type = request.data.get("analyzer_type", "basic")
    print(analyzer_type)

    facade.select_analyzer(analyzer_type)
    result = facade.analyze_text(text)

    analysis_result = Analyze.objects.create(
        analyzer=analyzer_type,
        text=text, 
        sentiment=result.get_sentiment(), 
        score=result.get_score()
    )

    return Response({
        'sentiment': result.get_sentiment(),
        'score': result.get_score()
    })

@api_view(["GET"])
def get_analysis_history(request):
    history = Analyze.objects.all().order_by("-date")[:10]
    serializer = AnalysisSerializer(history, many=True)
    return Response(serializer.data)