from django.db import models

class Trend(models.Model):
    keyword = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    interest = models.FloatField(default=0.0)

    def __str__(self):
        return self.keyword