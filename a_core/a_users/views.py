import json
import os
import shutil


from django.utils import timezone
import re
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RegisterForm, LoginForm, ChangeUsername, ChangePassword
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from a_users.models import Profile, PasswordHistory
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
import os

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

def send_email(request, recipient_email, subject, message):
    send_mail(
        subject=subject,
        message=message,
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
            password_record = PasswordHistory.objects.create(user=user, old_password=make_password(password))
            password_record.save()
            login(request, user)
            send_email(request, email, subject=f'thank you for registering on our site {username}', message='Welcome To our site')
            return JsonResponse({'message': 'User registered successfully'})

    form = RegisterForm()
    return render(request, 'a_users/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url="/users/login")
def profile(request):
    return render(request, 'a_users/profile.html')

@login_required(login_url="/users/login")
def personal_info(request):
    user = request.user
    if request.method == 'POST':
        if 'username' in request.POST:
            username_form = ChangeUsername(request.POST, initial={'username': request.user.username})
            if username_form.is_valid():
                new_username = username_form.cleaned_data.get('username')
                if new_username != user.username:
                    user.username = new_username
                    user.save()
                return redirect('profile')
    username_form = ChangeUsername(initial={'username': request.user.username})
    return render(request, 'a_users/personal_info.html', {'user': user, 'username_form':username_form})

@login_required(login_url="/users/login")
def security(request):
    user = request.user
    password_records = PasswordHistory.objects.get(user=user)
    print(password_records.password_changed)
    if password_records.password_changed:
        print(password_records.password_changed)
        now = timezone.now()
        end = password_records.changed_at
        last_time = timesince(end, now).replace(',', ' and')
    else:
        last_time = timesince(user.date_joined).replace(',', ' and')
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        old_password = data.get('old_password', '').strip()
        new_password = data.get('new_password', '').strip()
        if check_password(old_password, user.password):
            password_records.old_password = make_password(old_password)
            password_records.new_password = make_password(new_password)
            password_records.password_changed = True
            password_records.save()

            user.set_password(new_password)
            user.save()
            send_email(request, recipient_email=user.email, subject='Security Alert', message=f'{user.username} Your Password has been changed.')
            return JsonResponse({'message': 'Password changed successfully'})
        else:
            return JsonResponse({'message': 'Incorrect old password'})
    password_form = ChangePassword(request.POST)
    return render(request, 'a_users/security.html', {'user': user, 'password_form': password_form, 'last_time': last_time})




def profile_picture(user, username):
    src_path = os.path.join(settings.BASE_DIR, 'a_users', 'static', 'a_users', 'images', 'default.jpeg')
    dest_dir = os.path.join(settings.MEDIA_ROOT, 'profile_pics')
    os.makedirs(dest_dir, exist_ok=True)
    dest_path = os.path.join(dest_dir, f'{username}_pfp.png')
    shutil.copy(src_path, dest_path)
    Profile.objects.create(
        user=user,
        profile_picture=f'profile_pics/{username}_default.png'
    )

@csrf_exempt
def change_pfp(request):
    if request.method == 'POST':
        if 'profile_picture' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        image = request.FILES['profile_picture']
        try:
            profile_status = Profile.objects.get(user=request.user)
            if profile_status.profile_picture:
                profile_status.profile_picture.delete(save=False)
                profile_status.times_changed += 1
                image.name = f'{request.user.username}_pfp_{profile_status.times_changed}.png'
            profile_status.profile_picture = image
            profile_status.save()
        except Profile.DoesNotExist:
            times_changed = 1
            image.name = f'{request.user.username}_pfp_{times_changed}.png'
            Profile.objects.create(user=request.user, profile_picture=image, times_changed=times_changed)


        return JsonResponse({'message': 'Image Uploaded Successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)