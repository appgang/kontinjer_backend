from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete, pre_delete
from django.contrib.auth.models import User

from .models import UserProduct

print('testproduct')


@receiver(pre_delete, sender=UserProduct)
def product_post_delete(sender, instance, **kwargs):
    print("deleted! ):")
    instance.user.recycled -= 1
    instance.user.years_saved -= instance.product.material.decay
    instance.user.save()
