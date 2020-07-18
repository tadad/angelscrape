from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Company, Investor
from django.template import loader
from .forms import CompanyQueryForm

def index(request):
    num_companies = Company.objects.count()
    num_investors = Investor.objects.count()
    top_companies_list = Company.objects.order_by('name')[:100]
    if request.method == "GET":
        form = CompanyQueryForm(request.GET)
        if form.is_valid():
            if form.cleaned_data["year_founded"] == True:
                top_companies_list = sorted(Company.objects.all(), key=lambda x: (x is None, -x.year_founded) )[:100]
            elif form.cleaned_data["most_investors"] == True:
                top_companies_list = sorted(Company.objects.all(), key=lambda x: -len(x.investors.all()))[:20]

    else:
        form = CompanyQueryForm()

    context = {
        'top_companies_list':top_companies_list,
        'form':form,
        'num_companies':num_companies,
        'num_investors':num_investors,
    }
    return render(request, 'database_interface/index.html', context)

def investors_index(request):
    investors = Investor.objects.order_by('name')
    context = {
        'investors':investors,
    }
    return render(request, 'database_interface/investors_index.html', context)

def detail_company(request, name):
    company = get_object_or_404(Company, pk=name)
    return render(request, 'database_interface/detail_company.html', {'company':company})

def detail_investor(request, name):
    investor = get_object_or_404(Investor, pk=name)
    context = {
        'investor': investor,
    }
    return render(request, 'database_interface/detail_investor.html', context)


