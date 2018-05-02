from django.contrib import admin

from .models import PaymentProfile, Card, Voucher, Order

admin.site.register(PaymentProfile)
admin.site.register(Card)
admin.site.register(Voucher)
admin.site.register(Order)
