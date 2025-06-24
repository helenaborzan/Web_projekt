
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyTrip

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class TripForm(forms.Form):
    start_destination = forms.CharField(
        label="Start Destination",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    end_destination = forms.CharField(
        label="End Destination",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    number_of_people = forms.IntegerField(
        label="Number of People",
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

