import logging
import os

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from profiles.models import Profile, Relationship
from winterfun.base_settings import AUTH_USER_MODEL

logger = logging.getLogger(__name__)






@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        logger.info(f"{instance}'s creating user profile")


@receiver(pre_save, sender=Profile)
def update_user_avatar(sender, instance, **kwargs):
    if not instance.pkid:
        return False
    try:
        old_file = Profile.objects.get(pkid=instance.pkid).avatar
    except Profile.DoesNotExist:
        return False
    new_file = instance.avatar
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
            logger.info(f"{old_file.path} ====>  Deleted")

"""Quando loga chama isso?"""
# @receiver(post_save, sender=AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     logger.info(f"{instance}'s save user profile")


@receiver(pre_delete, sender=Profile)
def delete_image(sender, instance, **kwargs):
    name = instance.avatar.name
    if name == 'avatar.png':
        print('user.signal.py Default.jpg not deleted')
    else:
        instance.avatar.delete()
        logger.info(f"{name}  ====>  Deleted")


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    if instance.status == "accepted":
        sender_.friends.add(receiver_.user)
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()
        logger.info(f"{instance}'s post save add to friends")


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_from_friends(sender, instance, **kwargs):
    sender = instance.sender
    receiver = instance.receiver
    sender.friends.remove(receiver.user)
    receiver.friends.remove(sender.user)
    sender.save()
    receiver.save()
    logger.info(f"{instance}'s pre delete remove from friends")
