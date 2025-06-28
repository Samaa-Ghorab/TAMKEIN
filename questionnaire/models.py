# # models.py
from django.db import models
from users.models import CustomUser

# class Question(models.Model):
#     questionid = models.AutoField(primary_key=True)
#     trackid = models.IntegerField(null=True, blank=True)
#     question = models.TextField()
#     correct_answer = models.TextField(null=True, blank=True)
#     explanation = models.TextField(null=True, blank=True)
#     createdat = models.DateTimeField(auto_now_add=True)
#     option_a = models.TextField(null=True, blank=True)
#     option_b = models.TextField(null=True, blank=True)
#     option_c = models.TextField(null=True, blank=True)
#     option_d = models.TextField(null=True, blank=True)
#     next_question_id = models.IntegerField(null=True, blank=True)
#     course_name = models.TextField(null=True, blank=True)
#     q_level = models.TextField(null=True, blank=True)

#     class Meta:
#         db_table = 'questions'  # Set the table name for the database

# #     def __str__(self):
# #         return self.question
# from django.db import models
# from django.contrib.auth import get_user_model

# CustomUser = get_user_model()

# class Answer(models.Model):
#     answerid = models.AutoField(primary_key=True)  # AutoField for primary key
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user')  
#     question = models.ForeignKey('Question', on_delete=models.CASCADE, db_column='questionid')  
#     answer = models.TextField(db_column='answer')  # Changed field name to 'answer' to match DB schema
#     is_correct = models.BooleanField(default=False, db_column='iscorrect')  
#     answered_at = models.DateTimeField(auto_now_add=True, db_column='answeredat')  

#     class Meta:
#         db_table = 'useranswers'  # Ensure table name matches the DB schema

#     def __str__(self):
#         return f"Answer for {self.question} by {self.user}"  # Corrected user reference
    
#    # from django.db import models

# class QuizAnswer(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # ربط الإجابة بالمستخدم
#     question_id = models.IntegerField()  # لتخزين معرف السؤال
#     selected_answer = models.CharField(max_length=1)  # لتخزين الإجابة المختارة (A, B, C, D)
#     created_at = models.DateTimeField(auto_now_add=True)  # تاريخ ووقت الإجابة

#     def __str__(self):
#         return f"Answer for Question {self.question_id} by {self.user.username}"
# from django.db import models

# class Question(models.Model):
#     question = models.TextField()
#     option_a = models.CharField(max_length=255)
#     option_b = models.CharField(max_length=255)
#     option_c = models.CharField(max_length=255)
#     option_d = models.CharField(max_length=255)
#     correct_answer = models.CharField(max_length=1)

#     class Meta:
#       db_table = 'questions'


# class UserAnswer(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     selected_answer = models.CharField(max_length=1)
#     submitted_at = models.DateTimeField(auto_now_add=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


#     class Meta:
#         db_table = 'useranswers'
#     def __str__(self):
#         return f"Answer for {self.question} by {self.submitted_at}"


# class Answer(models.Model):
#     answerid = models.AutoField(primary_key=True)  # المفتاح الأساسي
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     answer = models.TextField(default="")  # الافتراضي: نص فارغ
#     iscorrect = models.BooleanField(default=False)  # الافتراضي: غير صحيح
#     answeredat = models.DateTimeField(auto_now_add=True)  # تاريخ الإجابة يتم تعيينه تلقائيًا

#     class Meta:
#         db_table = "useranswers"
