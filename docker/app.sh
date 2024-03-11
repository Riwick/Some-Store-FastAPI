#!/usr/bin/env sh

alembic upgrade heads

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000