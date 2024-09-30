from django.db import models

# Create your models here.
class Analyze(models.Model):
    analyzer = models.CharField(max_length=50)
    text = models.TextField()
    sentiment = models.CharField(max_length=10)
    score = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.analyzer} - {self.sentiment} - {self.score}"
