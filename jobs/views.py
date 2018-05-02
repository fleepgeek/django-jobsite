from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Job, Application
from .forms import ApplicationForm
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

    
    def get_context_data(self, **kwargs):
        context = super(JobCreate, self).get_context_data(**kwargs)
        context['is_create'] = True
        return context

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
    


class JobApply(ApplicantRequiredMixin, CreateView):
    model = Application
    # form_class = ApplicationForm()
    template_name = 'jobs/job_apply.html'
    fields = ('resume', 'cover_letter',)

    def get_context_data(self, *args, **kwargs):
        context = super(JobApply, self).get_context_data(**kwargs)
        job_id = self.request.GET.get('job_id')
        self.job = get_object_or_404(Job, pk=job_id)
        context['job'] = self.job
        return context
    
    def form_valid(self, form, **kwargs):
        request = self.request
        job_id = request.GET.get('job_id')
        job = get_object_or_404(Job, pk=job_id)
        has_applied, msg = Application.objects.has_applied(request.user, job)
        if not has_applied:
            applicant = request.user.applicant
            form.instance.applicant = applicant
            form.instance.job = job
            form.save()
            messages.success(request, msg)
        else:
            messages.info(request, msg)

        return redirect('job', job.slug)
