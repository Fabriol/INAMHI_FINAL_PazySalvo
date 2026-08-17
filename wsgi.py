"""Punto de entrada para Gunicorn en producción.

Uso (ver deploy/gunicorn-pazsalvo.service):
    gunicorn --workers 3 --timeout 120 --bind unix:/opt/paz_salvo/paz_salvo.sock wsgi:app
"""
from app import create_app

app = create_app()
