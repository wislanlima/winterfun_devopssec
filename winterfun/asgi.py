"""
ASGI config for winterfun project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from pathlib import Path
import environ

from django.core.asgi import get_asgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR / ".env")
if os.environ.get('HOST_ENV') == 'PRODUCTION':
    # print('prod settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.prod_settings')
elif os.environ.get('HOST_ENV') == 'STAGING':
    # print('staging settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.stage_settings')
else:
    # print('dev settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.dev_settings')

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "winterfun.dev_settings")

application = get_asgi_application()
