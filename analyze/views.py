from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Analyze
from .serializers import AnalysisSerializer
import logging
from .tasks import analyze_text_task
from celery.result import AsyncResult
import os 
import redis
import ssl
from django.http import JsonResponse



logger = logging.getLogger(__name__)

redis_url = os.environ.get('REDIS_URL')
redis_client = redis.from_url(
    redis_url, 
    ssl_cert_reqs=ssl.CERT_NONE  # Adjust as needed: CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED
)

@api_view(["POST"])
def analyze_text(request):
    try:
        text = request.data.get("text")
        analyzer_type = request.data.get("analyzer_type", "basic")

        if not text:
            logger.warning("No text provided in request.")
            return Response({"error": "Text field is required."}, status=400)

        logger.info(f"Received analysis request with analyzer_type: {analyzer_type}")

        # Start the Celery task and return its task ID
        task = analyze_text_task.delay(analyzer_type, text)
        return Response({"task_id": task.id}, status=202)

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
    
@api_view(["GET"])
def get_task_status(request, task_id):
    try:
        result = AsyncResult(task_id)
        if result.state == 'SUCCESS':
            response_data = {
                'status': result.state,
                'sentiment': result.result.get('sentiment', None),
                'score': result.result.get('score', None)
            }
        elif result.state == 'FAILURE':
            response_data = {
                'status': result.state,
                'error': str(result.info)
            }
        else:
            response_data = {'status': result.state}
        return JsonResponse(response_data)
    except Exception as e:
        return JsonResponse({'status': 'FAILURE', 'error': str(e)}, status=500)