from django.db import models

from media.models import Media
from users.models import Admin


class Materials(models.Model):

    Title = models.CharField(max_length=255)
    Summary = models.TextField()
    MaterialsLink = models.TextField()
    MediaFiles = models.ForeignKey(Media, on_delete = models.SET_NULL,db_column='MEDIA_FILES_ID',  null = True )
    Administrator = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column='ADMIN_ID')
    CreateAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "MATERIALS"





