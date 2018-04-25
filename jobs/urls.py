from django.urls import path

from jobs import views

urlpatterns = [
    path('apply/', views.JobApply.as_view(), name='job_apply'),
    path('<slug:slug>/', views.JobDetail.as_view(), name='job'),
    path('', views.JobList.as_view(), name='jobs'),
]
