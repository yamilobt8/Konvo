from django import forms
import re

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    
    
class RegisterForm(forms.Form):
    username = forms.CharField(label="Username", max_length=16, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entre your username', 'id':'is_username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email', 'id':'email_field'}))
    otp = forms.CharField(label="otp", max_length=6, required=False, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'verification code'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'confirm password'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

    def clean_password(self):
        password = self.cleaned_data['password']
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r'[@./!#$%^&*()_+=\-]', password):
            raise forms.ValidationError("Password must contain at least one special character (@, ., /, etc.).")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password
