from django import forms

class CompanyQueryForm(forms.Form):
    most_investors = forms.BooleanField(label="Most Investors", required=False)
    YC = forms.BooleanField(label="Y-Combinator", required=False)
    Alexis_Ohanian = forms.BooleanField(label="Alexis Ohanian", required=False) # to get this to work I need to fix this
    Ben_Ling = forms.BooleanField(label="Ben Ling", required=False)
    Elad_Gil = forms.BooleanField(label="Elad Gil", required=False)
    Gaurav_Jain = forms.BooleanField(label="Gaurav Jain", required=False)
    Jude_Gomila = forms.BooleanField(label="Jude Gomila", required=False)
    Julia_Dewahl = forms.BooleanField(label="Julia Dewahl", required=False)
    Max_Levchin = forms.BooleanField(label="Max Levchin", required=False)
