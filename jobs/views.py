from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Job, Application
from accounts.mixins import ApplicantRequiredMixin, CompanyRequiredMixin
from accounts.models import Company


class JobList(ListView):
    model = Job

class JobDetail(DetailView):
    model = Job
    template_name='jobs/job_detail.html'


class JobCreate(CompanyRequiredMixin, CreateView):
    model = Job
    fields = ('title', 'industry', 'job_type', 'min_qualification', 'years_of_exp', 'salary', 'description',)

    def form_valid(self, form):
        form.instance.company = self.request.user.company
        return super().form_valid(form)


class JobUpdate(CompanyRequiredMixin, UpdateView):
    model = Job
    fields = ('title', 'industry', 'job_type', 'min_qualification', 'years_of_exp', 'salary', 'description',)

class JobDelete(CompanyRequiredMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobs')


class JobsByCompany(CompanyRequiredMixin, ListView):
    template_name = 'companydashboard/job_list.html'
    company = None
    def get_queryset(self):
        self.company = self.request.user.company
        jobs = Job.objects.filter(company=self.company)
        return jobs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = self.company
        return context

class JobsByCompanyDetail(CompanyRequiredMixin, DetailView):
    model = Job
    template_name = 'companydashboard/job_detail.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        applications = Application.objects.filter(job=self.get_object())
        context['applications'] = applications
        return context
    


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
