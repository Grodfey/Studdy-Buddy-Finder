from django.shortcuts import render, redirect

def index(request):
    if request.method == "GET":
        return render(request, "chat/index.html")
    elif request.method == "POST":
        return redirect('chat:room', room_name=request.POST['room'])

def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})