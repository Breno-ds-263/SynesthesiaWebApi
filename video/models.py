from django.db import models

from users.models import Admin


class Video(models.Model):
    Title= models.CharField(max_length=255, unique=True)
    VideoUrl = models.TextField()
    Administrator = models.ForeignKey(Admin, on_delete=models.SET_NULL, db_column='ADMIN_ID', null=True)
    CreateAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "VIDEO"
