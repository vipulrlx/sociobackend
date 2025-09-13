# App Settings

A Django app for managing global application settings with unlimited media items and a read-only API.

## Features

- **Singleton Settings**: AppSettings model that always has exactly one row (pk=1)
- **Unlimited Media**: AppMedia model with support for MP4 files and YouTube URLs
- **Admin Interface**: Custom admin with inline media management
- **Read-only API**: REST API endpoint at `/api/app-settings/`
- **Validation**: Proper validation for media types (MP4 requires file, YouTube requires URL)

## Models

### AppSettings
- `name` (CharField, max_length=200)
- `description` (TextField, blank=True)
- `logo` (ImageField, upload_to="settings/logo/", blank=True, null=True)
- `terms` (TextField, blank=True)
- `updated_at` (DateTimeField, auto_now=True)

### AppMedia
- `app_settings` (ForeignKey to AppSettings, related_name='media')
- `kind` (CharField, choices: 'MP4' or 'YOUTUBE')
- `title` (CharField, max_length=255, blank=True)
- `file` (FileField, upload_to="settings/videos/", blank=True, null=True)
- `url` (URLField, blank=True, null=True)
- `order` (PositiveIntegerField, default=0)
- `is_active` (BooleanField, default=True)
- `created_at` (DateTimeField, auto_now_add=True)

## API

### Endpoint
`GET /api/app-settings/`

### Response Format
```json
{
  "name": "ISTI",
  "description": "App description",
  "logo": "http://example.com/media/settings/logo/logo.png",
  "terms": "Terms and conditions",
  "updated_at": "2024-01-01T12:00:00Z",
  "media": [
    {
      "id": 1,
      "kind": "MP4",
      "title": "Introduction Video",
      "file": "http://example.com/media/settings/videos/intro.mp4",
      "url": null,
      "order": 0,
      "is_active": true
    },
    {
      "id": 2,
      "kind": "YOUTUBE",
      "title": "Tutorial Video",
      "file": null,
      "url": "https://youtube.com/watch?v=example",
      "order": 1,
      "is_active": true
    }
  ]
}
```

## Usage

### Getting Settings
```python
from app_settings.models import AppSettings

# Get the singleton settings instance
settings = AppSettings.get_solo()
```

### Adding Media
```python
from app_settings.models import AppSettings, AppMedia

settings = AppSettings.get_solo()

# Add MP4 media
mp4_media = AppMedia.objects.create(
    app_settings=settings,
    kind='MP4',
    title='My Video',
    file='path/to/video.mp4'
)

# Add YouTube media
youtube_media = AppMedia.objects.create(
    app_settings=settings,
    kind='YOUTUBE',
    title='YouTube Video',
    url='https://youtube.com/watch?v=example'
)
```

## Validation Rules

- **MP4 Media**: Must have a file, URL must be empty
- **YouTube Media**: Must have a URL, file must be empty
- **Settings**: Only one instance can exist (pk=1)

## Admin Interface

The admin interface provides:
- AppSettings management with inline media editing
- AppMedia list view with filtering and search
- Validation enforcement through the admin interface 