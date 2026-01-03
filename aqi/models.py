from django.db import models

class AirQuality(models.Model):
    city = models.CharField(max_length=100)
    aqi = models.IntegerField()
    level = models.CharField(max_length=50)
    pm2_5 = models.FloatField(null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.city