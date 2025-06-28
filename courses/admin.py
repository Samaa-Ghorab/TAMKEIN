from django.contrib import admin
from .models import playlist

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'duration', 'difficultylevel', 'course', 'created_at')  # إضافة created_at لعرضه في القائمة
    list_filter = ('difficultylevel', 'course')  # فلاتر لتصفية البيانات بناءً على مستوى الصعوبة أو الكورس
    search_fields = ('name', 'description')  # تمكين البحث بناءً على الاسم والوصف
    ordering = ('-rating',)  # ترتيب البيانات حسب التقييم بشكل تنازلي
    #date_hierarchy = 'created_at'  # تسلسل هرمي حسب تاريخ الإنشاء

# تسجيل الـ model في لوحة الإدارة
admin.site.register(playlist, PlaylistAdmin)
