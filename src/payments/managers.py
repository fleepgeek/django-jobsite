from django.db import models

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


class VoucherManager(models.Manager):
    def all(self):
        return self.get_queryset().filter(active=True) # selects only active vouchers



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