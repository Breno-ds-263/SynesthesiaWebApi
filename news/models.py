from django.db import models
from media.models import Media
from users.models import Admin


class News(models.Model):
    Title = models.TextField(max_length=255)
    Summary = models.TextField()
    NewsLink = models.TextField(max_length=255)
    MediaFiles = models.ForeignKey(Media,on_delete = models.SET_NULL, db_column='MEDIA_FILES_ID', null = True)
    Administrator = models.ForeignKey(Admin, on_delete=models.SET_NULL, db_column='ADMIN_ID', null = True)
    CreateAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "NEWS"
