from django.contrib import admin
from .models import TravelPlan, MyTrip, Account, TripQuestion, TripAnswer

admin.site.register(Account)
admin.site.register(TravelPlan) 
admin.site.register(MyTrip)

from django.contrib import admin
from .models import TripQuestion, TripAnswer

@admin.register(TripQuestion)
class TripQuestionAdmin(admin.ModelAdmin):
    list_display = ['trip', 'user', 'question_preview', 'is_answered', 'created_at']
    list_filter = ['is_answered', 'created_at', 'trip']
    search_fields = ['question_text', 'user__username', 'trip__name']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    def question_preview(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_preview.short_description = "Question Preview"

@admin.register(TripAnswer)
class TripAnswerAdmin(admin.ModelAdmin):
    list_display = ['question_trip', 'question_user', 'admin_user', 'answer_preview', 'created_at']
    list_filter = ['created_at', 'admin_user']
    search_fields = ['answer_text', 'question__question_text', 'admin_user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']

    def question_trip(self, obj):
        return obj.question.trip.name
    question_trip.short_description = "Trip"

    def question_user(self, obj):
        return obj.question.user.username
    question_user.short_description = "Question By"

    def answer_preview(self, obj):
        return obj.answer_text[:50] + "..." if len(obj.answer_text) > 50 else obj.answer_text
    answer_preview.short_description = "Answer Preview"
