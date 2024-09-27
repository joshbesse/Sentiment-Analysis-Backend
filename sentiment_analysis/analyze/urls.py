from django.urls import path
from .views import analyze_text, get_analysis_history

urlpatterns = [
    path('analyze/', analyze_text, name='analyze_text'),
    path('history/', get_analysis_history, name='get_analysis_history'),
]