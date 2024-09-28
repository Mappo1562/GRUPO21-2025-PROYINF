from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import NewRegister

def hola(request):
    return HttpResponse("HOLA MUNDO!")

def index(request):
    return render(request,'index.html')

def registerView(request):
    if request.method == "POST":
        form = NewRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = NewRegister()
    
    return render(request,'registration/register.html',{'form':NewRegister})