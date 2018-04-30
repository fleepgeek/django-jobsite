from django.contrib import admin

from .models import PaymentProfile, Card

admin.site.register(PaymentProfile)
admin.site.register(Card)
