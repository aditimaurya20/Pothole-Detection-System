from django.db import models

class Detection(models.Model):
    image = models.ImageField(upload_to='detections/')
    severity = models.CharField(max_length=20)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)