from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User

from .models import Profile

print('test')


@receiver(post_save, sender=User, dispatch_uid='user.create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print("test")
        Profile.objects.create(user=instance, recycled=0)
