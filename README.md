# Netbox Firmware Plugin

A [Netbox](https://github.com/netbox-community/netbox) plugin for tracking the firmware of devices.
This plugin was developed by a student during an internship, so temporary updates may occur during the duration of this internship.

## Features

A plugin for tracking the firmware versions installed on your devices and modules.
This is a simple plugin that lays the foundation for custom extensions.

## Compatibility
| Netbox Version | Plugin Version |
|----------------|----------------|
|       4.2      |      1.0.0     |

## Installing

Official installation instructions: [official Netbox plugin documentation](https://docs.netbox.dev/en/stable/plugins/#installing-plugins)

You can install the plugin via the GitHub CLI or Git:
```bash
$ source /opt/netbox/venv/bin/activate
(venv) $ cd /opt/netbox/netbox/netbox/plugins
(venv) $ gh repo clone discedric/netbox_firmware
(venv) $ pip install ./netbox_firmware
```

```python
PLUGINS = [
    'netbox_firmware'
]
```

You will also need to update the database migrations and Netbox search index:

```bash
(venv) $ cd /opt/netbox/netbox/
(venv) $ python3 manage.py migrate
(venv) $ python3 manage.py reindex --lazy
```