from django.urls import path, include
from django.views.generic import TemplateView

from applicantprofile import views

urlpatterns = [
    path('home/', views.ApplicantHome.as_view(), name='applicant_home'),
]