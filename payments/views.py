from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, DetailView
from django.http import JsonResponse, HttpResponse
from django.urls import reverse

from .models import PaymentProfile, Card, Voucher, Order, Charge
from accounts.mixins import CompanyRequiredMixin


class AddCard(CompanyRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cards = request.user.paymentprofile.card_set.all()
        return render(request, 'companydashboard/cards.html', {'cards':cards})

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            payment_profile, created = PaymentProfile.objects.get_or_create(user=request.user)
            if not payment_profile:
                return JsonResponse({'msg': 'Your profile does not exist!'}, status_code=404)
            
            token = request.POST.get('token')
            new_card = Card.objects.new(token=token, payment_profile=payment_profile)
            return JsonResponse({'msg': 'Token Success'})
        return HttpResponse('error', status_code=401)


class MakeOrder(CreateView):
    model = Order
    fields = ('quantity',)
    template_name = 'companydashboard/make_order.html'

    def form_valid(self, form):
        request = self.request
        form.instance.payment_profile = request.user.paymentprofile
        return super(MakeOrder, self).form_valid(form)

    def get_success_url(self):
        return reverse('checkout')



class CheckoutView(CompanyRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        qs = Order.objects.filter(payment_profile=request.user.paymentprofile, active=True)
        order = qs.first()
        context = {
            'order': order
        }
        if order is None:
            return redirect('make_order')
        return render(request, 'payments/checkout.html', context)
    
    def post(self, request, *args, **kwargs):
        order_id = request.POST.get('order_id')
        order = Order.objects.get(order_id=order_id)
        payment_profile, created = PaymentProfile.objects.get_or_create(user=request.user)
        paid, message = Charge.objects.take(payment_profile, order)
        if paid:
            return redirect('checkout_success')
        context = {
            'charge_error': True,
            'error_message': 'An Error Occured, Please Try again'
        }
        return render(request, 'payments/checkout.html', context)


