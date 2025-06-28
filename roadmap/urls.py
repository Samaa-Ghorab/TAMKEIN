from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


# Create the router for API endpoints
# router = DefaultRouter()
# router.register(r'roadmaps', RoadmapViewSet)
# router.register(r'answers', AnswerViewSet)

urlpatterns = [
    # API routes
    # path('api/', include(router.urls)),  # Prefix API routes with 'api/'

    # View-based routes
    # path('flowchart/', views.flowchart_view, name='roadmap_flowchart'),  # Correct path for the flowchart view
    
]
