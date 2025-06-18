from django.urls import path
from . import views

urlpatterns = [
    #path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('register', views.register_user, name='register'),
    path('ajax/send-otp/', views.send_otp, name='send_otp'),
    path('ajax/verify-otp/', views.verify_otp, name='verify_otp'),
]