#!/usr/bin/env bash

# make manage.py executable
chmod +x {{ cookiecutter.project_slug }}/manage.py

# run the script to setup the environment
chmod +x setup_env.sh
./setup_env.sh
