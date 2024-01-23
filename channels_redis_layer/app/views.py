from django.shortcuts import render

# Create your views here.

def index(request, group_name):
    context = None
    return render(request, 'app/index.html', {"groupname": group_name})

