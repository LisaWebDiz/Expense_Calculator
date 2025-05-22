#!/bin/sh

echo "Миграции"
python manage.py migrate --noinput

echo "Очистка статики"
rm -rf /app/staticfiles

echo "Статика"
python manage.py collectstatic --noinput

echo "Запуск"
exec "$@"