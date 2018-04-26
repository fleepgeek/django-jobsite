from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView, FormView, UpdateView
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
        complete_profile = reverse('reg_profile', kwargs={'pk': user.applicant.pk})
        return redirect(complete_profile)

class UpdateApplicant(ApplicantRequiredMixin, UpdateView):
    model = Applicant
    fields = ('date_of_birth','location', 'gender', 'about', 'years_of_exp')
    template_name = 'accounts/complete_reg.html'
    success_url = '/applicant/home'


class ApplicantHome(ApplicantRequiredMixin, TemplateView):
    template_name='accounts/applicant_home.html'


class CompanySignUp(CreateView):
    model = Company
    form_class = CompanySignUpForm
    template_name = 'accounts/signup.html'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        complete_company = reverse('reg_company', kwargs={'pk': user.company.pk})
        return redirect(complete_company)


class UpdateCompany(CompanyRequiredMixin, UpdateView):
    model = Company
    fields = ('name', 'description', 'website', 'country', 'state')
    template_name = 'accounts/complete_reg.html'
    success_url = '/company/home'


class LoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get_success_url(self):
        next_get = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        next_url = next_get or next_post or None
        if next_url is not None:
            return next_url
            
        if self.request.user.is_applicant:  
            return '/applicant/home/'
        if self.request.user.is_employer:
            return '/company/home/'