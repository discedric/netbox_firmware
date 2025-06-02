# Structuur van de NetBox Firmware Plugin

## Overzicht mappen en bestanden

De plugin volgt de standaard NetBox plugin-structuur. Hier een overzicht van de belangrijkste onderdelen:

| Bestand / Map         | Functie                                           |
|----------------------|--------------------------------------------------|
| `models.py`          | Definitie van de data modellen (Firmware, Assignment) |
| `forms.py`           | Validatie en logica voor formulieren              |
| `filters.py`         | Filters om lijsten te beperken                     |
| `views.py`           | Webviews voor CRUD operaties en paginaweergave    |
| `urls.py`            | URL routing voor pluginpagina’s en API endpoints  |
| `api/`               | API viewsets en serializers                        |
| `tables.py`          | Configuratie voor tabellen in de UI                |
| `signal.py`          | Tussensignalen voor bewerkingen die niet standaar gebeuren                          |
| `templates/`         | HTML templates, vaak overgenomen van NetBox zelf  |
| `static/`            | Statische bestanden (css, js) — meestal niet nodig |
| `migrations/`        | Database migraties                                  |

## Hoe werken de onderdelen samen?

1. **Modellen** definiëren de data en relaties.
2. **Forms** zorgen voor invoer van data en validatie.
3. **Views** tonen data in de UI en handelen gebruikersacties af.
4. **Filters en Tables** geven dynamische lijsten met zoek- en filteropties.
5. **URLs** koppelen webadressen aan views.
6. **API** biedt toegang tot data via REST, bruikbaar voor automatisering.

## Extra aandachtspunten

- De plugin maakt veel gebruik van NetBox helpers (`utilities`, `extras`) om consistentie en eenvoud te bewaren.
- Voor uitbreidingen: houd je aan deze structuur voor compatibiliteit.
- Voeg bij nieuwe modellen ook altijd migraties toe (`python manage.py makemigrations`).

---

## Links

- [NetBox Plugin Development](https://docs.netbox.dev/en/stable/plugins/development/)
- [Django Project Structure](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
