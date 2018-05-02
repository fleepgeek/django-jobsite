from decimal import Decimal

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings

from accounts.models import Company
from jobsite.utils import random_string_generator, current_time_milli

User = settings.AUTH_USER_MODEL

import stripe
STRIPE_SECRET_KEY = getattr(settings, 'STRIPE_SECRET_KEY')
stripe.api_key = STRIPE_SECRET_KEY


class PaymentProfile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    email       = models.EmailField()
    customer_id = models.CharField(max_length=120, blank=True)
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    @property
    def has_voucher(self):
        vouchers = self.user.company.voucher_set
        if vouchers.exists():
            return True
        return False

def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.is_employer:
        PaymentProfile.objects.get_or_create(
            user    = instance,
            email   = instance.email
        )

post_save.connect(user_post_save_receiver, sender=User)


def payment_profile_pre_save_receiver(sender, instance, *args, **kwargs): 
    customer = stripe.Customer.create(email=instance.email)
    instance.customer_id = customer.id

pre_save.connect(payment_profile_pre_save_receiver, sender=PaymentProfile)


class CardManager(models.Manager):
    def new(self, token, payment_profile):
        if token and payment_profile.user.is_employer:
            customer_id = payment_profile.customer_id
            customer    = stripe.Customer.retrieve(customer_id)
            card_rsp    = customer.sources.create(source=token)
            new_card = self.model.objects.create(
                payment_profile = payment_profile,
                card_id         = card_rsp.id,
                brand           = card_rsp.brand,
                country         = card_rsp.country,
                exp_month       = card_rsp.exp_month,
                exp_year        = card_rsp.exp_year,
                last4           = card_rsp.last4,
            )
            return new_card
        return None

class Card(models.Model):
    payment_profile = models.ForeignKey(PaymentProfile, on_delete=models.CASCADE)
    card_id         = models.CharField(max_length=60)
    brand           = models.CharField(max_length=120, null=True, blank=True)
    country         = models.CharField(max_length=20, null=True, blank=True)
    exp_month       = models.IntegerField(null=True, blank=True)
    exp_year        = models.IntegerField(null=True, blank=True)
    last4           = models.CharField(max_length=4, null=True, blank=True)
    default         = models.BooleanField(default=True)
    created_on      = models.DateTimeField(auto_now_add=True)

    objects         = CardManager()

    def __str__(self):
        return self.card_id

def card_post_save_receiver(sender, instance, created, *args, **kwargs):
    if created:
        qs = Card.objects.filter(default=True).exclude(id=instance.id)
        if qs.exists():
            qs.update(default=False)
    
post_save.connect(card_post_save_receiver, sender=Card)


class Voucher(models.Model):
    voucher_id  = models.CharField(max_length=50)
    company     = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    active      = models.BooleanField(default=True)
    created_on  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.voucher_id


class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('abandoned', 'Abandoned'),
    )
    order_id        = models.CharField(max_length=50)
    payment_profile = models.ForeignKey(PaymentProfile, on_delete=models.CASCADE, blank=True, null=True)
    quantity        = models.PositiveIntegerField(default=1)
    total           = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    status          = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    active          = models.BooleanField(default=True)
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = random_string_generator() + str(current_time_milli())
    instance.total = Decimal(instance.quantity) * Decimal(10.00)
    
pre_save.connect(order_pre_save_receiver, sender=Order)


def order_post_save_receiver(sender, created, instance, *args, **kwargs):
    if created:
        qs = Order.objects.filter(payment_profile=instance.payment_profile, active=True).exclude(id=instance.id)
        if qs.exists():
            qs.update(active=False, status='abandoned')

post_save.connect(order_post_save_receiver, sender=Order)