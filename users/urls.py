from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from . import views
from .views import SignupView, get_user_data, get_quiz_results

# from questionnaire.views import quiz_questions_view

router = DefaultRouter()
router.register(r'users', UserViewSet)



urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('user_questions/', views.user_questions, name='user_questions'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('quiz/', views.get_quiz_data, name='get_quiz_data'),
    # path('get-questions/', views.get_questions, name='get_questions'),  # Add this
    path('', views.UserListView.as_view(), name='user-list'),
    # path('submit-quiz/', views.submit_quiz, name='submit_quiz'),
    path('signup/', SignupView.as_view(), name='signup_api'),
    # # path('submit/', views.submit_form, name='submit_form'),
    path('userData/<int:user_id>/', get_user_data, name='userData'),
    path('quizScore/<int:user_id>/', get_quiz_results, name='quizData'),
]

