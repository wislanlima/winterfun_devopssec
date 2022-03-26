import logging
import os

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from posts.models import Post
from winterfun.base_settings import AUTH_USER_MODEL

logger = logging.getLogger(__name__)



@receiver(pre_save, sender=Post)
def update_post_image(sender, instance, **kwargs):
    print('post here update post image')
    if not instance.pkid:
        return False
    try:
        old_file = Post.objects.get(pkid=instance.pkid).image
    except Post.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
            logger.info(f"{old_file.path} ====>  Deleted")


