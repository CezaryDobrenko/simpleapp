from scrapper.settings import *  # noqa

# PostgreSQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres",
        "USER": "postgres",
        "PASSWORD": "password",
        "HOST": "localhost",
        "PORT": "5432",
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}
