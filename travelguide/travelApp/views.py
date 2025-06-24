from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SignUpForm, TripForm
from .models import Account, MyTrip, TravelPlan
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

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

@login_required
def plan_trip(request):
    available_trips = None
    no_trips = False

    if request.method == 'POST':
        if 'search' in request.POST:
            form = TripForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                available_trips = TravelPlan.objects.filter(
                    start_destination__iexact=cd['start_destination'],
                    end_destination__iexact=cd['end_destination'],
                    start_date__gte=cd['start_date'],
                    end_date__lte=cd['end_date'],
                    number_of_people__gte=cd['number_of_people']
                )
                if not available_trips.exists():
                    no_trips = True
        elif 'book_trip_id' in request.POST:
            trip_id = request.POST.get('book_trip_id')
            plan = get_object_or_404(TravelPlan, id=trip_id)
            MyTrip.objects.create(
                user=request.user,
                start_destination=plan.start_destination,
                end_destination=plan.end_destination,
                start_date=plan.start_date,
                end_date=plan.end_date
            )
            return redirect('travelApp:my_trips')
    else:
        form = TripForm()

    return render(request, 'travelApp/planTrip.html', {
        'form': form,
        'available_trips': available_trips,
        'no_trips': no_trips
    })

@login_required
def my_trips(request):
    trips = MyTrip.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'travelApp/myTrips.html', {'trips': trips})
