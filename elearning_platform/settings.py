from pathlib import Path
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Security / Debug ---
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")  # set in Render
ALLOWED_HOSTS = [
    "localhost", "127.0.0.1",
    # your local IP if needed:
    "172.31.192.53",
    # Render domains:
    ".onrender.com",
    # add your custom domain too (without protocol)
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.onrender.com",
    # "https://yourdomain.com",
]

# --- Apps ---
INSTALLED_APPS = [
      "cloudinary",
    "cloudinary_storage",
    "whitenoise.runserver_nostatic",  # dev convenience (no collectstatic needed locally)
    "drf_spectacular",
    "rest_framework",
    "widget_tweaks",
    "channels",
    "chat",
    "courses",
    "dashboard",
    "accounts",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# --- Middleware (WhiteNoise must be right after SecurityMiddleware) ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "elearning_platform.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "dashboard.context_processors.merged_notifications",
            ],
        },
    },
]

# WSGI/ASGI
WSGI_APPLICATION = "elearning_platform.wsgi.application"
ASGI_APPLICATION = "elearning_platform.asgi.application"

# --- Database (Render supplies DATABASE_URL) ---
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", "postgresql://localhost:5432/mydb"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# --- DRF / Spectacular ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SPECTACULAR_SETTINGS = {
    "TITLE": "eLearning Platform API",
    "DESCRIPTION": "Auto-generated API docs for the eLearning coursework.",
    "VERSION": "1.0.0",
}

# --- Auth / Redirects ---
AUTH_USER_MODEL = "accounts.CustomUser"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

# --- Media ---
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

CLOUDINARY_URL = os.getenv("CLOUDINARY_URL", "")
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME", None),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY", None),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET", None),
    "SECURE": True,          # use https
    # "overwrite": False,    # keep versions if you prefer
}

# --- Password validators ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Channels (choose ONE block) ---

# A) Simple single-instance (no Redis), OK to start:
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",
#     }
# }

# B) Production / multi-instance via Redis on Render:
# set REDIS_URL env var in Render (e.g. from a Redis service)
if os.getenv("REDIS_URL"):
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {"hosts": [os.getenv("REDIS_URL")]},
        }
    }
else:
    # fallback to in-memory if REDIS_URL not set
    CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

# --- Email ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "noreply@example.com"

# --- I18N / TZ ---
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Singapore"  # optional; you can keep UTC if you prefer
USE_I18N = True
USE_TZ = True

# --- Static / WhiteNoise ---
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# --- Defaults ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
