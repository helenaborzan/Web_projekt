from django.db import models
from django.contrib.auth.models import User

class TravelPlan(models.Model):
    name = models.CharField(max_length=100)
    start_destination = models.CharField(max_length=100)
    end_destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_people = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.start_destination} → {self.end_destination})"
    
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    mail = models.CharField(max_length=50)

    def __str__(self):
        return f'User: {self.name}'
    
class MyTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_trips')
    start_destination = models.CharField(max_length=100)
    end_destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s trip: {self.start_destination} → {self.end_destination}"


