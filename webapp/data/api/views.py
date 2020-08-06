from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q, Count
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated


from ..models import Company, Investor
from .serializers import CompanySerializer, InvestorSerializer

@login_required
@api_view(['GET', ])
def api_detail_company_view(request, slug):
    try:
        company = Company.objects.get(slug=slug)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CompanySerializer(company)
        return Response(serializer.data)

@login_required
@api_view(['GET', ])
def api_detail_investor_view(request, slug):
    try:
        investor = Investor.objects.get(slug=slug)
    except Investor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = InvestorSerializer(investor)
        return Response(serializer.data)


class ApiCompanyListView(ListAPIView):
    def get_queryset(self):
        theMap = {
            'Ag&Food': 'Ag & Food',
            'Cleantech': 'Cleantech',
            'Consumer': 'Consumer',
            'Real-Estate/Construction': 'Real Estate/Construction',
            'Health-IT': 'Health IT',
            'Industrials': 'Industrial Tech',
            'Fintech': 'Fintech',
            'Enterprise': 'Enterprise',
            'Other-Verticals': 'Other Verticals',
        }

        queryset = Company.objects.all()
        for vertical in theMap.keys():
            if self.request.query_params.get(vertical) == 'on':
                queryset = queryset.filter(verticals=theMap[vertical])

        return queryset.filter(Q(relevant=None) | Q(relevant=True)).annotate(num_investors=Count('investors')).order_by("-num_investors")

    serializer_class = CompanySerializer
    pagination_class = PageNumberPagination
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ('^name', '^description', '^location', 'website', 'investors__name',)
