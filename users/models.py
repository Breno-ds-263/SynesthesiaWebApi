from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ADMIN'