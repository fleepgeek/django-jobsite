"""jobsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from .views import HomePage
from accounts.views import ApplicantSignUp, ApplicantHome, CompanySignUp, LoginView, UpdateApplicant, UpdateCompany


urlpatterns = [
    path('company/', include('companydashboard.urls')),
    path('jobs/', include('jobs.urls')),
    path('reg/company/<int:pk>/', UpdateCompany.as_view(extra_context={'title': 'Complete your Company\'s Profile'}), name='reg_company'),
    path('reg/profile/<int:pk>/', UpdateApplicant.as_view(extra_context={'title': 'Complete your Profile'}), name='reg_profile'),
    path('signup/company/', CompanySignUp.as_view(extra_context={'title': 'Employer SignUp'}), name='company_signup'),
    path('applicant/home/', ApplicantHome.as_view(), name='applicant_home'),
    path('signup/applicant/', ApplicantSignUp.as_view(extra_context={'title': 'Applicant SignUp'}), name='applicant_signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('', HomePage.as_view(), name='home'),
    path('admin/', admin.site.urls),
]
