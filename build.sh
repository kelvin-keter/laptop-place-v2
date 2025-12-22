#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# 1. Force delete old static files to ensure a fresh copy
rm -rf staticfiles

# 2. Collect static files but IGNORE the broken Cloudinary file
# This is the "Magic Flag" that fixes the build crash
python manage.py collectstatic --no-input --clear --ignore "cloudinary_cors.html"

python manage.py migrate

# Create Superuser if missing
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin already exists')"