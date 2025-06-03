# Debugging the NetBox Firmware Plugin

## Common issues

### 1. Plugin does not appear in the UI

- Check if the plugin is added to `configuration.py` in `PLUGINS`.
- Check logs for errors during startup.
- Check if the URL routes are correct.

### 2. Database errors or missing migrations

- Always run after changes in `models.py`:

```bash
python manage.py makemigrations netbox_firmware
python manage.py migrate
python manage.py reindex
```

Check for duplicate migrations or conflicts.

### 3. API endpoints do not work or give errors

- Check if the serializers are registered correctly.
- Test with Postman or the NetBox browsable API.
- Check the logs for any errors.

### 4. Errors with assigned_object_type or NoneType

- This is often because a ForeignKey is not filled in correctly.
- Add debug prints in clean() or serializers to check which values are received.
- Set DEBUG = True in NetBox config for detailed error messages.

### Debugging tips

Use the Django shell to inspect models:

```bash
python manage.py shell
>>> from netbox_firmware.models import Firmware, FirmwareAssignment
>>> Firmware.objects.all()
```

- Logs are often in the default NetBox log files (/opt/netbox/netbox.log or similar).

- Temporarily add print() statements in your code to check values.
