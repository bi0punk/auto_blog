from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, default='')
    magnitude = models.FloatField(null=True, blank=True)
    depth_km = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    utc_time = models.DateTimeField(null=True, blank=True)
    content = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return self.title
