from django.urls import path

from jobs import views

urlpatterns = [
    path('delete/<int:pk>/', views.JobDelete.as_view(extra_context={'title': 'Delete Job'}), name='job_delete'),
    path('update/<int:pk>/', views.JobUpdate.as_view(extra_context={'title': 'Update Job'}), name='job_update'),
    path('create/', views.JobCreate.as_view(extra_context={'title': 'Create Job'}), name='job_create'),
    path('company/job/<int:pk>', views.JobsByCompanyDetail.as_view(), name='company_job_detail'),
    path('company/', views.JobsByCompany.as_view(), name='company_jobs'),
    path('apply/', views.JobApply.as_view(), name='job_apply'),
    path('<slug:slug>/', views.JobDetail.as_view(), name='job'),
    path('', views.JobList.as_view(), name='jobs'),
]
