#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path
import environ


def main():
    """Run administrative tasks."""
    BASE_DIR = Path(__file__).resolve().parent.parent
    environ.Env.read_env(BASE_DIR / ".env")
    if os.environ.get('HOST_ENV') == 'PRODUCTION':

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.prod_settings')
    elif os.environ.get('HOST_ENV') == 'STAGING':
        # print('staging settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.stage_settings')
    else:
        # print('dev settings')
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'winterfun.dev_settings')



    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
