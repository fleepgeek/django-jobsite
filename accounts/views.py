from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from .models import Applicant, Company
from .forms import ApplicantSignUpForm, CompanySignUpForm, LoginForm
from .mixins import ApplicantRequiredMixin, CompanyRequiredMixin

class ApplicantSignUp(CreateView):
    model = Applicant
    form_class = ApplicantSignUpForm
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('applicant-home')


class ApplicantHome(ApplicantRequiredMixin, TemplateView):
    template_name='accounts/applicant-home.html'


class CompanySignUp(CreateView):
    model = Company
    form_class = CompanySignUpForm
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('company-home')


class CompanyHome(CompanyRequiredMixin, TemplateView):
    template_name='accounts/company-home.html'


class LoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.is_applicant:
            return '/applicant/home/'
        if self.request.user.is_employer:
            return '/company/home/'