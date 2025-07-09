from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from a_app.models import Channel
from a_app.forms import ChannelForm
# Create your views here.

def home(request):
    user = request.user
    channels = Channel.objects.all()
    return render(request, 'a_app/home.html', {'user': user, 'channels': channels})

def about(request):
    return render(request, 'a_app/about.html')

def view_channel(request, id):
    channel = Channel.objects.get(id=id)


    return render(request, 'a_app/layout.html', {'channel': channel})

def create_channel(request):
    owner = request.user
    if request.method == "POST":
        form = ChannelForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            channel = Channel(owner=owner, title=title, description=description)
            channel.save()
            return redirect('home')
    else:
        form = ChannelForm()
    return render(request, 'a_app/create_channel.html', {'owner': owner, 'form': form})