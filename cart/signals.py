from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import *
from .models import *



@receiver(post_save, sender=User)
def create_user_resources(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
        Wishlist.objects.create(user=instance)