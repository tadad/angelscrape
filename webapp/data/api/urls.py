from django.urls import path
from .views import (
    api_detail_company_view,
    api_detail_investor_view,
    ApiCompanyListView,
)


urlpatterns = [
    path('list/', ApiCompanyListView.as_view(), name='list'), # for some reason this has to be first
    path('<slug>/', api_detail_company_view, name="company_detail"),
    path('investor/<slug>/', api_detail_investor_view, name="investor_detail"),
]