#!/usr/bin/env bash

echo 'LOG_LEVEL="INFO"' > .env
echo DJANGO_SECRET_KEY=\"`base64 /dev/urandom | head -c50`\" >> .env
