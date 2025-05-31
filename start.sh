#!/bin/bash

# Criar diretório de logs se não existir
mkdir -p logs
chmod 755 logs

# Iniciar o Gunicorn
gunicorn wsgi:application -c gunicorn.conf.py 