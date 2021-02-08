"""
Django settings for {{ cookiecutter.project_slug }} project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

import logging
import os
import sys
from functools import partial, partialmethod
from pathlib import Path

from dotenv import find_dotenv, load_dotenv


# Load environment variables from the .env file
load_dotenv(find_dotenv(filename=".env", raise_error_if_not_found=True, usecwd=False))

# Setup default variables
PROJECT_NAME = "{{ cookiecutter.project_name }}"


# Logging setup

# Add new TRACE logging level
logging.TRACE = 5
logging.addLevelName(logging.TRACE, "TRACE")
logging.Logger.trace = partialmethod(logging.Logger.log, logging.TRACE)
logging.trace = partial(logging.log, logging.TRACE)

# Configure logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(asctime)s %(levelname)-8s %(name)s %(message)s"}
    },
    "handlers": {
        "console": {
            "formatter": "simple",
            "level": os.environ.get("LOG_LEVEL", "INFO"),
            "class": "logging.StreamHandler",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {"": {"handlers": ["console"], "level": "TRACE"}},
    "django": {
        "handlers": ["console"],
        "level": "TRACE",
    },
    "django.server": {
        "handlers": ["null"],
        "level": "TRACE",
        "propagate": False,
    },
}
logger = logging.getLogger("{{ cookiecutter.project_slug }}")


# Define the exception handler for unhandled exceptions
def handle_exception(exctype, value, traceback):
    """Sends unhandled exceptions to logging mechanism."""
    # ignore KeyboardInterrupt so a console python program can exit with ctrl + c
    if issubclass(exctype, KeyboardInterrupt):
        sys.__excepthook__(exctype, value, traceback)
        return
    # rely entirely on python's logging module for formatting the exception
    logger.critical("Uncaught exception", exc_info=(exctype, value, traceback))


# Hook up the exception handler
sys.excepthook = handle_exception


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{{ cookiecutter.project_slug }}.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "{{ cookiecutter.project_slug }}.wsgi.application"


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "{{ cookiecutter.project_slug }}" / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"
