"""Test settings: in-memory SQLite, LocMem cache, eager Celery. Fast + isolated."""
from .settings import *  # noqa: F401,F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CACHES = {
    "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
}

CELERY_TASK_ALWAYS_EAGER = True

# Throttling off in tests (avoid 429 noise); re-enable per-test if needed.
REST_FRAMEWORK["DEFAULT_THROTTLE_CLASSES"] = []  # noqa: F405
