from django.shortcuts import render
from django.views.generic import TemplateView

class ApplicantHome(TemplateView):
    template_name = 'applicantprofile/home.html'
