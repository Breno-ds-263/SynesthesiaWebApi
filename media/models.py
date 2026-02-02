from django.db import models
from users.models import Admin


class Media(models.Model):
    FileName = models.CharField(max_length=255, unique=True)
    Path = models.CharField(max_length=500)
    TypeFile = models.CharField(max_length=50)
    SizeBytes = models.IntegerField()
    administrator = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column='ADMINISTRADOR_ID')
    CreateAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "MEDIA_FILES"
