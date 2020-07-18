from django.db import models

class Investor(models.Model):
    name = models.CharField(primary_key=True, max_length=50, default="NONAME")
    website = models.URLField(blank=True, null=True)
    """
    Add a sources field- angellist profile, personal website, etc.
    """
    def __str__(self):
        return (self.name).replace("-", " ")

    def get_companies(self):
        return self.company_set.all()

class Company(models.Model):
    name = models.CharField(primary_key=True, max_length=50, default="NONAME")
    description = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)
    year_founded = models.SmallIntegerField(blank=True, null=True)
    team_size = models.SmallIntegerField(blank=True, null=True)
    original_pull = models.DateField(blank=True, null=True)
    last_updated = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    stage = models.CharField(max_length=15, blank=True)
    total_raised = models.CharField(max_length=15, blank=True, null=True)
    investors = models.ManyToManyField(Investor)

    def __str__(self):
        return self.name.replace("-", " ")

    def get_investors_as_str(self):
        return ", ".join([inv.name for inv in self.investors.all()])

    def get_tags_as_str(self):
        return ", ".join([t.name for t in self.tag_set.all()])

    def get_tags_as_list(self):
        return [t.name for t in self.tag_set.all()]

class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True, default="NONAME")
    companies = models.ManyToManyField(Company)

    def __str__(self):
        return self.name

    def get_companies(self):
        return self.company_set.all()
