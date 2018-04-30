from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponse

from .models import PaymentProfile, Card
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

