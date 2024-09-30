from rest_framework import serializers
from .models import Analyze

class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analyze
        fields = '__all__'