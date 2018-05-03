from django.contrib import admin

from .models import Job, Application


class JobAdmin(admin.ModelAdmin):
    readonly_fields = ('voucher',)

admin.site.register(Job, JobAdmin)
admin.site.register(Application)