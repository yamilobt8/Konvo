from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('create_channel', views.create_channel, name='create_channel'),
    path('view_channel/<int:channel_id>', views.view_channel, name='view_channel'),
]