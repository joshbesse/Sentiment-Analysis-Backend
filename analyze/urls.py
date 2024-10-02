from django.urls import path
from .views import analyze_text, get_analysis_history, get_task_status

urlpatterns = [
    path('analyze/', analyze_text, name='analyze_text'),
    path('history/', get_analysis_history, name='get_analysis_history'),
    path('', analyze_text, name='home'),
    path('status/<str:task_id>/', get_task_status, name='get_task_status'),
]