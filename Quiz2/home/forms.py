from django import forms
from .models import Quiz, Question, Answer,Hotel
from django.contrib import admin

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('name', 'desc', 'number_of_questions', 'time')

    
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('content', 'quiz')


class HotelForm(forms.ModelForm):

	class Meta:
		model = Hotel
		fields = ['name', 'hotel_Main_Img']
