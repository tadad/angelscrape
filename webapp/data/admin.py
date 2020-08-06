from django.contrib import admin

from .models import Company, Investor, Tag, Vertical

admin.site.register(Company)
admin.site.register(Investor)
admin.site.register(Tag)
admin.site.register(Vertical)

