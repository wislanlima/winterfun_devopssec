from .base_settings import *

# ALLOWED_HOSTS = env("ALLOWED_HOSTS").split(" ")
ALLOWED_HOSTS = ['44.193.75.39']

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_PORT = env("EMAIL_PORT")
DEFAULT_FROM_EMAIL = "info@winterfun.com"
DOMAIN = env("DOMAIN")
SITE_NAME = "WinterFun"

REDIS_URL = env("REDIS_URL")

CACHES = {"default": {"BACKEND": "redis_cache.RedisCache", "LOCATION": REDIS_URL}}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": env("PG_HOST"),
        "PORT": env("PG_PORT"),
    }
}
