from django.db import models
from django.conf import settings
from django.utils import timezone
from user.models import Profile


class Material(models.Model):
    name = models.CharField(max_length=100, default="")
    decay = models.IntegerField(default=41)

    def __str__(self):
        return self.name


class Product(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.name



class UserProduct(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product')
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.username + ", " + self.product.name
