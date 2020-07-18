from django import forms

class CompanyQueryForm(forms.Form):
    year_founded = forms.BooleanField(label="Year Founded", required=False)
    most_investors = forms.BooleanField(label="Most Investors", required=False)

