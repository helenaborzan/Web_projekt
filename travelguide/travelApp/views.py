from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import SignUpForm
from .models import Account
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout


def home(request):
    return render (request, 'travelApp/home.html')

def custom_logout(request):
    logout(request)
    return redirect('/')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            
            Account.objects.create(
                user=user,
                name=username,
                mail=email,
            )
            
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
