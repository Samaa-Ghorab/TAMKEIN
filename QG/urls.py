from django.urls import path
from .views import MCQGenerationView, MCQListView, GenerateQuizAPIView, GenerateReportView

urlpatterns = [
    path('generate-mcq/', MCQGenerationView.as_view(), name='generate_mcq'),
    path('mcq-list/', MCQListView.as_view(), name='mcq_list'),
    path('generate-quiz/', GenerateQuizAPIView.as_view(), name='generate-quiz'),
    path("generate-report/", GenerateReportView.as_view(), name="generate_report"),
]
