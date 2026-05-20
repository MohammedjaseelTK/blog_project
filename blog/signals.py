# blog/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # make sure profile is created only once
    Profile.objects.get_or_create(user=instance)
    instance.profile.save()

        
@receiver(post_save, sender=User)
def save_profile_on_user_save(sender, instance, **kwargs):
    # If a profile exists, save it; if not, create it (for safety in fresh DBs)
    Profile.objects.get_or_create(user=instance)
    instance.profile.save()
