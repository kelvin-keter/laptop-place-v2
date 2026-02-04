import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-123')

# Render sets this to False automatically
DEBUG = 'RENDER' not in os.environ

# --- 1. SECURITY UPDATE: DOMAIN WHITELIST ---
ALLOWED_HOSTS = [
    'laptopplacekenya.com',       # Your Root Domain
    'www.laptopplacekenya.com',   # Your WWW Domain
    '.onrender.com',              # Allows Render subdomains (e.g. laptop-place.onrender.com)
    '127.0.0.1',                  # Localhost
    'localhost',
]

# --- 2. SECURITY UPDATE: FORM TRUST ---
# Essential for login/upload forms to work on your new domain
CSRF_TRUSTED_ORIGINS = [
    'https://laptopplacekenya.com',
    'https://www.laptopplacekenya.com',
    'https://*.onrender.com',
]

INSTALLED_APPS = [
    # --- 1. NEW: JAZZMIN ADMIN THEME (MUST BE AT THE TOP) ---
    'jazzmin',

    # 3rd Party
    'cloudinary_storage',
    'cloudinary',
    'whitenoise.runserver_nostatic',

    # Django Default Apps
    'django.contrib.staticfiles',
    'django.contrib.admin',         # Jazzmin must be loaded BEFORE this
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    
    # Helper for adding commas to numbers
    'django.contrib.humanize',

    # Our Apps
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Critical: This serves the files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# --- STATIC FILES CONFIGURATION ---
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 1. Look for static files in our custom folder (Logo, Theme CSS)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 2. Look for static files inside Django Apps (Admin CSS)
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# --- WHITENOISE CONFIGURATION ---
WHITENOISE_USE_FINDERS = True

# Media Files (User Uploads)
MEDIA_URL = '/media/'

# CLOUDINARY CONFIGURATION
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'drkkg7wf2',
    'API_KEY': '637631316581369',
    'API_SECRET': 'tOdPXLziEQMeOyDR3yJXdv0Wp-s',
}

# --- STORAGE CONFIGURATION (SAFE & STABLE) ---
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# --- AUTHENTICATION REDIRECTS ---
LOGIN_REDIRECT_URL = 'dashboard'

# --- 2. NEW: JAZZMIN CONFIGURATION ---
JAZZMIN_SETTINGS = {
    "site_title": "Laptop Place Admin",
    "site_header": "Laptop Place Kenya",
    "site_logo": None, 
    "welcome_sign": "Welcome to Laptop Place HQ",
    "copyright": "Laptop Place Kenya Ltd",
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core.Product": "fas fa-laptop",
        "core.Category": "fas fa-tag",
        "core.Review": "fas fa-star",
    },
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-success",
    "navbar": "navbar-success navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-success",
    "sidebar_nav_small_text": False,
    "theme": "flatly",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-success",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}