from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    handicap = forms.DecimalField(max_value=15.0, min_value=-4.0)
    bio = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows':5, 'placeholder':'Tell others about you'}
        ),
        max_length=4000,
        help_text='Max Length: 4000'
    )

    class Meta:
        model = Profile
        fields = ('handicap','bio')
