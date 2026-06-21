"""
Django settings for Forge — AI portfolio generator backend.
Env-driven via django-environ. See .env.example.
"""
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
# Read .env if present (local dev). Prod sets real env vars.
environ.Env.read_env(BASE_DIR / ".env")

# --- Core ---
SECRET_KEY = env("SECRET_KEY", default="dev-insecure-change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third-party
    "rest_framework",
    "corsheaders",
    "drf_spectacular",
    # local
    "apps.users",
    "apps.portfolios",
    "apps.gallery",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Database (Neon prod / docker-compose Postgres local) ---
# DATABASE_URL=postgres://user:pass@host:5432/dbname
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://forge:forge@localhost:5432/forge",
    ),
}
# env.db() already maps postgres:// -> django.db.backends.postgresql (uses psycopg3).

AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = []  # Clerk owns passwords; Django stores none

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- DRF ---
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.users.authentication.ClerkJWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "20/hour",        # gallery browse only
        "user": "100/hour",       # general authed API
        "generate": "5/hour",     # ScopedRateThrottle — Groq LLM (cost)
        "avatar_gen": "5/hour",   # ScopedRateThrottle — Replicate (cost)
        "deploy": "10/hour",      # ScopedRateThrottle
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Forge API",
    "DESCRIPTION": "AI multi-niche portfolio generator",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# --- Redis (optional in dev) ---
# Set REDIS_URL for real Redis. If empty: LocMem cache + Celery runs eager
# (tasks execute synchronously in-process — fine for local dev, no broker needed).
REDIS_URL = env("REDIS_URL", default="")

if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        },
    }
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    CELERY_TASK_ALWAYS_EAGER = False
else:
    CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    }
    CELERY_TASK_ALWAYS_EAGER = True  # no broker; run tasks inline

CELERY_TASK_TRACK_STARTED = True

# --- CORS ---
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:3000"],
)

# --- Clerk auth (verify JWT via JWKS; Django does NOT issue) ---
CLERK_JWKS_URL = env("CLERK_JWKS_URL", default="")
CLERK_ISSUER = env("CLERK_ISSUER", default="")
CLERK_WEBHOOK_SECRET = env("CLERK_WEBHOOK_SECRET", default="")
CLERK_SECRET_KEY = env("CLERK_SECRET_KEY", default="")

# --- LLM / generation ---
GROQ_API_KEY = env("GROQ_API_KEY", default="")
GROQ_MODEL = env("GROQ_MODEL", default="llama-3.3-70b-versatile")
TOGETHER_AI_API_KEY = env("TOGETHER_AI_API_KEY", default="")

# --- Avatar generation ---
REPLICATE_API_KEY = env("REPLICATE_API_KEY", default="")
READYPLAYER_API_KEY = env("READYPLAYER_API_KEY", default="")

# --- Publishing ---
PORTFOLIO_WILDCARD_DOMAIN = env("PORTFOLIO_WILDCARD_DOMAIN", default="forge.app")

# --- Storage (Cloudflare R2, S3-compatible) ---
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID", default="")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY", default="")
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME", default="")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL", default="")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="auto")

# --- Free-tier limits (enforced in service layer; env-overridable for dev) ---
FREE_PLAN_MAX_PORTFOLIOS = env.int("FREE_PLAN_MAX_PORTFOLIOS", default=1)
FREE_PLAN_MAX_INTRO_CARDS = env.int("FREE_PLAN_MAX_INTRO_CARDS", default=1)
