from django.shortcuts import render
from django.views.generic import TemplateView

from accounts.mixins import CompanyRequiredMixin

class CompanyHome(CompanyRequiredMixin, TemplateView):
    template_name='companydashboard/home.html'