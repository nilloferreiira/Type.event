from django.db import models
from django.db.models import CharField, ImageField, DateField, IntegerField, TextField
from django.contrib.auth.models import User

class Evento(models.Model):
    criador = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    nome = CharField(max_length=200)
    descricao = TextField()
    data_inicio = DateField()
    data_termino = DateField()
    carga_horaria = IntegerField()
    logo = ImageField(upload_to="logos")

    #paleta de cores

    cor_principal = CharField(max_length=7)
    cor_secundaria = CharField(max_length=7)
    cor_fundo = CharField(max_length=7)

    def __str__(self):
        return self.nome