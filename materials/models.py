from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=100, default="test")
    decay = models.IntegerField(default=41)

    def __str__(self):
        return self.name
