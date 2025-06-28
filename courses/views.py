from rest_framework import viewsets
from .models import playlist
from .serializers import PlaylistSerializer
from django.shortcuts import render

# View for Playlists
class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = playlist.objects.all()
    serializer_class = PlaylistSerializer

# # View for Answers
# class AnswerViewSet(viewsets.ModelViewSet):
#     queryset = Answer.objects.all()
#     serializer_class = AnswerSerializer

# View for Tracks
# class TrackViewSet(viewsets.ModelViewSet):
#     queryset = Tracks.objects.all()
#     serializer_class = TrackSerializer

# View for Courses


# class CourseViewSet(viewsets.ModelViewSet):
#     queryset = Courses.objects.all()
#     serializer_class = CourseSerializer

#     def list(self, request, *args, **kwargs):
#         print("Courses ViewSet is being accessed.")  # سيتم طباعتها في السجل عند الوصول للـ API
#         return super().list(request, *args, **kwargs)



# Rendering a template for all courses
# def get_courses(request):
#     playlists = playlist.objects.all()  # Fetch all playlists
#     return render(request, 'courses/all_courses.html', {'playlists': playlists})
import requests
from django.shortcuts import render
from .models import playlist

def get_courses(request):
    # Fetch playlists from the database
    db_playlists = playlist.objects.values()  # Converts QuerySet to dictionaries

    # Fetch playlists from an external API
    api_url = "https://example.com/api/playlists/"  # Replace with actual API URL
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        api_playlists = response.json()  # Assuming API returns JSON list of playlists
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        api_playlists = []

    # Combine database playlists and API playlists
    all_playlists = list(db_playlists) + api_playlists

    return render(request, 'courses/all_courses.html', {'playlists': all_playlists})
