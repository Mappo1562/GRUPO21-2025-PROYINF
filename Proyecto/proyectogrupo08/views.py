from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login , logout
from .forms import NewRegister, RegistroForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages


def index(request):
    return render(request,'index.html')


"""
def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            # Manejar el error de contraseñas no coincidentes
            error_message = "Las contraseñas no coinciden."
            return render(request, 'Register.html', {'error_message': error_message})

        # Guardar el usuario
        usuario = User.objects.create_user(username=username, password=password)

        auth_login(request, usuario)  # Autenticar al usuario automáticamente

        return redirect('index')  # Redirigir a la página de inicio

    return render(request, 'Register.html')
"""
