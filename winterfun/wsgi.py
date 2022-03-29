"""
WSGI config for winterfun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winterfun.dev_settings")


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / ".env")
if env("HOST_ENV") == 'PRODUCTION':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.prod_settings')
elif env("HOST_ENV") == 'STAGING':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.stage_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.dev_settings')


application = get_wsgi_application()
