from django.urls import path
from .views import recommend_course

urlpatterns = [
    path("recommend/", recommend_course, name="recommend_course"),
]
