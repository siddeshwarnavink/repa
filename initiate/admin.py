from django.contrib import admin
from .models import Process

class ProcessAdmin(admin.ModelAdmin):
    list_display = ['job_title', 'status']

admin.site.register(Process, ProcessAdmin)
