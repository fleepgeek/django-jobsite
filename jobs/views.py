from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView, View
from django.contrib import messages

from .models import Job, Application
from accounts.mixins import ApplicantRequiredMixin

class JobList(ListView):
    model = Job

class JobDetail(DetailView):
    model = Job
    template_name='jobs/job_detail.html'

class JobApply(ApplicantRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        job_id = request.GET.get('job_id')
        job = get_object_or_404(Job, pk=job_id)
        context = {
            'job': job,
        }
        return render(request, 'jobs/job_apply.html', context)

    def post(self, request, *args, **kwargs):
        job_id = request.GET.get('job_id')
        job = get_object_or_404(Job, pk=job_id)
        obj, created = Application.objects.get_or_apply(request, job)
        if not created:
            messages.info(request, 'You already applied for this job')
        else:
            messages.success(request, 'Thanks for your Application')
        return redirect('job', job.slug)
