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


def payment_profile_pre_save_receiver(instance, *args, **kwargs): 
    customer = stripe.Customer.create(email=instance.email)
    instance.customer_id = customer.id

pre_save.connect(payment_profile_pre_save_receiver, sender=PaymentProfile)


# class Card(models.Model):
    

#     def __str__(self):
#         return 