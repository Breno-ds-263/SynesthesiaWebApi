from django.db import models

from media.models import Media
from users.models import Admin
import json

class Card(models.Model):

    class Roles(models.TextChoices):
        Coordenador = 'Coordenador'
        Pesquisador = 'Pesquisador'
        Colaborador =  'Colaborador'
        Egresso =  'Egresso'

    Name = models.CharField(max_length=255)
    EducationLevel = models.TextField()
    Role = models.TextField(choices=Roles, default=Roles.Pesquisador)
    LinkLattes = models.TextField(null=True, blank=True)
    Gmail = models.EmailField(null=True, blank=True)
    Linked = models.TextField(null=True, blank=True)
    MediaFiles = models.ForeignKey(Media, on_delete=models.SET_NULL, db_column='MEDIA_FILES_ID', null=True)
    Administrator = models.ForeignKey(Admin, on_delete=models.SET_NULL, db_column='ADMIN_ID', null=True)
    CreateAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "TEAM_CARDS"
