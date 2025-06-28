from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaylistViewSet, get_courses

router = DefaultRouter()
router.register(r'playlists', PlaylistViewSet)
# router.register(r'tracks', TrackViewSet)
# router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),  # API endpoints
    path('all_courses/', get_courses, name='all_courses'),  # Template for all courses
]
