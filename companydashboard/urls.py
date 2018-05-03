from django.urls import path
from django.views.generic import TemplateView

from jobs import views as jobviews
from payments import views as payviews
from .views import CompanyHome

urlpatterns = [
    path('order/success/', payviews.CheckoutSuccess.as_view(), name='checkout_success'),
    path('order/checkout/', payviews.CheckoutView.as_view(), name='checkout'),
    path('order/create', payviews.MakeOrder.as_view(), name='buy_voucher'),
    path('payment/cards', payviews.AddCard.as_view(), name='cards'),
    path('job/delete/<int:pk>/', jobviews.JobDelete.as_view(extra_context={'title': 'Delete Job'}), name='job_delete'),
    path('job/update/<int:pk>/', jobviews.JobUpdate.as_view(extra_context={'title': 'Update Job'}), name='job_update'),
    path('job/create/', jobviews.JobCreate.as_view(extra_context={'title': 'Create Job'}), name='job_create'),
    path('job/<int:pk>', jobviews.JobsByCompanyDetail.as_view(), name='company_job_detail'),
    path('jobs/', jobviews.JobsByCompany.as_view(), name='company_jobs'),
    path('home/', CompanyHome.as_view(), name='company_home'),
]
