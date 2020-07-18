from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
#from ..database_interface.models import Company, Investor


def index(request):
    #all_companies = len(Company.objects.all())
    #all_investors = len(Investor.Objects.all())
    context = {
    #    'all_companies':all_companies,
    #    'all_investors':all_investors,
    }
    return render(request, 'templates/index.html', context)
