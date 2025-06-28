from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import RecommendView, UserRoadmapListView, RoadmapCoursesView

router = DefaultRouter()
# router.register(r'questions', QuestionViewSet, basename='question')  # استخدم ViewSet بدلاً من Serializer
# router.register(r'answers', AnswerViewSet, basename='answer')        # استخدم ViewSet بدلاً من Serializer

urlpatterns = [
    # path('signup/questionnaire/questionnaire_view', views.questionnaire_view, name='questionnaire_view'),
    # path('quiz_view', views.quiz_view, name='quiz_view'),
    # path('quiz_form/questionnaire_completed/', views.questionnaire_completed, name='questionnaire_completed'),
    path('api/', include(router.urls)),  # تضمين API المسارات الصحيحة
    # path('api/submit-quiz/', submit_quiz, name='submit_quiz'),
    # path("chat/", views.chat_with_llm, name="chat_with_llm"),
    # path('save-answer/', save_answer, name='save_answer'),
    # path('recommendations/', get_recommendations, name='recommendations'),
    path('recommendations/', RecommendView.as_view(), name='recommendations'),
    path('roadmapID/', UserRoadmapListView.as_view(), name='user-roadmaps'),
    path('roadmapCourses/', RoadmapCoursesView.as_view(), name='roadmap-courses'),
]