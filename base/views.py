from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, Topic
from .forms import RoomForm
# Create your views here.

# rooms = [
#   {'id' : 1, 'name' : 'Lets Learn Python!'},
#   {'id' : 2, 'name' : 'Lets Learn C++!'},
#   {'id' : 3, 'name' : 'Lets Learn Java!'},
#   {'id' : 4, 'name' : 'Lets Learn javascript!'},
# ]

def login_page(request):
  if request.method == 'POST':

    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
      user = User.objects.get(username=username)
    except:
      messages.error(request, 'User does not exist')


    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('home')
    else:
      messages.error(request, 'Username or Password does not exist')


  context = {}
  return render(request, 'base/login_register.html', context)


def logout_user(request):
  logout(request)
  return redirect('home')

def home(request):
    topics = Topic.objects.all()
    q = request.GET.get('q') if request.GET.get('q') != None else ""

    rooms = Room.objects.filter(
      Q(topic__name__icontains = q) |
      Q(name__icontains = q) |
      Q(description__icontains = q) |
      Q(host__username__icontains = q)
    )
    rooms_count = rooms.count()
    context = {'rooms' : rooms, 'topics' : topics, 'rooms_count': rooms_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
  room = Room.objects.get(id=pk)
  context = {'room' : room}
  return render(request, 'base/room.html', context)


# Making a post request in Django

def create_room(request):
  form  = RoomForm()
  if(request.method == 'POST'):
    form = RoomForm(request.POST)
    if form.is_valid():
      form.save();
      return redirect('home')


  context = {'form' : form}
  return render(request, 'base/room_form.html', context)

def update_room(request, pk):
  room = Room.objects.get(id=pk)
  form = RoomForm(instance=room)

  if request.method == 'POST':
    form = RoomForm(request.POST, instance=room)
    if form.is_valid():
      form.save()
      return redirect('home')


  context = {'form' : form}
  return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
  room = Room.objects.get(id=pk)
  if request.method == 'POST':
    room.delete()
    return redirect('home')

  return render(request, 'base/delete.html', {'obj': room})