from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def populate(request):
    return HttpResponse('populate')

def display(request):
    return HttpResponse('display')