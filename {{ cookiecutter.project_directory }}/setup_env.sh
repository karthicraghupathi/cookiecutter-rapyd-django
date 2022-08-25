#!/usr/bin/env bash

{
    echo
    echo 'LOG_LEVEL="INFO"'
    echo
    echo DJANGO_SECRET_KEY=\"`base64 /dev/urandom | head -c50`\"
    echo
    echo 'DEBUG="True"'
    echo
    echo DATABASE_URL=\"sqlite:///`pwd`/db.sqlite3\"
    echo
} >> .env
