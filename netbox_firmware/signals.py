import logging
import os
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver

from netbox_firmware.models import *

### This is needed to delete the file from the storage when the Firmware or BIOS object is deleted or the file is changed. ###
@receiver(pre_save, sender=Bios)
@receiver(pre_save, sender=Firmware)
def delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    old_file = old_instance.file
    new_file = instance.file

    if not old_file:
        return

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)