import logging
import os
from django.db.models.signals import post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver

from firmware_management.models import *

@receiver(pre_save, sender=Bios)
@receiver(pre_save, sender=Firmware)
def delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        # Nieuw object, geen bestand om te verwijderen
        return

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return
    print("old_instance", old_instance)
    old_file = old_instance.file  # jouw file field
    new_file = instance.file

    if not old_file:
        return

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)