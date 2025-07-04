from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login_view, name='login'),
    path('register', views.register_user, name='register'),
    path('ajax/send-otp/', views.send_otp, name='send_otp'),
    path('ajax/verify-otp/', views.verify_otp, name='verify_otp'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('personal-info', views.personal_info, name='personal_info'),
    path('security', views.security, name='security_info'),
    path('change_pfp', views.change_pfp, name='change_pfp'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)