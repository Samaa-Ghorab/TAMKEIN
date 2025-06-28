"""
Django settings for courses_website project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-nny1rv%&ba0-+mqk$_v4(7yjp=6o%jv8_cn+m$8%c7ln8$x@fm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # يفضل تغييره إلى False في بيئة الإنتاج

ALLOWED_HOSTS = ["*"]  # يسمح بكل النطاقات، لكن الأفضل تحديد النطاقات في بيئة الإنتاج

# Application definition
INSTALLED_APPS = [
    'chatbot',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'courses',
    'home',
    'users',
    'roadmap',
    'questionnaire',
    'recommendations',
    'QG',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': None,  # تعطيل الترقيم لعرض كل البيانات دفعة واحدة
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # يجب أن يكون أولًا في القائمة
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'courses_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # مسار ملفات HTML
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'courses_website.wsgi.application'

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default="postgresql://postgres:xSkhOQCGELvkHZOIAhTubFKBxbfpsssg@tramway.proxy.rlwy.net:25665/railway",
        conn_max_age=600,
        ssl_require=True  
    )
}

# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.getenv("DATABASE_URL"),
#         conn_max_age=600,
#         ssl_require=True  
#     )
# }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static and media files
STATICFILES_DIRS = [BASE_DIR / "static"]  
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS_ALLOW_ALL_ORIGINS = True  # يسمح للجميع
# CORS_ALLOW_CREDENTIALS = True  # السماح بإرسال الكوكيز والجلسات مع الطلبات
# CORS_ALLOW_HEADERS = ["*"]  # السماح بكل الرؤوس في الطلبات
# CORS_ALLOW_METHODS = ["*"]  # السماح بكل أنواع الطلبات (GET, POST, PUT, DELETE, ...)

# CSRF_TRUSTED_ORIGINS = [
#     "http://127.0.0.1:5500",
#     "http://localhost:8000",
#     "https://*.ngrok-free.app",  # ✅ السماح لكل روابط ngrok

# ]

# ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '.ngrok-free.app']




# CORS_ALLOWED_ORIGINS = [
#     "http://127.0.0.1:5501",  # ✅ السماح لصفحة الـ frontend
    
# ]
CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5501",
    "https://*.trycloudflare.com",  # السماح بطلبات CSRF من Cloudflare
    'https://tamkeen-ehdab2hpbye3dsh4.uaencrth-01.azurewebsites.net',
    'https://tamkeen-render-5.onrender.com',
]

# ALLOWED_HOSTS = [
#     ".trycloudflare.com",
#     "127.0.0.1",
#     "localhost"
# ]

CORS_ALLOW_ALL_ORIGINS = True  # 👈 هذا يسمح لجميع النطاقات (للتجربة فقط)
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [  # السماح بكل أنواع الطلبات
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
]

CORS_ALLOW_HEADERS = [  # السماح بجميع الهيدرز المطلوبة
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
]



# Login configuration
LOGIN_URL = '/users/login/'
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,  
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

AUTHENTICATION_BACKENDS = [
    'users.authentication.EmailBackend',  # غيري accounts باسم الـ app بتاعك
]
