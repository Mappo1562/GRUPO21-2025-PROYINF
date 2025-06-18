from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login , logout
from proyectogrupo08.forms import NewRegister, RegistroForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib import messages
from .models import Profile,Solicitud,Preenvios,Categoria,Historial
from proyectogrupo08.forms import solicitud_form, CategoriaForm
from django.views.generic.edit import UpdateView
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
# Create your views here.

@require_GET
@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'index.html', {'profile': profile})

@require_http_methods(["GET", "POST"])
def registro_view(request):
    if request.method == 'POST':
        form = NewRegister(request.POST)
        if form.is_valid():
            user = form.save()
            if not request.user.is_authenticated:
                auth_login(request, user)
            return redirect('index')
    else:
        form = NewRegister()
    return render(request, 'Register.html', {'form': form})

@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión correctamente.')
    return redirect('index')

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        form = NewRegister(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request,'registration/register.html',{'form': NewRegister})

@require_http_methods(["GET", "POST"])
def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = get_user_model().objects.get(username=username)
            user.delete()
            return redirect('index')
        except get_user_model().DoesNotExist:
            return render(request, 'delete_user.html', {'error': 'Usuario no encontrado.'})
    return render(request, 'delete_user.html')

@require_http_methods(["GET", "POST"])
def solit(request):
    if request.method == 'POST':
        form = solicitud_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = solicitud_form()
    return render(request, 'solit.html', {'form': form})

@require_GET
def boletin_list(request):
    boletines = Solicitud.objects.all()
    return render(request, 'boletines_list.html', {'boletines': boletines})

@require_http_methods(["GET", "POST"])
def boletin_detail(request, boletin_id):
    boletin = get_object_or_404(Solicitud, id=boletin_id)
    categorias = Categoria.objects.all()
    error = None
    if request.method == 'POST':
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

@require_http_methods(["GET", "POST"])
def aprobar_boletin(request, boletin_id):
    boletin = get_object_or_404(Solicitud, id=boletin_id)
    categorias = Categoria.objects.all()
    if request.method == 'POST':
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
            error = "Debes seleccionar una categoría"
            return render(request, 'aprobar_boletin.html', {
                'boletin': boletin,
                'categorias': categorias,
                'error': error
            })
    return render(request, 'aprobar_boletin.html', {
        'boletin': boletin,
        'categorias': categorias
    })

@require_POST
def rechazar_preenvio(request, preenvio_id):
    preenvio = get_object_or_404(Preenvios, id=preenvio_id)
    Solicitud.objects.create(
        title=preenvio.title,
        content=preenvio.content
    )
    preenvio.delete()
    return redirect('categorias_list')

@require_GET
def preenvios_list(request):
    preenvios = Preenvios.objects.all()
    return render(request, 'preenvios_list.html', {'preenvios': preenvios})

@require_GET
def preenvios_detail(request, preenvio_id):
    preenvio = get_object_or_404(Preenvios, id=preenvio_id)
    return render(request, 'Preenvios_detail.html', {'preenvio': preenvio})

@require_POST
def subir_preenvio(request, preenvio_id):
    preenvio = get_object_or_404(Preenvios, id=preenvio_id)
    Historial.objects.create(
        title=preenvio.title,
        content=preenvio.content,
        categoria=preenvio.categoria
    )
    preenvio.delete()
    return redirect('categorias_list')

class BoletinUpdateView(UpdateView):
    model = Solicitud
    fields = ['title', 'content']  
    template_name = 'boletin_edit.html'
    def get_success_url(self):
        return reverse('boletin_detail', kwargs={'boletin_id': self.object.pk})

@require_http_methods(["GET", "POST"])
def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CategoriaForm()
    return render(request, 'crear_categoria.html', {'form': form})

@require_GET
def categorias_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'categorias_list.html', {'categorias': categorias})

@require_GET
def preenvios_por_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    boletines = Preenvios.objects.filter(categoria=categoria)
    return render(request, 'preenvios_list.html', {'boletines': boletines, 'categoria': categoria})

@require_GET
def historial_list(request):
    boletines = Historial.objects.all().order_by('-created_at')
    return render(request, 'historial_list.html', {'boletines': boletines})

@require_GET
def historial_detail(request, historial_id):
    boletin = get_object_or_404(Historial, id=historial_id)
    return render(request, 'historial_detail.html', {'boletin': boletin})