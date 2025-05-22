#!/bin/sh

echo "Миграции"
python manage.py migrate --noinput

echo "Статика"
python manage.py collectstatic --noinput

echo "Запуск"
exec "$@"