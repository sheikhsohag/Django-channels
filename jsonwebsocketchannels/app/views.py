from django.shortcuts import render
from . models import Group, Chat

# Create your views here.

def index(request, group_name):
    group = Group.objects.filter(name=group_name).first()
    if group:
        chats = Chat.objects.filter(group=group)
    else:
        groupname  = Group(name = group_name)
        groupname.save()
    return render(request, 'app/index.html', {'groupname': group_name, 'chats': chats})
