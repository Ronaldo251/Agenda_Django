from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.
PERIODICIDADE_OPCOES = [
    ('nenhuma', 'Nenhuma'),
    ('diaria', 'Diariamente'),
    ('semanal', 'Semanalmente'),
    ('mensal', 'Mensalmente'),
]
class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    local = models.CharField(max_length=25,blank=True,null=True)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    periodicidade = models.CharField(max_length=10, choices=PERIODICIDADE_OPCOES, blank=True, null=True)
    frequencia = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'evento'

    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False
