# Structure of the NetBox Firmware Plugin

## Overview of folders and files

The plugin follows the standard NetBox plugin structure. Here is an overview of the most important components:

| File / Folder        | Function                                         |
|----------------------|--------------------------------------------------|
| `models`          | Definition of the data models (Firmware, Assignment) |
| `forms`           | Validation and logic for forms                    |
| `filters.py`         | Filters to limit lists                            |
| `views.py`           | Web views for CRUD operations and page display    |
| `urls.py`            | URL routing for plugin pages and API endpoints    |
| `api/`               | API viewsets and serializers                     |
| `tables`          | Configuration for tables in the UI                |
| `signal.py`          | Intermediate signals for operations that are not standard |
| `templates/`         | HTML templates, often inherited from NetBox itself|
| `static/`            | Static files (css, js) — usually not needed       |
| `migrations/`        | Database migrations                               |

## How do the components work together?

1. **Models** define the data and relationships.
2. **Forms** handle data input and validation.
3. **Views** display data in the UI and handle user actions.
4. **Filters and Tables** provide dynamic lists with search and filter options.
5. **URLs** link web addresses to views.
6. **API** provides access to data via REST, useful for automation.

## Additional notes

- The plugin makes extensive use of NetBox helpers (`utilities`, `extras`) to maintain consistency and simplicity.
- For extensions: stick to this structure for compatibility.
- When adding new models, always add migrations as well (`python manage.py makemigrations`).

---

## Links

- [NetBox Plugin Development](https://docs.netbox.dev/en/stable/plugins/development/)
- [Django Project Structure](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
