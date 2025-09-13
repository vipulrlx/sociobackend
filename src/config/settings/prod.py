from .base import *       # noqa
DEBUG = False
ALLOWED_HOSTS = ["api.example.com"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
SECURE_HSTS_SECONDS = 31536000
