from django.db import models
from django import forms
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm


# Opções de repetição de evento
PERIODICIDADE_OPCOES = [
    ('nenhuma', 'Nenhuma'),
    ('diaria', 'Diariamente'),
    ('semanal', 'Semanalmente'),
    ('mensal', 'Mensalmente'),
]

from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefone = models.CharField(max_length=20)
    
    NIVEL_CHOICES = (
        ('admin', 'Administrador'),
        ('usuario', 'Usuário'),
    )
    nivel = models.CharField(max_length=10, choices=NIVEL_CHOICES, default='usuario')
    
    # Novo campo:
    foto = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.nivel}'

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    cor = models.CharField(max_length=7, default='#00ff88')  # Ex: #FF0000

    def __str__(self):
        return self.nome

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    local = models.CharField(max_length=25, blank=True, null=True)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    periodicidade = models.CharField(
        max_length=10,
        choices=PERIODICIDADE_OPCOES,
        blank=True,
        null=True,
        default='nenhuma'
    )
    frequencia = models.PositiveIntegerField(blank=True, null=True, default=1)
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):
        return self.data_evento < datetime.now()
    

