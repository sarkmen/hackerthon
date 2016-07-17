from django.contrib import admin
from accounts.models import Resume
# Register your models here.

class ResumeAdmin(admin.ModelAdmin):
    list_display = ['user', 'name']

admin.site.register(Resume, ResumeAdmin)