from .base import *  # noqa


DEBUG = False

STATIC_ROOT = BASE_DIR / "static"

# CORS

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = ["*"]