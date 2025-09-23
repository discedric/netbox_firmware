import os
from netbox.plugins import PluginConfig
from django.conf import settings
from .version import __version__

class NetboxFirmwareConfig(PluginConfig):
    name = 'netbox_firmware'
    verbose_name = 'Netbox Firmware'
    version = __version__
    description = 'Firmware management in NetBox'
    author = 'Bart Van der Biest'
    author_email = 'bart@zimmo.be'
    base_url = 'firmware'
    min_version = '4.3.0'
    default_settings = {
        'top_level_menu': True,
    }

    def ready(self):
        firmware_dir = os.path.join(settings.MEDIA_ROOT, 'firmware-files')
        if not os.path.exists(firmware_dir):
            os.makedirs(firmware_dir)
        super().ready()
        from . import signals

config = NetboxFirmwareConfig