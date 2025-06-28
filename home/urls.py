# home/urls.py
from django.urls import path
from .views import homepage

urlpatterns = [
    path('', homepage, name='homepage'),  # This maps the home page URL
]
# home/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page
    path('questionnaire/', views.questionnaire_view, name='questionnaire_view'),  # Questionnaire page
    path('roadmap/', views.roadmap_view, name='flowchart'),  # Roadmap page
    path('login/', views.login_view, name='login'),  # Login page
    path('signup/', views.signup_view, name='signup'),  # Sign-up page
]
