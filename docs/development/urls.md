# URL Routing in the NetBox Firmware Plugin

## What is URL routing?

Routing determines which URL leads to which view. This ensures that the correct pages and API endpoints are available.

## Location

The URLs of this plugin are in `urls.py`.

## Main routes

- `/plugins/firmware/firmwares/` — list and detail of firmware
- `/plugins/firmware/assignments/` — list and detail of assignments

## How does it work?

The plugin uses NetBox's `get_model_urls()` to generate standard CRUD pages for the models.

In addition, there are extra routes for special actions or API calls.

## Example from `urls.py`:

```python
from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    path('firmwares/', include(get_model_urls('firmware', 'firmware'))),
    path('assignments/', include(get_model_urls('firmware', 'firmwareassignment'))),
    # other routes
]
```
