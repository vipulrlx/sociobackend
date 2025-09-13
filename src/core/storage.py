from datetime import timedelta
from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings
from google.cloud import storage as gcs

class PrivateMediaStorage(GoogleCloudStorage):
    """GCS backend that returns short-lived signed URLs (bucket stays private)."""
    def url(self, name):
        client = gcs.Client(
            project=getattr(settings, "GS_PROJECT_ID", None),
            credentials=settings.STORAGES["default"]["OPTIONS"]["credentials"],
        )
        bucket = client.bucket(self.bucket_name)
        # name is relative to self.location (e.g., "docs/file.pdf")
        path = f"{self.location.rstrip('/')}/{name.lstrip('/')}" if self.location else name
        ttl = int(getattr(settings, "MEDIA_SIGNED_URL_TTL_MINUTES", 15))
        return bucket.blob(path).generate_signed_url(
            version="v4",
            expiration=timedelta(minutes=ttl),
            method="GET",
        )
