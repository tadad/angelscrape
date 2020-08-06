import requests
from .models import Company, Investor
from .api.serializers import CompanySerializer

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination


class CompanyListView(LoginRequiredMixin, APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'data/index.html'
    model = Company
    serializer_class = CompanySerializer
    pagination_class = PageNumberPagination


    def get(self, request):
        payload = request.query_params
        queryset = requests.get("http://127.0.0.1:8000/api/list", params=payload).json()
        context = {
            'top_companies_list': queryset['results'],
            'count': queryset['count'],
            'on_page': len(queryset['results']),
            'num_companies': len(Company.objects.all()),
            'num_investors': len(Investor.objects.all()),
        }

        try:
            next = queryset['next'].split('/')[-1]
            context['next'] = next
        except:
            pass

        try:
            previous = queryset['previous'].split('/')[-1]
            context['previous'] = previous
        except:
            pass

        return Response(context)


class CompanyDetailView(LoginRequiredMixin, DetailView):
    model = Company


@login_required
def investors_index(request):
    investors = Investor.objects.order_by('name')
    context = {
        'investors':investors,
    }
    return render(request, 'data/investors_index.html', context)



@login_required
def investor_detail(request, slug):
    investor = get_object_or_404(Investor, slug=slug)
    context = {
        'investor': investor,
    }
    return render(request, 'data/investor_detail.html', context)


