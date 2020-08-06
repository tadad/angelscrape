from django.urls import path

from . import views
from .views import CompanyListView, CompanyDetailView

app_name = 'data'
urlpatterns = [
    path('', CompanyListView.as_view(), name='index'),
    path('investors', views.investors_index, name='investors_index'),
    path('investors/<slug:slug>/', views.investor_detail, name='investor_detail'),
    path('companies/<slug:slug>/', CompanyDetailView.as_view(), name='company_detail'),
]