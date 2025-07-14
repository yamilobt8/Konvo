import json
import os
import shutil

import logging
from django.utils import timezone
import re
from django.conf import settings
from django.shortcuts import render, redirect
#from django.views.decorators.csrf import csrf_exempt
from PIL import Image as PilImage
from io import BytesIO
from .forms import RegisterForm, LoginForm, ChangeUsername, ChangePassword
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django_ratelimit.core import is_ratelimited
from django.contrib.auth import authenticate, login, logout
from a_users.models import Profile, PasswordHistory
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.utils.timesince import timesince
import os
from a_users.tasks import send_email
import requests
from django.core.cache import cache
from django.contrib import messages
from time import sleep

logger = logging.getLogger(__name__)

@ratelimit(key='ip', rate='10/m', method='POST', block=False)
def login_view(request):
    limited = getattr(request, 'limited', False)

    if request.method == 'POST':
        form = LoginForm(request.POST)
        recaptcha_token = request.POST.get('g-recaptcha-response')
        if not recaptcha_token:
            form.add_error(None, "reCAPTCHA token missing. Please try again.")
            return render(request, 'a_users/login.html', {'form': form})

        if limited:
            form.add_error(None, "Too many login attempts. Please wait a minute and try again.")
            return render(request, 'a_users/login.html', {'form': form})

        try:
            recaptcha_response = requests.post(
                'https://www.google.com/recaptcha/api/siteverify',
                data={
                    'secret': settings.RECAPTCHA_PRIVATE_KEY,
                    'response': recaptcha_token,
                    'remoteip': request.META.get('REMOTE_ADDR')
                },
                timeout=5
            )
            recaptcha_response.raise_for_status()
            result = recaptcha_response.json()
            print(result)
            success = result.get('success', False)
            score = result.get('score', 0.0)
            action = result.get('action', '')
            if not (success and score > 0.5 and action == 'login'):
                logger.warning(f"reCAPTCHA verification failed: {result}")
                form.add_error(None, "reCAPTCHA verification failed. Please try again.")
                return render(request, 'a_users/login.html', {'form': form})

        except requests.RequestException as e:
            logger.error(f"reCAPTCHA API error: {str(e)}")
            form.add_error(None, "Error verifying reCAPTCHA. Please try again later.")
            return render(request, 'a_users/login.html', {'form': form})

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                logger.info(f"User {username} logged in successfully")
                return redirect('home')
            else:
                form.add_error(None, "Invalid username or password")
        else:
            logger.warning(f"Form validation failed: {form.errors}")
            form.add_error(None, "Please Verify the username and password fields")
    else:

        form = LoginForm()
    return render(request, 'a_users/login.html', {'form': form})

def send_otp(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        email  = data.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already registered'})
        else:
            otp = str(random.randint(100000, 999999))
            request.session['otp'] = otp
            send_email.delay(email, 'Your Verification Code' ,otp)
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
        if not request.session['otp_verified']:
            return JsonResponse({'message': 'Error Please Try Again'})
        else:
            email = data.get('email', '').strip()
            password = data.get('password', '').strip()
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            password_record = PasswordHistory.objects.create(user=user, old_password=make_password(password))
            password_record.save()
            login(request, user)
            send_email.delay(email, subject=f'thank you for registering on our site {username}', message='Welcome To our site')
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
    print("function called")
    limited = getattr(request, 'limited', False)
    print(f'limited: {limited}')
    user = request.user
    if request.method == 'POST':
        print(request.POST)
        username_form = ChangeUsername(request.POST, initial={'username': user.username})
        print(f'errors: {username_form.errors}')
        if username_form.is_valid():
            print('valid')
            new_username = username_form.cleaned_data.get('username')
            print(new_username)
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                username_form.add_error(None, "Username already exists")
            elif user.username == new_username:
                username_form.add_error(None, "No changes made; the submitted username is the same.")
            else:
                if is_ratelimited(request, key='user', group='change-username', rate='1/7d', method='POST', increment=True):
                    username_form.add_error(None, "You can only change your username once a week. Try again later.")
                else:
                    user.username = new_username
                    user.save()
                    logger.debug("Username changed")
                    print('username changed')
                    messages.success(request, "Username Changed Successfully")
        else:
            username_form.add_error(None, "An error occurred please try again")

    else:
        username_form = ChangeUsername(initial={'username': user.username})
    return render(request, 'a_users/personal_info.html', {'user': user, 'username_form':username_form})

@login_required(login_url="/users/login")
def security(request):
    user = request.user
    password_records = PasswordHistory.objects.get(user=user)
    if password_records.password_changed:
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
            send_email.delay(recipient_email=user.email, subject='Security Alert', message=f'{user.username} Your Password has been changed.')
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


@login_required(login_url="/users/login")
@ratelimit(key='user', rate='1/d', method='POST', block=False)
def change_pfp(request):
    if request.method == 'POST':
        limited = getattr(request, 'limited', False)
        if limited:
            return JsonResponse({'error': 'You can only change your profile picture once per day. Try again later'},status=429)

        image = request.FILES.get('profile_picture')
        if not image:
            return JsonResponse({'error': 'No file uploaded'}, status=400)

        if image.size > 2 * 1024 * 1024:
            return JsonResponse({'error': 'File too large (max 2MB)'}, status=400)

        if image.content_type not in ['image/png', 'image/jpeg']:
            print(image.content_type)
            return JsonResponse({'error': 'Unsupported image type'}, status=400)

        try:
            img = PilImage.open(BytesIO(image.read()))
            img.verify()
            image.seek(0)
        except Exception:
            return JsonResponse({'error': 'Invalid image file content'}, status=400)

        valid_image = os.path.splitext(image.name)[1].lower() in ['.png', '.jpeg', '.jpg']
        if not valid_image:
            return JsonResponse({'error': 'Invalid image'}, status=400)
        else:
            try:
                profile_status = Profile.objects.get(user=request.user)
                if profile_status.profile_picture:
                    profile_status.profile_picture.delete(save=False)
                    profile_status.times_changed += 1
                    image.name = f'{request.user.username}_pfp_{profile_status.times_changed}.png'
                profile_status.profile_picture = image
                profile_status.save()
                send_email.delay(recipient_email=request.user.email, subject='Profile Picture', message=f'{request.user.username} Your Profile Picture has been changed.')
            except Profile.DoesNotExist:
                times_changed = 1
                image.name = f'{request.user.username}_pfp_{times_changed}.png'
                Profile.objects.create(user=request.user, profile_picture=image, times_changed=times_changed)

        return JsonResponse({'message': 'Image Uploaded Successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

