# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # تأكد من استيراد النموذج المخصص إذا كنت تستخدمه

class CustomUserCreationForm(UserCreationForm):
    disability_type = forms.ChoiceField(
        choices=CustomUser.DISABILITY_CHOICES,
        required=False,  # اختيار الحقل كاختياري
        label="Disability Type",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    interest = forms.ChoiceField(
        choices=CustomUser.INTEREST_CHOICES,
        required=True,
        label="Interest",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    level = forms.ChoiceField(
        choices=CustomUser. LEVEL_CHOICES,
        required=True,
        label="level",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2','gender','first_name','last_name','birthdate','phone','photo','location', 'disability_type','interest','level')


