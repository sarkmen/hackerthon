from django.contrib import admin

from .models import Idea, Comment

admin.site.register(Idea)
admin.site.register(Comment)