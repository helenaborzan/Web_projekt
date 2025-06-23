from django.contrib import admin
from .models import TravelPlan, MyTrip, Account

admin.site.register(Account)
admin.site.register(TravelPlan) 
admin.site.register(MyTrip)
