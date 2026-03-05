from django.db import models
from users.models import Admin


class Card(models.Model):

    class Roles(models.IntegerChoices):
        Coordenador = 'Coordenador'
        Pesquisador = 'Pesquisador'
        Colaborador =  'colaborador'
        Egresso =  'Egresso'

    Name = models.CharField(max_length=255)
    EducationLevel = models.TextField()
    Role = models.IntegerField(choices=Roles, default=Roles.Pesquisador)
    Administrator = models.ForeignKey(Admin, on_delete=models.SET_NULL, db_column='ADMIN_ID', null=True)
    CreateAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "TEAM_CARDS"
