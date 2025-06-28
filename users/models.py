from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    join_date = models.DateTimeField(default=datetime.now, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
            ('Prefer not to say', 'Prefer not to say')
        ],
        null=True,
        blank=True
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    profile_picture_url = models.URLField(max_length=2083, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    DISABILITY_CHOICES = [
        ('visual', 'Visual Impairment'),
        ('auditory', 'Auditory Impairment'),
        ('physical', 'Physical Impairment'),
        ('cognitive', 'Cognitive Impairment'),
        ('none', 'No Disability'),
    ]
    INTEREST_CHOICES = [
        ('AI', 'AI'),
        ('Web development', 'Web development'),
        ('Network', 'Network'),
        ('Mobile app development', 'Mobile app development'),
        ('Data Science', 'Data Science'),
        ('Data Engineering', 'Data Engineering'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Robotics', 'Robotics'),
    ]
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('Quiz','Take this quiz to determine your level!')
    ]

    disability_type = models.CharField(
        max_length=20,
        choices=DISABILITY_CHOICES,
        default='none',
    )
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES, default='AI')
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='beginner')

    class Meta:
        db_table = 'users_customuser'

    def __str__(self):
        return self.username



class DisabilityInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    disability_status = models.CharField(max_length=10)
    disability_type = models.CharField(max_length=100, null=True, blank=True)


class CSKnowledge(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cs_knowledge = models.CharField(max_length=10)
    cs_interest = models.CharField(max_length=100, null=True, blank=True)
    cs_level = models.CharField(max_length=50, null=True, blank=True)
    cs_suggestion = models.CharField(max_length=10, null=True, blank=True)
    trackid = models.PositiveIntegerField(default=0)

from django.db import models

class Track(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def _str_(self):
        return self.name
    class Meta:
        db_table = 'Tracks'

# class Question(models.Model):
#     track = models.ForeignKey(Track, related_name='questions', on_delete=models.CASCADE)
#     question_text = models.TextField()
#     answer = models.TextField(default="answer")  # Optional: Store correct answers

#     def _str_(self):
#         return self.question_text
#     class Meta:
#         db_table = 'questions'
