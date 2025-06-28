from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TravelPlan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    picture_url = models.URLField(max_length=500, blank=True) 
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
    travel_plan = models.ForeignKey('TravelPlan', on_delete=models.CASCADE, null=True, blank=True)
    start_destination = models.CharField(max_length=100)
    end_destination = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    number_of_people = models.PositiveIntegerField(default=1)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s trip: {self.start_destination} → {self.end_destination}"

class TripQuestion(models.Model):
    trip = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='questions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    is_answered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Question by {self.user.username} for {self.trip.name}"

class TripAnswer(models.Model):
    question = models.OneToOneField(TripQuestion, on_delete=models.CASCADE, related_name='answer')
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    answer_text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Answer by {self.admin_user.username} to question {self.question.id}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.is_answered = True
        self.question.save()
