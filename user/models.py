from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recyled = models.IntegerField()
    products = models.ManyToManyField(
        'materials.Product', through='materials.UserProduct', related_name='products')

    def __str__(self):
        return self.user.username
