from django.urls import path
from .views import TextToSpeechView, SpeechToTextAPI

urlpatterns = [
    path('generate/', TextToSpeechView.as_view(), name='text-to-speech'),
    path("transcribe/", SpeechToTextAPI.as_view(), name="transcribe"),
]
