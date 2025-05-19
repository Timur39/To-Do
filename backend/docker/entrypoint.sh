#!/bin/bash

# Применяем миграции
alembic upgrade head

# Запускаем приложение
exec uvicorn src.main:app --host 0.0.0.0 --port 8080 --workers 3
