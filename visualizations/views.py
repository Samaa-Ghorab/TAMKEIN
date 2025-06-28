from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .serializers import VideoProcessingSerializer
from .video_processor import main
import os
import uuid

class ProcessVideoView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = VideoProcessingSerializer(data=request.data)
        if serializer.is_valid():
            video_file = serializer.validated_data['video']
            number_of_images = serializer.validated_data.get('number_of_images', 2)

            # Save the uploaded video temporarily
            video_name = f"{uuid.uuid4()}.mp4"
            video_path = os.path.join("media/temp_videos", video_name)
            os.makedirs(os.path.dirname(video_path), exist_ok=True)

            with open(video_path, 'wb+') as f:
                for chunk in video_file.chunks():
                    f.write(chunk)

            try:
                final_video, _ = main(video_path, number_of_images)
                output_path = video_path.replace(".mp4", "_final.mp4")
                final_video.write_videofile(output_path, codec='libx264', audio_codec='aac')

                return Response({
                    "status": "success",
                    "video_url": f"/media/temp_videos/{os.path.basename(output_path)}"
                })

            except Exception as e:
                return Response({"error": str(e)}, status=500)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
