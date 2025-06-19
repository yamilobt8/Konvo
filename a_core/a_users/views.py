import json
from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == 'POST':
        print(request.body)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'Invalid username or password'})

    form = LoginForm()
    return render(request, 'a_users/login.html', {'form': form})

def send_email(request, recipient_email, subject):
    send_mail(
        subject=subject,
        message='Thank you for registering at MySite',
        from_email='bouloujouramin.82@gmail.com',
        recipient_list=[recipient_email],
        fail_silently=False,
    )
def send_otp(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        email  = data.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            form.add_error('email', 'Enter a valid email address.')
            return JsonResponse({'message': 'Email already registered'})
        else:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            send_email(request, email, otp)
            print(f"Sending OTP {otp} to {email}")
            return JsonResponse({'message': 'OTP sent Successfully'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
def verify_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        otp = request.session['otp']
        user_otp = data.get('otp', '').strip()
        if user_otp == otp:
            request.session['otp_verified'] = True
            return JsonResponse({'message': 'OTP verified'})
        return JsonResponse({'message': 'Invalid OTP'})
    return JsonResponse({'error': 'Invalid request method.'}, status=405)
def register_user(request):
    if request.method == 'POST':
        print(request.body)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        username = data.get('username', '').strip()
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already registered'})
        else:
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            send_email(request, email, f'thank you for registering on our site {username}')
            return JsonResponse({'message': 'User registered successfully'})

    form = RegisterForm()
    return render(request, 'a_users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')