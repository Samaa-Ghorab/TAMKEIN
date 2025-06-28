# courses_website/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from home import views as home_views
from users import views as user_views  # إضافة views الخاصة بـ users
# from questionnaire.views import QuestionSerializer,AnswerSerializer
# from users.views import signup
# from questionnaire.views import questionnaire_view
from django.conf import settings
from django.conf.urls.static import static
# from roadmap.views import AnswerViewSet
# from courses.views import PlaylistViewSet
# from questionnaire.views import AnswerViewSet,QuestionViewSet
# from users.views import UserViewSet
# from recommendations.views import RecommendationViewSet


# Create a router for API viewsets
router = DefaultRouter()
# تسجيل UserViewSet و QuestionViewSet في الـ router
# router.register(r'users', UserViewSet)
# router.register(r'questions', QuestionViewSet)
# router.register(r'answers',AnswerViewSet)
# router.register(r'playlist',PlaylistViewSet)
# router.register(r'recommend', RecommendationViewSet, basename='recommend')

urlpatterns = [
    path('admin/', admin.site.urls),  # لوحة إدارة Django
    path('', home_views.homepage, name='homepage'),  # الصفحة الرئيسية للموقع
    # path('courses/', include('courses.urls')),  # مسارات خاصة بالدورات
    path('questions/', include('questionnaire.urls')),  # تضمين مسارات questionnaire
    path('users/', include('users.urls')),  # مسارات المستخدمين
    # path('roadmap/', include('roadmap.urls')),  # مسارات roadmap
    # path('signup/', signup_api, name='signup'),  # مسار تسجيل المستخدم
    # path('login/', login_api, name='login'),  
    # path('logout/', logout_api, name='logout'), 

    # API URLs
    path('api/', include(router.urls)),  # API لجميع المسارات المسجلة في router
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),  # API لتسجيل الدخول والخروج
    # path('questionnaire/quiz_form/', questionnaire_view, name='quiz_form'),  # مسار لـ questionnaire
    # path("recommendations/", include("recommendations.urls")),  # ربط التطبيق بالـ API
    # path('api/tts/', include('TTS.urls')),
    # path('api/chatbot/', include('chatbot.urls')),
    # path('qg/', include('QG.urls')),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
