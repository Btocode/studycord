from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm
# Create your views here.

# rooms = [
#   {'id' : 1, 'name' : 'Lets Learn Python!'},
#   {'id' : 2, 'name' : 'Lets Learn C++!'},
#   {'id' : 3, 'name' : 'Lets Learn Java!'},
#   {'id' : 4, 'name' : 'Lets Learn javascript!'},
# ]

def home(request):
    rooms = Room.objects.all() 
    context = {'rooms' : rooms}
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
