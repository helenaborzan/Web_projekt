from django.urls import path

from . import views

app_name = 'travelApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('plan-trip/', views.plan_trip, name='plan_trip'),
    path('my-trips/', views.my_trips, name='my_trips'),
    path('profile/', views.profile, name='profile'),
    path('trip/<int:trip_id>/', views.trip_details, name='trip_details'),
    path('add-trip/', views.add_trip, name='add_trip'),
    path('trip-success/', views.trip_success, name='trip_success'),
    path('edit-trips/', views.edit_trips, name='edit_trips'),
    path('delete-trip/<int:trip_id>/', views.delete_trip, name='delete_trip'),
    path('api/trips/', views.TravelPlanListCreateAPIView.as_view(), name='api_trips'),
    path('api/accounts/', views.AccountListCreateAPIView.as_view(), name='api_accounts'),
    path('api/my-trips/', views.MyTripListCreateAPIView.as_view(), name='api_my_trips'),
    path('api/trip-questions/', views.TripQuestionListCreateAPIView.as_view(), name='api_trip_questions'),
    path('api/trip-answers/', views.TripAnswerListCreateAPIView.as_view(), name='api_trip_answers'),
    path('api/upcoming-trips/', views.UpcomingTripsAPIView.as_view(), name='api_upcoming_trips'),
    path('api/trips/<int:pk>/', views.TravelPlanDetailAPIView.as_view(), name='api_trip_detail')
]