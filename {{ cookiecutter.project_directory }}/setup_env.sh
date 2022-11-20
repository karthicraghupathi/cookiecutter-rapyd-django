#!/usr/bin/env bash

{
    echo
    echo 'LOG_LEVEL="INFO"'
    echo
    echo DJANGO_SECRET_KEY=\"`head -c50 < /dev/urandom | base64`\"
    echo
    echo 'DEBUG="True"'
    echo
    echo DATABASE_URL=\"sqlite:///`pwd`/db.sqlite3\"
    echo
} >> .env
