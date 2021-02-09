#!/usr/bin/env bash

echo LOG_LEVEL=INFO > .env
echo DJANGO_SECRET_KEY=$(LC_ALL=C tr -dc 'A-Za-z0-9!"#$%&'\''()*+,-./:;<=>?@[\]^_`{|}~' </dev/urandom | head -c 64 ; echo) >> .env
