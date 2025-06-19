from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.register_user, name='register'),
    path('ajax/send-otp/', views.send_otp, name='send_otp'),
    path('ajax/verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout', views.logout_view, name='logout'),
]