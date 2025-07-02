from rest_framework import serializers
from .models import TravelPlan, Account, MyTrip, TripQuestion, TripAnswer
from django.contrib.auth.models import User

class TravelPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelPlan
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class MyTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyTrip
        fields = '__all__'

class TripQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripQuestion
        fields = '__all__'

class TripAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TripAnswer
        fields = '__all__'