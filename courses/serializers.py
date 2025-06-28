from rest_framework import serializers
from .models import playlist

# class AnswerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Answer
#         fields = ['user', 'course', 'question', 'answer', 'disability_type']

class PlaylistSerializer(serializers.ModelSerializer):
    # answers = AnswerSerializer(many=True, read_only=True)  # Nested answers for the playlist

    class Meta:
        model = playlist
        fields = [
            'video_id',
            'name',
            'description',
            'url',
            'rating',
            'duration',
            'difficultylevel',
            'track_id',
            
            
        ]

# class TrackSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Tracks
#         fields = ['id', 'name', 'description']

# from rest_framework import serializers
# from .models import Courses

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Courses
#         fields = ['id', 'name', 'description', 'track', 'level', 'quiz_score', 'rating', 'created_at']
