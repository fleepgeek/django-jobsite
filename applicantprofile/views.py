from django.shortcuts import render
from django.views.generic import ListView
from django.conf import settings

from jobs.models import Application
from accounts.mixins import ApplicantRequiredMixin

User = settings.AUTH_USER_MODEL

class ApplicantHome(ApplicantRequiredMixin, ListView):
    model = Application
    template_name = 'applicantprofile/home.html'

    def get_queryset(self):
        applicant = self.request.user.applicant
        qs = Application.objects.filter(applicant=applicant)
        return qs
    
