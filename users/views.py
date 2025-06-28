from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm
from .models import CustomUser
from rest_framework import viewsets
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()
from .forms import CustomUserCreationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()  # حفظ المستخدم
            
            # استخراج قيمة disability_type من النموذج
            disability_type = form.cleaned_data.get('disability_type')
            
            if disability_type:
                user.disability_type = disability_type  # تخزين نوع الإعاقة
                user.save()  # حفظ التحديثات في قاعدة البيانات
            # استخراج قيمة interest من النموذج
            interest = form.cleaned_data.get('interest')
            
            if interest:
                user.interest = interest  # تخزين الاهتمام
                user.save()
            
            # استخراج قيمة interest من النموذج
            level = form.cleaned_data.get('level')
            
            if level:
                user.level = level  # تخزين الاهتمام
                user.save()

            messages.success(request, 'Your account has been created successfully! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error in your signup. Please try again.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/user_signup.html', {'form': form})





from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # تحقق من بيانات المستخدم
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # تسجيل الدخول للمستخدم
                return redirect('homepage')  # إعادة التوجيه إلى الصفحة الرئيسية باستخدام اسم الرابط
            else:
                messages.error(request, "wrong username or password")           
        else:
            messages.error(request, " Please enter correct username and password")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})




# Logout view
def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login page or any other page



def user_questions(request):
    return render(request, 'users/user_questions.html')  


# User API viewset (for REST framework)
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


from django.shortcuts import render

def dashboard_view(request):
    # Add any logic for the dashboard here (e.g., user data)
    return render(request, 'users/dashboard.html')  # The template for the dashboard


from django.http import JsonResponse
from .models import Track

def get_quiz_data(request):
    tracks = Track.objects.all()
    data = []
    for track in tracks:
        data.append({
            "name": track.name,
            "questions": [{"question_text": q.question_text} for q in track.questions.all()]
        })
    return JsonResponse(data, safe=False)
from django.http import JsonResponse
from .models import Track

def get_quiz_data(request):
    tracks = Track.objects.all()  # إحضار جميع الـ Tracks
    quiz_data = []
    
    for track in tracks:
        track_data = {
            'name': track.name,
            'questions': []
        }
        for question in track.questions.all():
            track_data['questions'].append({
                'id': question.id,
                'question_text': question.question_text
            })
        quiz_data.append(track_data)
    
    return JsonResponse(quiz_data, safe=False)

# views.py
from django.http import JsonResponse
# from questionnaire.models import Question

# def get_questions(request):
#     track_name = request.GET.get('track', None)
#     if track_name:
#         questions = Question.objects.filter(track__name=track_name)
#         data = [
#             {"id": question.id, "text": question.question}
#             for question in questions
#         ]
#         return JsonResponse(data, safe=False)
#     return JsonResponse({"error": "Track not provided"}, status=400)

# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer

class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

# users/views.py
from rest_framework.viewsets import ModelViewSet
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework import viewsets, permissions


class UserViewSet(ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


from django.http import JsonResponse
import json
# from questionnaire.models import Answer
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def submit_quiz(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             for item in data['answers']:
#                 Answer.objects.create(
#                     user=request.user,
#                     question_id=item['question_id'],
#                     answer=item['answer']
#                 )
#             return JsonResponse({"message": "Answers submitted successfully!"})
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     return JsonResponse({"error": "Invalid request"}, status=400)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from users.serializers import UserSerializer

class SignupView(APIView):
    permission_classes = [AllowAny]  # السماح للجميع بالوصول لهذه الـ API

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])  # تشفير كلمة المرور
            user.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from django.shortcuts import render, redirect

# def submit_form(request):
#     if request.method == 'POST':
#         # Handle form submission
#         disability_status = request.POST.get('disabilityStatus')
#         disability_type = request.POST.get('disabilityType')
#         # Add logic to process the form data
#         return redirect('login')  

#     return render(request, 'your_template.html')  # Render the page if the request is not POST

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import CustomUser
# from roadmap.models import UserRoadmaps
from courses.models import playlist, Courses

@csrf_exempt
def get_user_data(request, user_id):
    try:
        # Get user information
        user = CustomUser.objects.get(id=user_id)
        user_data = {
            "username": user.username,
            "birthdate": user.birthdate,
            "phone": user.phone,
            "email": user.email,
            "location": user.location,
        }

        # Get user's courses
        user_courses = Courses.objects.filter(user_id=user_id)
        courses_list = []
        total_sessions = 0
        
        for course in user_courses:
            print(course)
            courses_list.append({
                "course_id": course.id,
                "coursename": course.name,
                "sessionsNumber": course.sessionsnumber,
            })
            total_sessions += course.sessionsnumber

        # Number of courses
        total_courses = user_courses.count()

        # Get completed sessions from Playlist
        done_sessions = playlist.objects.filter(
            course_id__in=[c['course_id'] for c in courses_list],
            isDone=True
        ).count()

        # # Calculate completion percentage
        completion_percentage = (done_sessions / total_sessions) * 100 if total_sessions > 0 else 0

        return JsonResponse({
            "user_data": user_data,
            "courses": courses_list,
            "total_courses": total_courses,
            "total_sessions": total_sessions,
            "done_sessions": done_sessions,
            "completion_percentage": round(completion_percentage, 2)
        })

    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error::": str(e)}, status=500)





from django.http import JsonResponse
from QG.models import  Courses, QuizResult # Import your models

@csrf_exempt
def get_quiz_results(request, user_id):
    try:
        # Retrieve quiz results for the specific user
        quiz_results = QuizResult.objects.filter(user_id=user_id)

        # Prepare the response data
        result_data = []        

        for quiz in quiz_results:
            # Get the course name from the courses table using course_id
            course = Courses.objects.get(id=quiz.course_id)
            course_name = course.name  # Assuming the course name is in the 'name' column

            result_data.append({
                "course_name": course_name,  # The course name
                "score": quiz.score,  # The user's score in this quiz
            })

        return JsonResponse({
            "quiz_results": result_data
        })

    except QuizResult.DoesNotExist:
        return JsonResponse({"error": "Quiz results not found"}, status=404)
    except Courses.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
