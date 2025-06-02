# URL Routing in de NetBox Firmware Plugin

## Wat is URL routing?

Routing bepaalt welke URL naar welke view leidt. Dit zorgt dat de juiste pagina’s en API endpoints beschikbaar zijn.

## Locatie

De URL’s van deze plugin staan in `urls.py`.

## Belangrijkste routes

- `/plugins/firmware/firmwares/` — lijst en detail van firmware
- `/plugins/firmware/assignments/` — lijst en detail van toewijzingen

## Hoe werkt het?

De plugin gebruikt `get_model_urls()` van NetBox om standaard CRUD-pagina’s te genereren voor de modellen.

Daarnaast zijn er extra routes voor speciale acties of API calls.

## Voorbeeld uit `urls.py`:

```python
from utilities.urls import get_model_urls
from . import views

urlpatterns = [
    path('firmwares/', include(get_model_urls('firmware', 'firmware'))),
    path('assignments/', include(get_model_urls('firmware', 'firmwareassignment'))),
    # andere routes
]
´´´
