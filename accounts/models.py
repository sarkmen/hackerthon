from django.db import models

# Create your models here.


class Profile(models.Model):
    image = models.ImageField()
    name = models.CharField(max_length = 100)
