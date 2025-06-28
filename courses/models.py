from django.conf import settings
from django.db import models
from django.utils import timezone


# class Tracks(models.Model):
#     track_id = models.AutoField(primary_key=True,default=0)
#     name = models.CharField(max_length=255)

#     class Meta:
#         db_table = 'tracks'



from django.db import models
from django.conf import settings
from users.models import CustomUser

# **THE COURSE**

class Courses(models.Model):
    name = models.CharField(max_length=255, null = True)  # Keep original DB column 'name'
    description = models.TextField()         # Course description
    instructor_id = models.IntegerField(null=True, blank=True)  # Allow NULL
    track = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)  # Rating
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )  
    sessionsnumber = models.IntegerField(
        null=True,
        blank=True,
        default=0,
        help_text="Number of sessions in this course"
    )

    updated_at = models.DateTimeField(auto_now=True)      # Auto timestamp on update

    class Meta:
        db_table = 'courses'

    def __str__(self):
        return f"{self.name}"



# from courses.models import Courses
# SESSIONS OF COURSE
class playlist(models.Model):
    video_id = models.IntegerField(primary_key=True, default=1)
    name = models.CharField(max_length=255, null=True, blank=True)  # Keep original DB column 'name'
    description = models.TextField()
    url = models.URLField(default="http://example.com")
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    duration = models.DurationField(default='1:00:00')
    difficultylevel = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced')],
        default='Beginner'
    )
    course = models.ForeignKey(Courses, related_name='playlists', on_delete=models.CASCADE, null=True)
    track = models.CharField(max_length=255)

    sessionOrder = models.PositiveIntegerField(default=0)
    
    isDone = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'playlist'

    def __str__(self):
        return self.name




# class Answer(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # استخدام AUTH_USER_MODEL بدلاً من auth.User
#     course = models.ForeignKey(playlist, related_name='answers', on_delete=models.CASCADE)  # ربط الإجابة بالفيديو
#     question = models.CharField(max_length=255)  # السؤال الذي تم الإجابة عليه
#     answer = models.CharField(max_length=255)  # الإجابة على السؤال
#     disability_type = models.CharField(max_length=100, blank=True, null=True)  # نوع الإعاقة

#     class Meta:
#         db_table = 'useranswers'  

#     def __str__(self):
#         return f"{self.user.username} - {self.course.name} - {self.question}"


# class Result(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # ForeignKey to User
#     course = models.ForeignKey(Courses, on_delete=models.CASCADE)  # ForeignKey to Course
#     track = models.ForeignKey(Tracks, on_delete=models.CASCADE)  # ForeignKey to Track
#     score = models.IntegerField()  # The score the user achieved
#     quiz_date = models.DateTimeField(auto_now_add=True)  # Date when the quiz was taken

#     class Meta:
#         db_table = 'result'  # Name of the table in the database

#     def __str__(self):
#         return f"Result for {self.user.username} in {self.course.name} - {self.track.name}"
