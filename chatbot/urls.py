from django.urls import path
from .views import ChatbotAPIView, chatbot_page

urlpatterns = [
    path("chat/", ChatbotAPIView.as_view(), name="chatbot_api"),
    path("web/", chatbot_page, name="chatbot_web"),
]