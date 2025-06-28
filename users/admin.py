from django.contrib import admin
from .models import CustomUser  # Import your custom user model

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('email', 'username', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_active')
    
    # Fields that can be searched
    search_fields = ('email', 'username', 'first_name', 'last_name')
    
    # Filters to make it easier to filter by specific conditions
    list_filter = ('is_staff', 'is_active', 'gender')

    # Fields to allow inline editing directly from the list view
    list_editable = ('is_active',)

    # Optionally, you can configure the ordering of users in the list view
    ordering = ('date_joined',)

    # You can also specify how to display the user’s full name (if desired)
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'

# from django.contrib import admin
# from .models import Track

# @admin.register(Track)
# class TrackAdmin(admin.ModelAdmin):
#     list_display = ('name',)

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ('question_text', 'track')
