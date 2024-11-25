from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login , logout
from proyectogrupo08.forms import NewRegister, RegistroForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Profile,Solicitud
from proyectogrupo08.forms import solicitud_form
# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    else:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'index.html', {'profile': profile})


def registro_view(request):
    if request.method == 'POST':
        form = NewRegister(request.POST)
        if form.is_valid():
            user = form.save()
            # Verifica si ya hay un usuario autenticado
            if not request.user.is_authenticated:
                auth_login(request, user)  # Solo autentica al nuevo usuario si no hay uno autenticado
            return redirect('index')  # Redirigir a la página de inicio
    else:
        form = NewRegister()
    
    return render(request, 'Register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, '')
    return redirect('index')


def login(request):
    if request.method == "POST":
        form = NewRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = NewRegister()
    return render(request,'registration/register.html',{'form':NewRegister})


def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            user.delete()
            return redirect('index')  # Redirigir después de eliminar
        except User.DoesNotExist:
            return render(request, 'delete_user.html', {'error': 'Usuario no encontrado.'})

    return render(request, 'delete_user.html')



def solit(request):
    if request.method == 'POST':
        form = solicitud_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index') 
    else:
        form = solicitud_form()
    return render(request, 'solit.html', {'form': form})



def boletin_list(request):
    boletines = Solicitud.objects.all()
    return render(request, 'boletines_list.html', {'boletines': boletines})


def boletin_detail(request, solicitud_id):
    boletin = get_object_or_404(Solicitud, id=solicitud_id)
    return render(request, 'boletin_detail.html', {'boletin': boletin})