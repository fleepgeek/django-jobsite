from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, FormView, View

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
        applicant = request.user.applicant
        qs = Application.objects.filter(job=job, applicant=applicant)
        if qs.exists():
            print("You already applied for this job")
        else:
            Application.objects.create(job=job, applicant=applicant)
        return redirect('job', job.slug)
