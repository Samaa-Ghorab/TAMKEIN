# roadmap/forms.py

from django import forms
from .models import Roadmap

class RoadmapForm(forms.ModelForm):
    class Meta:
        model = Roadmap
        fields = ['title', 'description']
