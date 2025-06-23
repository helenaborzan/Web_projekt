from django.urls import path

from . import views

app_name = 'travelApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('plan-trip/', views.plan_trip, name='plan_trip'),
    path('my-trips/', views.my_trips, name='my_trips'),
]