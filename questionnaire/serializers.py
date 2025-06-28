# # from rest_framework import serializers
# # from .models import Question, Answer

# # class QuestionSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Question
# #         fields = ['questionid', 'trackid', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'course_name', 'q_level']

# # class AnswerSerializer(serializers.ModelSerializer):
# #     # Using the related questionid field as a nested serializer
# #     questionid = serializers.PrimaryKeyRelatedField(queryset=Question.objects.all(), source='question')

# #     class Meta:
# #         model = Answer
# #         fields = ['userid', 'questionid', 'answer', 'is_correct']
# from rest_framework import serializers
# from .models import Question, Answer

# # class QuestionSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Question
# #         fields = ['questionid', 'trackid', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'course_name', 'q_level']

# # class AnswerSerializer(serializers.ModelSerializer):
# #     questionid = serializers.PrimaryKeyRelatedField(
# #         queryset=Question.objects.all(), 
# #         source='question'
# #     )
# #     is_correct = serializers.BooleanField(read_only=True)  # Make 'is_correct' read-only

# #     class Meta:
# #         model = Answer
# #         fields = ['user', 'questionid', 'answer', 'is_correct']  # Changed 'answer_text' to 'answer'

# #     def validate(self, data):
# #         """
# #         Validate the answer by comparing it with the correct answer for the question.
# #         """
# #         question = data['question']
# #         if data['answer'].lower() != question.correct_answer.lower():  # Changed 'answer_text' to 'answer'
# #             data['is_correct'] = False
# #         else:
# #             data['is_correct'] = True
# #         return data