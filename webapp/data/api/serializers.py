from rest_framework import serializers
from ..models import Company, Investor, Tag

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ('name', 'company_set')

class SmallInvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ('name',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class CompanySerializer(serializers.ModelSerializer):
    tag_set = TagSerializer(many=True, required=False)
    investors = SmallInvestorSerializer(many=True)
    class Meta:
        model = Company
        fields = '__all__'
        depth = 2


