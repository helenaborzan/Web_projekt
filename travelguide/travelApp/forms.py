
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MyTrip, TravelPlan
from django.utils import timezone

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

class TravelPlanForm(forms.ModelForm):
    class Meta:
        model = TravelPlan
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'picture_url': forms.URLInput(attrs={'class': 'form-control'}),
            'start_destination': forms.TextInput(attrs={'class': 'form-control'}),
            'end_destination': forms.TextInput(attrs={'class': 'form-control'}),
            'number_of_people': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        if start_date < timezone.now().date():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data.get('start_date')
        if start_date and end_date < start_date:
            raise forms.ValidationError("End date must be after the start date.")
        return end_date

