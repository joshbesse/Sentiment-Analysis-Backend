from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Analyze
from .serializers import AnalysisSerializer
import logging
from .tasks import analyze_text_task
from celery.result import AsyncResult
import os 
import redis


logger = logging.getLogger(__name__)

redis_url = os.environ.get('REDIS_URL')
redis_client = redis.from_url(redis_url, ssl_cert_reqs=None)

@api_view(["POST"])
def analyze_text(request):
    try:
        text = request.data.get("text")
        analyzer_type = request.data.get("analyzer_type", "basic")

        if not text:
            logger.warning("No text provided in request.")
            return Response({"error": "Text field is required."}, status=400)

        logger.info(f"Received analysis request with analyzer_type: {analyzer_type}")

        # Send the task to Celery for asynchronous processing
        task = analyze_text_task.delay(analyzer_type, text)

        logger.info(f"Task {task.id} dispatched to worker.")

        # Return a response indicating the task has been accepted
        return Response({"message": "Analysis started", "task_id": task.id}, status=202)

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
    task_result = AsyncResult(task_id)
    return Response({
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    })