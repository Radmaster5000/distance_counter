from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, "distance/index.html")

def log(request):
    return render(request, "distance/log.html")