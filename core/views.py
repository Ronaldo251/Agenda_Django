from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
# Create your views here.

#def index(request):
#   return redirect('/agenda/')
def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password = password)
        if usuario is not None:
            login(request,usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuario ou senha inválidos")
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)#filter(usuario=usuario) #get(id=1)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html',dados)

@login_required(login_url='/login/')
def evento_duplo(request):
    return render(request, 'evento.html')

@login_required(login_url='/login/')
def evento_submit(request):
    if request.POST:
        titulo =request.POST.get('titulo')
        descricao =request.POST.get('descricao')
        data_evento =request.POST.get('data_evento')
        id_evento = request.POST.get('id_evento')
        local = request.POST.get('local')
        usuario = request.user
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local = local
                evento.save()
            #Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                           descricao=descricao,
            #                                          data_evento=data_evento,
            #                                          local=local)
        else:
            Evento.objects.create(titulo = titulo,
                                  data_evento = data_evento,
                                  descricao = descricao,
                                  usuario = usuario,
                                  local = local)
    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request,id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()

    return redirect('/')

@login_required(login_url='/login/')
def json_lista_eventos(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id','titulo',)
    return JsonResponse(list(evento), safe=False)