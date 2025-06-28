import torch
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModel
from courses.models import playlist  # adjust if your app name is different

# Set device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
MODEL_NAME = "Lolity/results"
HF_TOKEN = "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"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN)
    model = AutoModel.from_pretrained(MODEL_NAME, use_auth_token=HF_TOKEN).to(device)
    print("Custom model and tokenizer loaded successfully.")
except Exception as e:
    raise RuntimeError(f"Error loading model: {str(e)}")

# Load data from the playlist table
try:
    qs = playlist.objects.all().values(
        'video_id', 'name', 'description', 'url', 'difficultylevel', 'track'
    )
    df = pd.DataFrame.from_records(qs)
    print("Playlist data loaded from database successfully.")
except Exception as e:
    raise RuntimeError(f"Error loading playlist data: {str(e)}")

# Preprocessing
df["track"] = df["track"].str.strip().str.lower()
df_exploded = df.assign(track=df["track"].str.split(" / ")).explode("track")
df_exploded["track"] = df_exploded["track"].str.strip().str.lower()

# Function to generate embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state[:, 0, :].cpu().numpy()

# Function to recommend courses based on similarity
def recommend_courses(track, difficulty_level, user_description):
    target_track = track.strip().lower()
    target_level = difficulty_level.strip().lower()
    user_description = user_description.strip()

    # Filter courses
    filtered_courses = df_exploded[
        (df_exploded["track"] == target_track) &
        (df_exploded["difficultylevel"].str.strip().str.lower() == target_level)
    ]

    if filtered_courses.empty:
        return {"message": "No courses found for the given criteria."}

    # Compute embeddings
    user_embedding = get_embedding(user_description)
    course_descriptions = filtered_courses["description"].tolist()
    course_embeddings = np.vstack([get_embedding(desc) for desc in course_descriptions])

    # Compute cosine similarity
    similarity_scores = cosine_similarity(user_embedding, course_embeddings)[0]

    # Combine results
    course_scores = list(zip(
        filtered_courses["name"],
        filtered_courses["url"],
        filtered_courses["video_id"],
        similarity_scores
    ))

    # Sort and get top 5
    sorted_courses = sorted(course_scores, key=lambda x: x[3], reverse=True)
    top_courses = [
        {"name": name, "url": url, "id": course_id}
        for name, url, course_id, _ in sorted_courses[:5]
    ]

    return {
        "track": track,
        "difficulty_level": difficulty_level,
        "top_courses": top_courses
    }

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from roadmap.models import UserRoadmaps, User_Ques_Answers
from users.models import CustomUser
from courses.models import playlist
from users.serializers import UserSerializer
import uuid
# from .recommendation_logic import recommend_courses  # assuming you have this

class RecommendView(APIView):
    def get(self, request):
        try:
            # Step 1: Retrieve query parameters
            user_id = request.GET.get("user_id", "").strip()
            track = request.GET.get("track", "").strip().lower()
            difficulty_level = request.GET.get("difficulty_level", "").strip().lower()
            user_description = request.GET.get("user_description", "").strip()

            # Step 2: Validate input
            if not user_id:
                return Response({"error": "Missing user ID"}, status=status.HTTP_400_BAD_REQUEST)
            if not track:
                return Response({"error": "Missing track"}, status=status.HTTP_400_BAD_REQUEST)
            if not difficulty_level:
                return Response({"error": "Missing difficulty level"}, status=status.HTTP_400_BAD_REQUEST)
            if not user_description:
                return Response({"error": "Missing user description"}, status=status.HTTP_400_BAD_REQUEST)

            # Step 3: Get user instance
            user = get_object_or_404(CustomUser, id=user_id)

            # Step 4: Get course recommendations
            recommendations = recommend_courses(track, difficulty_level, user_description)
            top_courses = recommendations.get("top_courses", [])

            # Step 5: Generate shared roadmap_id
            roadmap_id = uuid.uuid4()

            # Step 6: Save each recommended course to UserRoadmaps
            for idx, course_data in enumerate(top_courses):
                courseId = course_data.get("id")
                course_name = course_data.get("name")
                
                try:
                    course_instance = playlist.objects.get(video_id=courseId)
                except playlist.DoesNotExist:
                    print(f"Course with ID {courseId} does not exist. Skipping.")
                    continue

                UserRoadmaps.objects.get_or_create(
                    user=user,
                    track=track,
                    course=course_instance.video_id,
                    roadmap_id=roadmap_id,
                    defaults={
                        "coursename": course_name,
                        "itsOrder": idx,
                        "course_url": course_data.get("url")
                    }
                )

            # Step 7: Save the questionnaire answer linked with this roadmap
            User_Ques_Answers.objects.create(
                user=user,
                difficulty_level=difficulty_level,
                track=track,
                custom_answer=user_description,
                roadmap_id=roadmap_id  # ✅ linking the same roadmap group
            )

            # Step 8: Return response
            return Response({
                "user_id": user_id,
                "user": UserSerializer(user).data,
                "roadmap_id": str(roadmap_id),
                "recommendations": recommendations
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print("Error:", str(e))
            return Response({"error": f"Server Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        # questions/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from users.models import CustomUser
# from questions.models import User_Ques_Answers

class UserRoadmapListView(APIView):
    def get(self, request):
        user_id = request.GET.get("user_id", "").strip()
        
        if not user_id:
            return Response({"error": "Missing user_id parameter"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CustomUser, id=user_id)

        # Collect distinct roadmap IDs linked to the user's questionnaire answers
        qs = User_Ques_Answers.objects.filter(user=user).values_list("roadmap_id", flat=True).distinct()
        # Filter out any nulls
        roadmap_ids = [str(rid) for rid in qs if rid is not None]

        return Response({
            "user_id": user_id,
            "roadmap_ids": roadmap_ids
        }, status=status.HTTP_200_OK)


class RoadmapCoursesView(APIView):
    def get(self, request):
        roadmap_id_str = request.GET.get("roadmap_id", "").strip()

        if not roadmap_id_str:
            return Response({"error": "Missing roadmap_id parameter"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            roadmap_id = uuid.UUID(roadmap_id_str)
        except ValueError:
            return Response({"error": "Invalid UUID format for roadmap_id"}, status=status.HTTP_400_BAD_REQUEST)

        roadmap_courses = UserRoadmaps.objects.filter(roadmap_id=roadmap_id).order_by("itsOrder")

        if not roadmap_courses.exists():
            return Response({"error": "No courses found for this roadmap_id"}, status=status.HTTP_404_NOT_FOUND)

        course_list = []
        for roadmap_course in roadmap_courses:
            try:
                course_obj = playlist.objects.get(video_id=roadmap_course.course)
                course_list.append({
                    "coursename": roadmap_course.coursename,
                    "course_id": roadmap_course.course,
                    "course_url": roadmap_course.course_url,
                    "itsOrder": roadmap_course.itsOrder
                })
            except playlist.DoesNotExist:
                continue

        return Response({
            "roadmap_id": str(roadmap_id),
            "courses": course_list
        }, status=status.HTTP_200_OK)