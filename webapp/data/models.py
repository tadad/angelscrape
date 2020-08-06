"""
TODO: get rid of all original pull fields in the scrape scripts. I handled it here automatically
"""

from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from unidecode import unidecode
from django.urls import reverse

class Investor(models.Model):
    name = models.CharField(primary_key=True, max_length=50, default="NONAME")
    website = models.URLField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name.replace("_", " ")

    def get_companies(self):
        return self.company_set.all()

    def save(self, *args, **kwargs):
        self.name = unidecode(self.name)
        self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('investor_detail', kwargs={'slug':self.slug})

class Vertical(models.Model):
    name = models.CharField(max_length=50, primary_key=True, default="NONAME")

    def __str__(self):
        return self.name

class Company(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50, unique=False)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    year_founded = models.SmallIntegerField(blank=True, null=True)
    team_size = models.SmallIntegerField(blank=True, null=True)
    original_pull = models.DateField(blank=True, null=True, default=timezone.now)
    location = models.CharField(max_length=30, blank=True)
    funding = models.CharField(max_length=20, blank=True, null=True)
    relevant = models.BooleanField(blank=True, null=True)
    dead = models.BooleanField(blank=True, null=True)
    investors = models.ManyToManyField(Investor)
    verticals = models.ManyToManyField(Vertical, blank=True, null=True)


    def __str__(self):
        return self.name

    def get_investors_as_str(self):
        return ", ".join([inv.name.replace('_', ' ') for inv in self.investors.all()])

    def get_tags_as_str(self):
        return ", ".join([t.name for t in self.tag_set.all()])

    def get_tags_as_list(self):
        return [t.name for t in self.tag_set.all()]

    def num_investors(self):
        return self.investors.count()

    def get_absolute_url(self):
        return reverse('company_detail', kwargs={'slug':self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True, default="NONAME")
    companies = models.ManyToManyField(Company)

    def __str__(self):
        return self.name

    def get_companies(self):
        return self.company_set.all()
