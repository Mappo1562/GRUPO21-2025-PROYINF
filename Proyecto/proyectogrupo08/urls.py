"""
URL configuration for proyectogrupo08 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import BoletinUpdateView

from django.contrib.auth.views import LoginView,LogoutView
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',views.index, name="index"),
    path('Register/',views.registro_view, name="Register"),
    path('logout/', views.logout_view, name='logout'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('solicitar_boletin/', views.solit, name='solit'),
    path('boletines/', views.boletin_list, name='boletines_list'),
    path('boletines/<int:boletin_id>/', views.boletin_detail, name='boletin_detail'),
    path('boletines/<int:boletin_id>/aprobar/', views.aprobar_boletin, name='aprobar_boletin'),
    path('boletin/<int:pk>/edit/', BoletinUpdateView.as_view(), name='boletin_edit'),

    path('categorias/nueva/', views.crear_categoria, name='crear_categoria'),
    path('categorias/', views.categorias_list, name='categorias_list'),
    path('preenvios/', views.preenvios_list, name='preenvios_list'),
    path('preenvios/<int:preenvio_id>/', views.preenvios_detail, name='preenvios_detail'),
    path('preenvios/<int:preenvio_id>/rechazar/', views.rechazar_preenvio, name='rechazar_preenvio'),
    path('preenvios/<int:preenvio_id>/subir/', views.subir_preenvio, name='subir_preenvio'),
    path('preenvios/categoria/<int:categoria_id>/', views.preenvios_por_categoria, name='preenvios_por_categoria'),
    
    path('historial/', views.historial_list, name='historial_list'),
    path('historial/<int:historial_id>/', views.historial_detail, name='historial_detail'),
]
