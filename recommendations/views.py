from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import os

# تحديد مسار الملف
data_path = "recommendations/Courses_Data.csv"

# التحقق من وجود الملف
if not os.path.exists(data_path):
    raise FileNotFoundError(f"❌ الملف غير موجود: {data_path}")

# تحميل البيانات
try:
    df = pd.read_csv(data_path)
    print("✅ تم تحميل الملف بنجاح!")
except Exception as e:
    raise ValueError(f"⚠️ خطأ أثناء تحميل الملف: {e}")

# التحقق من الأعمدة المطلوبة
required_columns = ["Course Name", "Course URL"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    raise ValueError(f"🚨 الملف يجب أن يحتوي على الأعمدة التالية: {missing_columns}")

# تجهيز البيانات
df["Course Name"] = df["Course Name"].str.lower().str.strip()

# استخراج الميزات باستخدام TF-IDF
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(df["Course Name"])

# حساب مصفوفة التشابه
similarity = cosine_similarity(tfidf_matrix)

@api_view(["GET"])
def recommend_course(request):
    """
    إرجاع قائمة بالدورات المشابهة لدورة معينة بناءً على اسم الدورة المدخل.
    """
    course = request.GET.get("course", "").lower().strip()  # الحصول على اسم الدورة من المعامل

    if not course:
        return Response({"error": "⚠️ لا يمكن أن يكون اسم الدورة فارغًا!"}, status=status.HTTP_400_BAD_REQUEST)

    # البحث عن الدورة في قاعدة البيانات
    course_index = df[df["Course Name"] == course].index
    if course_index.empty:
        return Response({"error": f"❌ الدورة '{course}' غير موجودة في قاعدة البيانات!"}, status=status.HTTP_404_NOT_FOUND)

    # الحصول على الدورات المشابهة
    course_index = course_index[0]
    distances = similarity[course_index]
    course_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]  # استثناء الدورة الأصلية

    # إنشاء قائمة التوصيات
    recommendations = [
        {"Course Name": df.iloc[i[0]]["Course Name"], "Course URL": df.iloc[i[0]]["Course URL"]}
        for i in course_list
    ]

    return Response(recommendations)
