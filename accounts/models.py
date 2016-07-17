from django.db import models
from django.conf import settings
# Create your models here.

class Resume(models.Model):
    POSITION_CHOICES = (
        ("Developer", 'Developer'),
        ("Planner", 'Planner'),
    )
    name = models.CharField(max_length=100)
    contents = models.TextField(max_length=500)
    group = models.CharField(max_length=20)
    position = models.CharField(max_length=20, choices = POSITION_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete =models.CASCADE)
