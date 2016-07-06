from django.conf import settings
from django.db import models

class Idea(models.Model):
    title = models.CharField(max_length=40)
    contents = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    recommend = models.PositiveSmallIntegerField(default=0)
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    idea = models.ForeignKey(Idea)
    contents = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
