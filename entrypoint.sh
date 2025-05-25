#!/bin/sh

echo "🔄 Ожидание PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ PostgreSQL доступен"

echo "Миграции"
python manage.py migrate --noinput

echo "Очистка статики"
rm -rf /app/staticfiles

echo "Статика"
python manage.py collectstatic --noinput

echo "Запуск"
exec "$@"