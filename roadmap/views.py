from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# from .models import Roadmap


# def generate_roadmap(user):
#     """Generate a roadmap based on user answers."""
#     user_answers = Answer.objects.filter(userid=user.id)  # استخدم userid بدلاً من user_id
    
#     for user_answer in user_answers:
#         try:
#             answer = Answer.objects.get(answer_text=user_answer.answer)
#             if answer.track_url:
#                 return Roadmap.objects.create(user=user, title="Generated Roadmap", description=answer.track_url)
#         except Answer.DoesNotExist:
#             continue  # Skip to the next user answer
    
#     return None




# @login_required

# def dashboard(request):
#     """Dashboard view to display the roadmap."""
#     roadmap = generate_roadmap(request.user)  # This should work since we are passing user object
#     return render(request, 'roadmap/dashboard.html', {'roadmap': roadmap})


# from questionnaire.models import Question,Answer

# @login_required
# def flowchart_view(request):
#     """Flowchart-based question handling view."""
#     if request.method == 'GET':
#         # Initialize the first question
#         try:
#             question = Question.objects.get(questionid=1)  # Starting question ID
#         except Question.DoesNotExist:
#             return render(request, 'roadmap/roadmap_flowchart.html', {'message': 'No questions available.'})

#         return render(request, 'roadmap/roadmap_flowchart.html', {'question': question})

#     elif request.method == 'POST':
#         # Process user answer and fetch the next question or track
#         question_id = request.POST.get('question_id')
#         user_answer = request.POST.get('answer')

#         try:
#             question = Question.objects.get(questionid=question_id)
#         except Question.DoesNotExist:
#             return render(request, 'roadmap/roadmap_flowchart.html', {'message': 'Invalid question.'})

#         try:
#             answer = Answer.objects.get(question=question, answer_text=user_answer)
#         except Answer.DoesNotExist:
#             return render(request, 'roadmap/roadmap_flowchart.html', {'message': 'No track found for the given answer.'})

#         if answer.track_url:
#             return render(request, 'roadmap/roadmap_flowchart.html', {'track_url': answer.track_url})

#         if answer.next_question:
#             return render(request, 'roadmap/roadmap_flowchart.html', {'question': answer.next_question})

#         return render(request, 'roadmap/roadmap_flowchart.html', {'message': 'End of the roadmap.'})


# # roadmap/views.py
# from rest_framework import viewsets
# from .models import Roadmap
# from .serializers import RoadmapSerializer

# class RoadmapViewSet(viewsets.ModelViewSet):
#     queryset = Roadmap.objects.all()
#     serializer_class = RoadmapSerializer

# # class QuestionViewSet(viewsets.ModelViewSet):
# #     queryset = Questions.objects.all()
# #     serializer_class = QuestionSerializer

# # class AnswerViewSet(viewsets.ModelViewSet):
# #     queryset = Answer.objects.all()
# #     serializer_class = AnswerSerializer
