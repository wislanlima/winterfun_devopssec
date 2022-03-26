

import logging

from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver


from django.contrib.auth import get_user_model

from winterfun.redis_key_schema import key_schema

logger = logging.getLogger(__name__)

User = get_user_model()

@receiver(pre_delete, sender=User)
def delete_user(sender, instance, **kwargs):
    user = instance.username
    key = key_schema().get_user_key(user)
    try:
        cache.delete(key)
    except Exception:
        print('key doesnt exist')
