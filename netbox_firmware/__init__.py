import os
from netbox.plugins import PluginConfig
from django.conf import settings
from django.urls import include, path
from .version import __version__

class FirmwareManagerConfig(PluginConfig):
    name = 'netbox_firmware'
    verbose_name = 'Netbox Firmware'
    version = __version__
    description = 'Firmware management in NetBox'
    author = 'Cedric Vaneessen'
    author_email = 'cedric.vaneessen@zabun.be'
    base_url = 'firmware'
    min_version = '4.2.0'
    default_settings = {
        'top_level_menu': True,
    }

    def ready(self):
        firmware_dir = os.path.join(settings.MEDIA_ROOT, 'firmware-files')
        if not os.path.exists(firmware_dir):
            os.makedirs(firmware_dir)
        super().ready()
        from . import signals

config = FirmwareManagerConfig