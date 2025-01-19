from django import forms
from .models import CustomUser

class RegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # Используйте вашу кастомную модель
        fields = ['username', 'password', 'email']
        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
        }