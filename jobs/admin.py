from django.contrib import admin

from .models import Job, Application


admin.site.register(Job)
admin.site.register(Application)