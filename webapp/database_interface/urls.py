from django.urls import path

from . import views

app_name = 'database_interface'
urlpatterns = [
    path('', views.index, name='index'),
    path('investors', views.investors_index, name='investors_index'),
    path('investors/<str:name>', views.detail_investor, name='detail_investor'),
    path('<str:name>/', views.detail_company, name='detail_company'),
]