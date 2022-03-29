"""
ASGI config for winterfun project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winterfun.dev_settings")

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / ".env")
if env("HOST_ENV") == 'PRODUCTION':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.prod_settings')
elif env("HOST_ENV") == 'STAGING':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.stage_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.dev_settings')

application = get_asgi_application()
