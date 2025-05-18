#!/bin/bash

# Применяем миграции
alembic upgrade head

# Запускаем приложение
exec gunicorn src.main:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --log-level info --bind=0.0.0.0:8080


