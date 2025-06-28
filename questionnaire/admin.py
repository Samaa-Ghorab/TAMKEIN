# from django.contrib import admin
# from .models import Question, UserAnswer

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('question_text',)

# @admin.register(UserAnswer)
# class UserAnswerAdmin(admin.ModelAdmin):
#     list_display = ('user', 'question', 'answer')
# from django.contrib import admin
# from .models import Question

# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('question', 'createdat', 'trackid', 'q_level', 'course_name')  # Display relevant fields
#     list_filter = ('q_level', 'trackid', 'course_name')  # Filters for easier navigation
#     search_fields = ('question', 'course_name')  # Search functionality for finding questions easily

# admin.site.register(Question, QuestionAdmin)
