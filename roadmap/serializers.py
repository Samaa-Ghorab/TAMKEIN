# roadmap/serializers.py
from rest_framework import serializers
from .models import Roadmap

class RoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = '__all__'  # Include all fields from the model
        # Alternatively, you can specify fields explicitly:
        # fields = ['id', 'user', 'title', 'description', 'created_at', 'updated_at']

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Questions
#         fields = '__all__'
#         # Explicitly define fields if needed:
#         # fields = ['questionid', 'trackid', 'question', 'correct_answer', 'option_a', 'option_b', 'option_c', 'option_d']

# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = '__all__'
        # Explicitly define fields if needed:
        # fields = ['answerid', 'userid', 'questionid', 'answer', 'iscorrect', 'answeredat']
