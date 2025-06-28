from rest_framework import serializers

class VideoProcessingSerializer(serializers.Serializer):
    video = serializers.FileField()
    number_of_images = serializers.IntegerField(default=2)
