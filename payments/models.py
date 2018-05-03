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

    @property
    def default_card(self):
        qs = self.card_set.filter(default=True)
        return qs.first()

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
    

def voucher_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.voucher_id:
        instance.voucher_id = random_string_generator(size=5) + str(current_time_milli())
    
pre_save.connect(voucher_pre_save_receiver, sender=Voucher)


class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Created'),
        ('paid', 'Paid'),
        ('abandoned', 'Abandoned'),
    )
    order_id        = models.CharField(max_length=50)
    payment_profile = models.ForeignKey(PaymentProfile, on_delete=models.CASCADE, blank=True, null=True)
    quantity        = models.PositiveIntegerField(default=1)
    total_amount    = models.DecimalField(default=0.00, max_digits=50, decimal_places=2)
    status          = models.CharField(max_length=50, choices=STATUS_CHOICES, default='created')
    active          = models.BooleanField(default=True)
    created_on      = models.DateTimeField(auto_now_add=True)
    updated_on      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

def order_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = random_string_generator() + str(current_time_milli())
    instance.total_amount = Decimal(instance.quantity) * Decimal(10.00)
    
pre_save.connect(order_pre_save_receiver, sender=Order)


def order_post_save_receiver(sender, created, instance, *args, **kwargs):
    if created:
        qs = Order.objects.filter(payment_profile=instance.payment_profile, active=True).exclude(id=instance.id)
        if qs.exists():
            qs.update(active=False, status='abandoned')

post_save.connect(order_post_save_receiver, sender=Order)


class ChargeManager(models.Manager):
    def take(self, payment_profile, order):
        card = payment_profile.default_card
        if card is None:
            return False, 'You dont have any Card to Perform this transaction!'
        charge = stripe.Charge.create(
                amount= int(order.total_amount)*100,
                currency="usd",
                customer=payment_profile.customer_id,
                source=card.card_id,
                description="Voucher purchase by {0}".format(payment_profile.user.email),
                metadata={'order_id':order.order_id}
            )

        new_charge = self.model.objects.create(
            charge_id = charge.id,     
            payment_profile = payment_profile,
            order = order,
            paid = charge.paid,        
            refunded = charge.refunded,      
            outcome = charge.outcome,       
            outcome_type = charge.outcome.get('type'), 
            seller_message = charge.outcome.get('seller_message'),
            risk_level = charge.outcome.get('risk_level')
        )

        if new_charge.paid:
            order.active=False 
            order.status='paid'
            order.save()

        return new_charge.paid, new_charge.seller_message

class Charge(models.Model):
    charge_id               = models.CharField(max_length=120)
    payment_profile         = models.ForeignKey(PaymentProfile, on_delete=models.CASCADE)
    order                   = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    paid                    = models.BooleanField(default=False)
    refunded                = models.BooleanField(default=False)
    outcome                 = models.TextField(null=True, blank=True)
    outcome_type            = models.CharField(max_length=120, null=True, blank=True)
    seller_message          = models.CharField(max_length=120, null=True, blank=True)
    risk_level              = models.CharField(max_length=120, null=True, blank=True)

    objects                 = ChargeManager()


def charge_post_save_receiver(sender, created, instance, *args, **kwargs):
    if created:
        quantity = int(instance.order.quantity)
        company = instance.payment_profile.user.company
        for v in range(quantity):
            Voucher.objects.create(company=company)
        
post_save.connect(charge_post_save_receiver, sender=Charge)
