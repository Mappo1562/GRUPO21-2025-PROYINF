from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login , logout
from .forms import NewRegister, RegistroForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages


def index(request):
    return render(request,'index.html')


