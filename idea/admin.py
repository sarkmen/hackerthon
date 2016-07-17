from django.contrib import admin

from .models import Idea, Comment,Vote

class TitleDisplay(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['title']

class VoteAdmin(admin.ModelAdmin):
    list_display = ['vote_user', 'vote_idea']

admin.site.register(Idea, TitleDisplay)
admin.site.register(Comment)
admin.site.register(Vote, VoteAdmin)