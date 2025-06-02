# Debugging van de NetBox Firmware Plugin

## Veelvoorkomende problemen

### 1. Plugin verschijnt niet in de UI

- Controleer of de plugin is toegevoegd aan `configuration.py` in `PLUGINS`.
- Controleer logs of er fouten zijn tijdens opstart.
- Controleer of de URL routes correct zijn.

### 2. Database fouten of migraties ontbreken

- Draai altijd na wijzigingen in `models.py`:

```bash
python manage.py makemigrations netbox_firmware
python manage.py migrate
python manage.py reindex
```

Check of er dubbele migraties of conflicten zijn.

### 3. API endpoints werken niet of geven errors

- Controleer of de serializers correct zijn geregistreerd.
- Test met Postman of de NetBox browsable API.
- Kijk in de logs welke errors er worden gelogd.

### 4. Foutmeldingen met assigned_object_type of NoneType

- Vaak komt dit doordat een ForeignKey niet correct gevuld is.
- Voeg debug prints toe in clean() of serializers om te checken welke waarden er binnenkomen.
- Zet DEBUG = True in NetBox config voor uitgebreide foutmeldingen.

### Debuggen tips

Gebruik de Django shell om models te inspecteren:

```bash
python manage.py shell
>>> from netbox_firmware.models import Firmware, FirmwareAssignment
>>> Firmware.objects.all()
```

- Logs staan vaak in de standaard NetBox logbestanden (/opt/netbox/netbox.log of vergelijkbaar).

- Voeg tijdelijk print() statements toe in je code om waarden te checken.
