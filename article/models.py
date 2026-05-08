from django.db import models
from django.core.exceptions import ValidationError

from media.models import Media
from users.models import Admin
from django.utils import timezone


class Articles(models.Model):

    class Tags(models.TextChoices):
        ARTIGO_COMPLETO = "Artigo Completo"
        RESUMO_EXPANDIDO = "Resumo Expandido"
        POSTER = "Poster"

    Title = models.CharField(max_length=255)
    Summary = models.TextField()
    Tag = models.CharField(
        max_length=20,
        choices=Tags.choices,
        default=Tags.ARTIGO_COMPLETO
    )
    Event = models.CharField(max_length=255, null=True, blank=True)
    Year = models.CharField(max_length=255, null=True, blank=True)
    ArticleLink = models.TextField()
    MediaFiles = models.ForeignKey(Media, on_delete=models.SET_NULL, db_column='MEDIA_FILES_ID', null=True)
    Administrator = models.ForeignKey(Admin, on_delete=models.CASCADE, db_column='ADMIN_ID')
    CreateAt = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.Tag not in self.Tags.values:
            raise ValidationError({
                "tag": "Tag inválida"
            })

    def save(self, *args, **kwargs):
        self.full_clean()  # chama o clean()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "ARTICLES"