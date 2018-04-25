from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Job

class JobList(ListView):
    model = Job

class JobDetail(DetailView):
    model = Job
    template_name='jobs/job_detail.html'