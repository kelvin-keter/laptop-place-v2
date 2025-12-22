#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# 1. Force delete old static files (Fixes "0 files copied" bug)
rm -rf staticfiles

# 2. Collect static files (Standard mode - no crashes)
python manage.py collectstatic --no-input --clear

python manage.py migrate

# Create Superuser if missing
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin already exists')"