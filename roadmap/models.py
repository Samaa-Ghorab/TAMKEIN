from django.db import models
from django.conf import settings
from users.models import CustomUser

# class Roadmap(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     title = models.CharField(max_length=100)
#     description = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

# from django.db import models
# from django.utils.timezone import now
# class Questions(models.Model):
#     questionid = models.AutoField(primary_key=True,default=1)  # العمود الرئيسي
#     trackid = models.IntegerField(null=True, blank=True)  # يمكن أن يكون فارغًا
#     question = models.TextField(default="Default Question Text")
#     correct_answer = models.TextField(null=True, blank=True)  # الإجابة الصحيحة
#     explanation = models.TextField(null=True, blank=True)  # الشرح
#     createdat = models.DateTimeField(default=now)
#     option_a = models.TextField(null=True, blank=True)  # الخيار أ
#     option_b = models.TextField(null=True, blank=True)  # الخيار ب
#     option_c = models.TextField(null=True, blank=True)  # الخيار ج
#     option_d = models.TextField(null=True, blank=True)  # الخيار د
#     next_question_id = models.IntegerField(null=True, blank=True)  # ID السؤال التالي
#     course_name = models.TextField(null=True, blank=True)  # اسم الكورس
#     q_level = models.TextField(null=True, blank=True)  # مستوى السؤال
#     track_id = models.IntegerField(null=True, blank=True)  # ID المسار

    # class Meta:
    #     db_table = 'questions'  # اسم الجدول في قاعدة البيانات

    # def __str__(self):
    #     return self.question


# from users.models import CustomUser
# from django.db import models
# from questionnaire.models import Question

# class Answer(models.Model):
#     userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ربط بالإجابة بالمستخدم
#     questionid = models.ForeignKey(Question, on_delete=models.CASCADE)  # ربط الإجابة بالسؤال
#     answer = models.TextField()
#     iscorrect = models.BooleanField(default=False)
#     answeredat = models.DateTimeField(auto_now_add=True)
#     answerid = models.AutoField(primary_key=True)

#     def __str__(self):
#         return f"Answer for question {self.question.id}: {self.answer}"

#     class Meta:
#         db_table = 'useranswers'  # اسم الجدول في قاعدة البيانات


from django.db import models
from django.contrib.auth.models import User  # Assuming you're using Django's built-in User model
from courses.models import Courses  # Assuming you have a 'Courses' model

from django.db import models
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
import uuid

class UserRoadmaps(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)  # Use AUTH_USER_MODEL
    track = models.CharField(max_length=100, null=True)  # Track name or ID
    course = models.IntegerField()  # Assuming you have a 'Courses' model
    coursename = models.CharField(max_length=255, null=True)
    itsOrder = models.PositiveIntegerField(default=0)
    roadmap_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    course_url = models.URLField(null=True, blank=True)
    def __str__(self):
        return f"Course {self.course.title} in Roadmap {self.user_roadmap.id}, Order: {self.order}"


# Model for storing user's questionnaire answers
class User_Ques_Answers(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    difficulty_level = models.CharField(max_length=50)
    track = models.CharField(max_length=100)
    custom_answer = models.TextField()
    roadmap_id = models.UUIDField(null=True, blank=True, db_index=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Questionnaire Answer {self.user.username} - {self.difficulty_level} - {self.track}"