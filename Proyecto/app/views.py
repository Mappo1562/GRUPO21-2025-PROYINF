from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login , logout
from proyectogrupo08.forms import NewRegister, RegistroForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Profile,Solicitud,Preenvios,Categoria
from proyectogrupo08.forms import solicitud_form, CategoriaForm
from django.views.generic.edit import UpdateView
from django.urls import reverse
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


def boletin_detail(request, boletin_id):
    boletin = get_object_or_404(Solicitud, id=boletin_id)
    categorias = Categoria.objects.all()
    error = None

    if request.method == 'POST':
        # Viene del formulario de “aprobar” con categoría
        categoria_id = request.POST.get('categoria_id')
        if categoria_id:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            Preenvios.objects.create(
                title=boletin.title,
                content=boletin.content,
                categoria=categoria
            )
            boletin.delete()
            return redirect('boletines_list')
        else:
            error = "Debes seleccionar una categoría para aprobar."

    return render(request, 'boletin_detail.html', {
        'boletin': boletin,
        'categorias': categorias,
        'error': error
    })


def aprobar_boletin(request, boletin_id):
    boletin = get_object_or_404(Solicitud, id=boletin_id)
    categorias = Categoria.objects.all()

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')
        if categoria_id:
            categoria = get_object_or_404(Categoria, id=categoria_id)
            # Crear el preenvío con categoría
            Preenvios.objects.create(
                title=boletin.title,
                content=boletin.content,
                categoria=categoria
            )
            boletin.delete()
            return redirect('boletines_list')
        else:
            error = "Debes seleccionar una categoría"
            return render(request, 'aprobar_boletin.html', {
                'boletin': boletin,
                'categorias': categorias,
                'error': error
            })

    # GET: mostrar formulario
    return render(request, 'aprobar_boletin.html', {
        'boletin': boletin,
        'categorias': categorias
    })








def rechazar_preenvio(request, preenvio_id):
    preenvio = get_object_or_404(Preenvios, id=preenvio_id)

    Solicitud.objects.create(
        title=preenvio.title,
        content=preenvio.content
    )

    preenvio.delete()
    return redirect('Preenvios_list')


def Preenvios_list(request):
    preenvios = Preenvios.objects.all()
    return render(request, 'preenvios_list.html', {'preenvios': preenvios})


def Preenvios_detail(request, preenvio_id):
    preenvio = get_object_or_404(Preenvios, id=preenvio_id)
    return render(request, 'Preenvios_detail.html', {'preenvio': preenvio})


def subir_preenvio(request, preenvio_id):
    preenvio = get_object_or_404(Preenvios, id=preenvio_id)
    preenvio.delete()
    return redirect('Preenvios_list')  


class BoletinUpdateView(UpdateView):
    model = Solicitud
    fields = ['title', 'content']  
    template_name = 'boletin_edit.html'
    
    def get_success_url(self):
        return reverse('boletin_detail', kwargs={'boletin_id': self.object.pk})
    












def crear_categoria(request):

    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CategoriaForm()

    return render(request, 'crear_categoria.html', {'form': form})



def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias_list.html', {
        'categorias': categorias
    })


def preenvios_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    boletines = Preenvios.objects.filter(categoria=categoria)
    return render(request, 'preenvios_list.html', {
        'boletines': boletines,
        'categoria': categoria
    })