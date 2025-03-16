from django.shortcuts import HttpResponse
from django.shortcuts import render


# Create your views here.
def init(request):
    return HttpResponse("ex01")