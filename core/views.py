import json
from django.shortcuts import render, redirect,get_object_or_404
from core.models import Evento, Categoria, Perfil
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime, timedelta
from django.http.response import Http404, JsonResponse
from django.http import HttpResponseBadRequest, JsonResponse
from dateutil.relativedelta import relativedelta  # precisa instalar: pip install python-dateutil
from django.views.decorators.csrf import csrf_exempt
from core.forms import UsuarioCadastroForm, UsuarioEdicaoForm
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import UsuarioCadastroForm, PerfilForm


# Create your views here.

@csrf_exempt
def atualizar_categoria(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        evento_id = data.get('evento_id')
        categoria_id = data.get('categoria')  # supondo que você envia o id da categoria

        try:
            evento = Evento.objects.get(id=evento_id, usuario=request.user)
            categoria = Categoria.objects.get(id=categoria_id)
            evento.categoria = categoria
            evento.save()
            # Retornar a cor junto
            return JsonResponse({'status': 'sucesso', 'cor': categoria.cor})
        except Evento.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Evento não encontrado'})
        except Categoria.DoesNotExist:
            return JsonResponse({'status': 'erro', 'mensagem': 'Categoria não encontrada'})

    return JsonResponse({'status': 'erro', 'mensagem': 'Método inválido'})
def login_user(request):
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuario ou senha inválidos")
    return redirect('/')

@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual).select_related('categoria').order_by('data_evento')
    dados = {
        'eventos': evento,
        'categorias': Categoria.objects.all()
    }
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    dados['categorias'] = Categoria.objects.all()
    return render(request, 'evento.html', dados)

@login_required(login_url='/login/')
def evento_novo(request):
    return render(request, 'evento.html')


@login_required(login_url='/login/')
def evento_submit(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_evento = request.POST.get('data_evento')
        id_evento = request.POST.get('id_evento')
        local = request.POST.get('local')
        periodicidade = request.POST.get('periodicidade', 'nenhuma')
        frequencia = request.POST.get('frequencia') or 1
        categoria_id = request.POST.get('categoria')

        # Recupera a categoria apenas uma vez
        categoria = None
        if categoria_id:
            try:
                categoria = Categoria.objects.get(id=categoria_id)
            except Categoria.DoesNotExist:
                categoria = None

        usuario = request.user

        # Converte data para datetime
        try:
            data_evento_dt = datetime.strptime(data_evento, '%Y-%m-%dT%H:%M')
        except (ValueError, TypeError):
            return HttpResponseBadRequest('Data inválida')

        # Impede salvar evento no passado
        if data_evento_dt < datetime.now():
            return HttpResponseBadRequest('Data do evento não pode ser no passado')

        # Converte frequência
        try:
            frequencia = int(frequencia)
            if frequencia < 1:
                frequencia = 1
        except ValueError:
            frequencia = 1

        if id_evento:
            try:
                evento = Evento.objects.get(id=id_evento, usuario=usuario)
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento_dt
                evento.local = local
                evento.periodicidade = periodicidade
                evento.frequencia = frequencia
                evento.categoria = categoria
                evento.save()
            except Evento.DoesNotExist:
                return HttpResponseBadRequest('Evento não encontrado ou acesso negado')
        else:
            # Cria o evento original
            Evento.objects.create(
                titulo=titulo,
                descricao=descricao,
                data_evento=data_evento_dt,
                local=local,
                usuario=usuario,
                periodicidade=periodicidade,
                frequencia=frequencia,
                categoria=categoria
            )

            # Cria eventos repetidos, se necessário
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
                    descricao=descricao,
                    data_evento=nova_data,
                    local=local,
                    usuario=usuario,
                    periodicidade=periodicidade,
                    frequencia=frequencia,
                    categoria=categoria
                )

    return redirect('/')

@login_required(login_url='/login/')
def delete_evento(request, id_evento):
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


@login_required
def usuarios_listar(request):
    if not request.user.perfil.nivel == 'admin':
        return redirect('evento_novo')

    busca = request.GET.get('q', '')
    ordenar_por = request.GET.get('ordenar_por', 'id')  # default ordenar por id
    direcao = request.GET.get('direcao', 'asc')

    usuarios = User.objects.all()

    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca) |
            Q(email__icontains=busca)
        )

    # Ordenação
    if ordenar_por not in ['id', 'username', 'email']:
        ordenar_por = 'id'  # fallback

    if direcao == 'desc':
        ordenar_por = '-' + ordenar_por

    usuarios = usuarios.order_by(ordenar_por)

    # Paginação
    paginator = Paginator(usuarios, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    cabecalhos = [
        ('id', 'ID'),
        ('username', 'Nome'),
        ('email', 'Email'),
    ]

    return render(request, 'usuarios/listar.html', {
        'page_obj': page_obj,
        'busca': busca,
        'ordenar_por': request.GET.get('ordenar_por', 'id'),
        'direcao': direcao,
        'cabecalhos': cabecalhos,
    })

def usuarios_cadastrar(request):
    if request.method == 'POST':
        user_form = UsuarioCadastroForm(request.POST)
        perfil_form = PerfilForm(request.POST, request.FILES)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            return redirect('usuarios_listar')  # ajuste conforme sua URL
    else:
        user_form = UsuarioCadastroForm()
        perfil_form = PerfilForm()

    return render(request, 'usuarios_cadastrar.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

@login_required
def usuarios_perfil(request, id):
    usuario = get_object_or_404(User, pk=id)
    return render(request, 'usuarios_perfil.html', {'usuario': usuario})

@login_required
def usuarios_editar(request, id):
    perfil_atual = getattr(request.user, 'perfil', None)
    if not perfil_atual or perfil_atual.nivel != 'admin':
        return redirect('usuarios_listar')

    user = get_object_or_404(User, id=id)
    perfil = get_object_or_404(Perfil, user=user)

    if request.method == 'POST':
        user_form = UsuarioEdicaoForm(request.POST, instance=user, perfil=perfil)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            return redirect('usuarios_listar')
    else:
        user_form = UsuarioEdicaoForm(instance=user, perfil=perfil)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'usuarios_editar.html', {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'user': user,
    })