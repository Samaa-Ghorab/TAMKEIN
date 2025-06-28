# from django import forms

# class InitialQuestionnaireForm(forms.Form):
#     DISABILITY_CHOICES = [
#         ("yes", "Yes"),
#         ("no", "No"),
#     ]

#     CS_KNOWLEDGE_CHOICES = [
#         ("yes", "Yes"),
#         ("no", "No"),
#     ]

#     TRACK_CHOICES = [
#         ("data_science", "Data Science"),
#         ("web_dev", "Web Development"),
#         ("ai", "Artificial Intelligence"),
#     ]

#     LEVEL_CHOICES = [
#         ("beginner", "Beginner"),
#         ("intermediate", "Intermediate"),
#         ("advanced", "Advanced"),
#     ]

#     disability = forms.ChoiceField(
#         choices=DISABILITY_CHOICES, widget=forms.RadioSelect, label="Do you have any disability?"
#     )
#     cs_knowledge = forms.ChoiceField(
#         choices=CS_KNOWLEDGE_CHOICES, widget=forms.RadioSelect, label="Do you have previous knowledge in CS?"
#     )
#     track = forms.ChoiceField(
#         choices=TRACK_CHOICES, widget=forms.Select, label="What is your primary interest?"
#     )
#     level = forms.ChoiceField(
#         choices=LEVEL_CHOICES, widget=forms.Select, label="What is your level in the chosen track?"
#     )
from django import forms
from .models import Answer, Question

class AnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(queryset=Question.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = Answer
        fields = ['question', 'answer', 'is_correct']
