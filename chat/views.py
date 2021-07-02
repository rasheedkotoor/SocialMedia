from django.shortcuts import render


# Create your views here.


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    # context = ''
    # context['room_name'] = room_name
    return render(request, 'chat/catroom.html', {'room_name': room_name})
