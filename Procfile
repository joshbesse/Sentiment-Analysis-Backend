web: gunicorn sentiment_analysis.wsgi --log-file - --workers 1
worker: celery -A sentiment_analysis worker --loglevel=info --concurrency=1

