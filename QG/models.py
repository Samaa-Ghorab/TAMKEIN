from django.db import models
from courses.models import playlist  # Assuming you have a 'Courses' model

class MCQQuestion(models.Model):
    document_index = models.CharField(max_length=50, default="Unknown Course")  # Lec1, Lec2, etc.
    course_name = models.CharField(max_length=255)  # Course name
    course_id = models.IntegerField(null=True, blank=True)  # <-- New field added
    document_name = models.CharField(max_length=255)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.document_index} - {self.question_text}"

    
from django.db import models
from courses.models import Courses  # لو عندك جدول Course

# class Session(models.Model):
#     course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='sessions')
#     title = models.CharField(max_length=200)
#     video_url = models.URLField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} - {self.course}"

from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Courses

User = get_user_model()

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


from django.db import models

class QuizResult(models.Model):
    user = models.IntegerField(null=True)
    quiz = models.IntegerField(null=True)
    session = models.CharField(max_length=50, default="Unknown Course")
    course = models.IntegerField(null=True)
    score = models.FloatField()

    class Meta:
        unique_together = ('user', 'quiz', 'session')

    def __str__(self):
        return f"User {self.user} - Quiz {self.quiz} - {self.session} => {self.score}"


class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(playlist, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'session')

    def __str__(self):
        return f"{self.user.username} - Session {self.session.id} - {'✅' if self.completed else '❌'}"


# (اختياري) لو عايزين نتابع كل إجابة
class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(MCQQuestion, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.question.id} - {'✅' if self.is_correct else '❌'}"