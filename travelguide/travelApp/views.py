from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import SignUpForm, TripForm, TravelPlanForm
from .models import Account, MyTrip, TravelPlan
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Now
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator
from .models import TravelPlan, MyTrip, TripQuestion, TripAnswer

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
    today = now().date()
    form_submitted = False
    no_trips = False

    available_trips = TravelPlan.objects.filter(
        number_of_people__gt=0,
        start_date__gte=today
    )

    if request.method == 'POST':
        if 'search' in request.POST:
            form = TripForm(request.POST)
            form_submitted = True

            if form.is_valid():
                cd = form.cleaned_data

                available_trips = TravelPlan.objects.filter(
                    start_destination__iexact=cd['start_destination'],
                    end_destination__iexact=cd['end_destination'],
                    start_date__gte=max(cd['start_date'], today),
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
                    number_of_people=num_people
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


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date

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

    all_trips = MyTrip.objects.filter(user=request.user).order_by('-start_date')
    
    today = date.today()
    
    current_trips = []
    upcoming_trips = []
    past_trips = []
    
    for trip in all_trips:
        if trip.start_date <= today <= trip.end_date:
            current_trips.append(trip)
        elif trip.start_date > today:
            upcoming_trips.append(trip)
        else:
            past_trips.append(trip)
    
    current_trips.sort(key=lambda x: x.start_date, reverse=True)
    
    upcoming_trips.sort(key=lambda x: x.start_date)
    
    past_trips.sort(key=lambda x: x.end_date, reverse=True)
    
    context = {
        'current_trips': current_trips,
        'upcoming_trips': upcoming_trips,
        'past_trips': past_trips,
    }
    
    return render(request, 'travelApp/myTrips.html', context)

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

@login_required
def trip_details(request, trip_id):
    trip = get_object_or_404(TravelPlan, id=trip_id)
    
    user_booking = MyTrip.objects.filter(user=request.user, travel_plan=trip).first()
    already_booked = user_booking is not None

    if request.method == 'POST':
        if 'book_trip_id' in request.POST:
            num_people = int(request.POST.get('number_of_people', 1))

            if already_booked:
                messages.error(request, "You have already booked this trip.")
            elif num_people > trip.number_of_people:
                messages.error(request, "Not enough available spots for the number of people selected.")
            else:
                MyTrip.objects.create(
                    user=request.user,
                    travel_plan=trip,
                    start_destination=trip.start_destination,
                    end_destination=trip.end_destination,
                    start_date=trip.start_date,
                    end_date=trip.end_date,
                    number_of_people=num_people
                )
                trip.number_of_people -= num_people
                trip.save()
                messages.success(request, "Trip booked successfully!")
                return redirect('travelApp:my_trips')

        elif 'submit_question' in request.POST:
            question_text = request.POST.get('question_text', '').strip()
            if question_text:
                TripQuestion.objects.create(
                    trip=trip,
                    user=request.user,
                    question_text=question_text
                )
                messages.success(request, "Your question has been submitted successfully!")
            else:
                messages.error(request, "Please enter a question before submitting.")
            return redirect('travelApp:trip_details', trip_id=trip.id)

        elif 'submit_answer' in request.POST and request.user.is_staff:
            question_id = request.POST.get('question_id')
            answer_text = request.POST.get('answer_text', '').strip()
            
            if question_id and answer_text:
                try:
                    question = TripQuestion.objects.get(id=question_id, trip=trip)
                    if not hasattr(question, 'answer'):
                        TripAnswer.objects.create(
                            question=question,
                            admin_user=request.user,
                            answer_text=answer_text
                        )
                        messages.success(request, "Answer submitted successfully!")
                    else:
                        messages.error(request, "This question has already been answered.")
                except TripQuestion.DoesNotExist:
                    messages.error(request, "Question not found.")
            else:
                messages.error(request, "Please provide an answer before submitting.")
            return redirect('travelApp:trip_details', trip_id=trip.id)

    questions = TripQuestion.objects.filter(trip=trip).select_related('user').prefetch_related('answer__admin_user')
    
    paginator = Paginator(questions, 10)  
    page_number = request.GET.get('page')
    questions_page = paginator.get_page(page_number)

    context = {
        'trip': trip,
        'already_booked': already_booked,
        'user_booking': user_booking,
        'questions': questions_page,
        'is_staff': request.user.is_staff,
    }
    return render(request, 'travelApp/tripDetails.html', context)

@staff_member_required
def add_trip(request):
    if request.method == 'POST':
        form = TravelPlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('travelApp:trip_success')
    else:
        form = TravelPlanForm()
    return render(request, 'travelApp/addTrip.html', {'form': form})

@staff_member_required
def trip_success(request):
    return render(request, 'travelApp/tripSuccess.html')

@staff_member_required
def edit_trips(request):
    upcoming_trips = TravelPlan.objects.filter(start_date__gte=now())
    return render(request, 'travelApp/editTrips.html', {'upcoming_trips': upcoming_trips})

@staff_member_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(TravelPlan, id=trip_id)
    trip.delete()
    messages.success(request, "Trip deleted successfully.")
    return redirect('travelApp:edit_trips')