from django.contrib import admin

from .models import Idea, Comment

class TitleDisplay(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']

admin.site.register(Idea, TitleDisplay)
admin.site.register(Comment)
