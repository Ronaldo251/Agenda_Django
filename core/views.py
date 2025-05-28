import json
from django.shortcuts import render, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.utils.timezone import now,make_aware
from django.http import HttpResponseBadRequest, JsonResponse
from dateutil.relativedelta import relativedelta  # precisa instalar: pip install python-dateutil
from django.views.decorators.csrf import csrf_exempt
from .models import Evento, Categoria

# Create your views here.

#def index(request):
#   return redirect('/agenda/')

@csrf_exempt
def atualizar_categoria(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        evento_id = data.get('evento_id')
        categoria_nome = data.get('categoria')

        try:
            evento = Evento.objects.get(id=evento_id, usuario=request.user)
            categoria = Categoria.objects.get(nome=categoria_nome)  # nome, não id
            evento.categoria = categoria
            evento.save()
            return JsonResponse({'status': 'sucesso'})
        except Evento.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Evento não encontrado'})
        except Categoria.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Categoria não encontrada'})
        
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
                                   data_evento__gt=data_atual).select_related('categoria').order_by('data_evento')#filter(usuario=usuario) #get(id=1)
    dados = {'eventos': evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    categoria_id = request.POST.get('categoria')
    categoria = None
    if categoria_id:
        try:
            categoria = Categoria.objects.get(id=categoria_id)
        except Categoria.DoesNotExist:
            categoria = None
    if id_evento:
        evento.categoria = categoria
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html',dados)

@login_required(login_url='/login/')
def evento_duplo(request):
    return render(request, 'evento.html')


@login_required(login_url='/login/')
def evento_submit(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_evento = request.POST.get('data_evento')
        id_evento = request.POST.get('id_evento')
        local = request.POST.get('local')
        periodicidade = request.POST.get('periodicidade', 'nenhuma')
        frequencia = request.POST.get('frequencia') or 1
        usuario = request.user

        # Converte data e frequencia com validação
        try:
            data_evento_dt = datetime.strptime(data_evento, '%Y-%m-%dT%H:%M')  # Sem make_aware
        except (ValueError, TypeError):
            return HttpResponseBadRequest('Data inválida')

        if data_evento_dt < datetime.now():  # Comparação entre naive datetimes
            return HttpResponseBadRequest('Data do evento não pode ser no passado')

        try:
            frequencia = int(frequencia)
            if frequencia < 1:
                frequencia = 1
        except ValueError:
            frequencia = 1

        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento_dt
                evento.local = local
                evento.periodicidade = periodicidade
                evento.frequencia = frequencia
                
                evento.save()
        else:
            # Evento principal
            Evento.objects.create(
                titulo=titulo,
                data_evento=data_evento_dt,
                descricao=descricao,
                usuario=usuario,
                local=local,
                periodicidade=periodicidade,
                frequencia=frequencia
                categoria=categoria
            )

            # Eventos periódicos
            for i in range(1, frequencia):
                if periodicidade == 'diario':
                    nova_data = data_evento_dt + timedelta(days=i)
                elif periodicidade == 'semanal':
                    nova_data = data_evento_dt + timedelta(weeks=i)
                elif periodicidade == 'mensal':
                    nova_data = data_evento_dt + relativedelta(months=i)
                else:
                    continue

                Evento.objects.create(
                    titulo=titulo,
                    data_evento=nova_data,
                    descricao=descricao,
                    usuario=usuario,
                    local=local,
                    periodicidade=periodicidade,
                    frequencia=frequencia
                    categoria=categoria
                )

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
    evento = Evento.objects.filter(usuario=usuario).order_by('data_evento').values('id', 'titulo', 'data_evento')
    return JsonResponse(list(evento), safe=False)
