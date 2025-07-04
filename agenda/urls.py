"""agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from core import views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agenda/',views.lista_eventos),
    path('agenda/lista/',views.json_lista_eventos),
    path('agenda/lista/<int:id_usuario>/',views.json_lista_eventos),
    path('agenda/evento/',views.evento),
    path('agenda/evento/submit',views.evento_submit, name='evento_submit'),   
    path('agenda/evento/delete/<int:id_evento>/',views.delete_evento),
    path('', RedirectView.as_view(url='/agenda/')),
    path('agenda/evento/evento/', RedirectView.as_view(url='/agenda/evento/')),
    #path('',views.index),
    path('login/',views.login_user),
    path('login/submit',views.submit_login),
    path('logout/',views.logout_user),
    path('atualizar_categoria/', views.atualizar_categoria, name='/atualizar_categoria/'),
    path('usuarios/listar/', views.usuarios_listar, name='usuarios_listar'),
    path('usuarios/cadastrar/', views.usuarios_cadastrar, name='usuarios_cadastrar'),
    path('agenda/usuarios/perfil/<int:id>/', views.usuarios_perfil, name='usuarios_perfil'),
    path('agenda/usuarios/editar/<int:id>/', views.usuarios_editar, name='usuarios_editar'),
    path('agenda/evento/', views.evento_novo, name='evento_novo'),
    path('agenda/usuarios/editar/<int:id>/', views.usuarios_editar, name='usuarios_editar'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
