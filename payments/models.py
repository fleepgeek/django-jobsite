from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings

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