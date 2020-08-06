from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserReigisterForm(UserCreationForm):
    email = forms.EmailField()

    def clean_email(self):
        data = self.cleaned_data['email']
        if "@builders.vc" not in data:
            raise forms.ValidationError("You cannot use that email for this website")
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']