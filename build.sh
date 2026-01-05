#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install Dependencies
pip install -r requirements.txt

# 2. Clean old files (Ensures no "corrupt" styles remain)
rm -rf staticfiles

# 3. Collect Static Files
# Fixed: it is "--noinput", not "--no-input"
python manage.py collectstatic --noinput

# 4. Migrate Database
python manage.py migrate

# 5. Create Superuser (Only if missing)
# Note: Changing the password here won't update an existing admin, only create a new one.
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else print('Admin already exists')"