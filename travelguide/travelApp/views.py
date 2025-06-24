from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SignUpForm, TripForm
from .models import Account, MyTrip, TravelPlan
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Now
from django.utils.timezone import now

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
    form = TripForm()
    available_trips = TravelPlan.objects.filter(number_of_people__gt=0)
    form_submitted = False
    no_trips = False

    if request.method == 'POST':
        if 'search' in request.POST:
            form = TripForm(request.POST)
            form_submitted = True

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
            num_people = int(request.POST.get('number_of_people', 1))

            plan = get_object_or_404(TravelPlan, id=trip_id)

            if plan.number_of_people >= num_people:
                MyTrip.objects.create(
                    user=request.user,
                    travel_plan=plan,
                    start_destination=plan.start_destination,
                    end_destination=plan.end_destination,
                    start_date=plan.start_date,
                    end_date=plan.end_date,
                    number_of_people=int(request.POST.get('number_of_people', 1))
                )

                plan.number_of_people -= num_people
                plan.save()

                return redirect('travelApp:my_trips')
            else:
                form = TripForm()
                available_trips = []
                no_trips = True
                form_submitted = True

    return render(request, 'travelApp/planTrip.html', {
        'form': form,
        'available_trips': available_trips,
        'form_submitted': form_submitted,
        'no_trips': no_trips
    })

@login_required
def my_trips(request):
    if request.method == 'POST' and 'delete_trip_id' in request.POST:
        trip_id = request.POST.get('delete_trip_id')
        trip = get_object_or_404(MyTrip, id=trip_id, user=request.user)

        if trip.travel_plan:
            trip.travel_plan.number_of_people += trip.number_of_people
            trip.travel_plan.save()

        trip.delete()
        return redirect('travelApp:my_trips')

    trips = MyTrip.objects.filter(user=request.user).order_by('-booked_at')
    return render(request, 'travelApp/myTrips.html', {'trips': trips})

@login_required
def profile(request):
    trips = MyTrip.objects.filter(user=request.user).select_related('travel_plan').order_by('-booked_at')[:5]
    all_user_trips = MyTrip.objects.filter(user=request.user).order_by('-booked_at')
    recent_trips = all_user_trips.filter(end_date__lt=now()).order_by('-end_date')
    upcoming_trips = all_user_trips.filter(start_date__gte=Now()).count()  
    total_spent = trips.aggregate(total=Sum('travel_plan__price'))['total'] or 0
    total_trips = all_user_trips.count()
    account = Account.objects.filter(user=request.user).first()

    return render(request, 'travelApp/profile.html', {
        'recent_trips': recent_trips,
        'total_trips': total_trips,
        'total_spent': total_spent,
        'upcoming_trips': upcoming_trips,
        'account': account,
    })
