from django.conf import settings
from django.db.models import Q
from django.db.models import Count, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import pre_save

from django.urls import reverse
from django.utils.html import format_html, format_html_join
from django_tables2 import tables
from dcim.models import Device, Module, Rack
from netbox.plugins import get_plugin_config
from .choices import FirmwareStatusChoices

class FirmwareColumn(tables.Column):
    def render(self, value, record):
        # `record` is een Device instance
        assignments = record.FirmwareAssignment.all()
        if not assignments:
            return "-"
        links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse('plugins:netbox_firmware:firmwareassignment', args=[a.pk]),
                a.firmware
            )
            for a in assignments
        ]
        return format_html_join(", ", "{}", ((link,) for link in links))

class BiosColumn(tables.Column):
    def render(self, value, record):
        # `record` is een Device instance
        assignments = record.BiosAssignment.all()
        if not assignments:
            return "-"
        links = [
            format_html(
                '<a href="{}">{}</a>',
                reverse('plugins:netbox_firmware:biosassignment', args=[a.pk]),
                a.bios
            )
            for a in assignments
        ]
        return format_html_join(", ", "{}", ((link,) for link in links))

def get_prechange_field(obj, field_name):
    """Get value from obj._prechange_snapshot. If field is a relation,
    return object instance.
    """
    value = getattr(obj, '_prechange_snapshot', {}).get(field_name)
    if value is None:
        return None
    field = obj._meta.get_field(field_name)
    if field.is_relation:
        rel_obj = field.related_model.objects.filter(pk=value).first()
        if rel_obj:
            return rel_obj
        else:
            return None
    return value


def get_plugin_setting(setting_name):
    return get_plugin_config('netbox_firmware', setting_name)


def get_status_for(status):
    status_name = get_plugin_setting(status + '_status_name')
    if status_name is None:
        return None
    if status_name not in dict(FirmwareStatusChoices):
        raise ImproperlyConfigured(
            f'netbox_firmware plugin configuration defines status {status_name}, but it is not defined in FIELD_CHOICES["netbox_firmware.Firmware.status"]'
        )
    return status_name


def get_all_statuses_for(status):
    status_names = get_plugin_setting(status + '_additional_status_names')
    status_names = set(status_names)
    # add primary status
    if primary_status := get_status_for(status):
        status_names.add(primary_status)
    if len(status_names) < 1:
        return None
    if extra_statuses := status_names.difference(set(dict(FirmwareStatusChoices))):
        raise ImproperlyConfigured(
            f'netbox_firmware plugin configuration defines statuses {extra_statuses}, but these are not defined in FIELD_CHOICES["netbox_firmware.Firmware.status"]'
        )
    return list(status_names)


def get_tags_that_protect_firmware_from_deletion():
    """Return a list of tags that prevent an firmware from being deleted.

    Which tags prevent deletion is defined in the plugin configuration,
    under the key ``firmware_disable_deletion_for_tags``.

    Returns:
        list: list of tag slug strings
    """
    return get_plugin_setting('firmware_disable_deletion_for_tags')


def get_tags_and_edit_protected_firmware_fields():
    """Return a dict of tags and fields that prevent editing specified fields.

    Which tags prevent editing is defined in the plugin configuration,
    under the key ``firmware_disable_editing_fields_for_tags``.

    Structure of the dict is::

        {
            'tag_slug': ['field1', 'field2'],
            'tag_slug2': ['field1', 'field4'],
        }

    Returns:
        dict: dict of tag slug strings and list of field names
    """
    return get_plugin_setting('firmware_disable_editing_fields_for_tags')


def firmware_set_new_hw(firmware, hw):
    """
    Firmware was assigned to hardware (device/module/inventory item/rack) and we want to
    sync some field values from firmware to hardware
    Validation if firmware can be assigned to hw should be done before calling this function.
    """
    # device, module... needs None for blank firmware_tag to enforce uniqness at DB level
    new_firmware_tag = firmware.firmware_tag or None
    # device, module... does not allow serial to be null
    new_serial = firmware.serial or ''
    hw_save = False
    if hw.serial != new_serial:
        hw.serial = new_serial
        hw_save = True
    if hw.firmware_tag != new_firmware_tag:
        hw.firmware_tag = new_firmware_tag
        hw_save = True
    # handle changing of model (<kind>_type)
    if firmware.kind in ['device', 'module', 'rack']:
        firmware_type = getattr(firmware, firmware.kind+'_type')
        hw_type = getattr(hw, firmware.kind+'_type')
        if firmware_type != hw_type:
            setattr(hw, firmware.kind+'_type', firmware_type)
            hw_save = True
    if hw_save:
        hw.save()


def is_equal_none(a, b):
    """ Compare a and b as string. None is considered the same as empty string. """
    if a is None or b is None:
        return a == b or a == '' or b == ''
    return a == b


def query_located(queryset, field_name, values, firmwares_shown='all'):
    """
    Filters queryset on located values. Can filter for installed
    location/site and/or stored location/site for firmwares makred as stored.
    Args:
        * queryset - queryset of Firmware model
        * field_name - 'site' or 'location' or 'rack'
        * values - list of PKs of location types to filter on
        * firmwares_shown - 'all' or 'installed' or 'stored'
    """
    if field_name == 'rack':
        q_installed = Q(**{f'rack__in':values})
    else:
        q_installed = Q(**{f'rack__{field_name}__in':values})
    q_installed = (
        q_installed|
        Q(**{f'device__{field_name}__in':values})|
        Q(**{f'module__device__{field_name}__in':values})
    )

    # Q expressions for stored
    if field_name == 'rack':
        # storage in rack is not supported
        # generate Q() that matches none
        q_stored = Q(pk__in=[])
    elif field_name == 'location':
        q_stored = (
            Q(**{f'storage_location__in':values})&
            Q(status__in=get_all_statuses_for('stored'))
        )
    elif field_name == 'site':
        q_stored = (
            Q(**{f'storage_location__site__in':values})&
            Q(status__in=get_all_statuses_for('stored'))
        )

    if firmwares_shown == 'all':
        q = q_installed | q_stored
    elif firmwares_shown == 'installed':
        q = q_installed
    elif firmwares_shown == 'stored':
        q = q_stored
    else:
        raise Exception('unsupported')
    return queryset.filter(q)


def get_firmware_custom_fields_search_filters():
    """Returns a list of custom field filter strings that can be used in Q() filter.

    Custom fields and filters are used is defined in the plugin configuration,
    under the key ``firmware_custom_fields_search_filters``.

    Returns:
        list: list of custom field filter strings
    """
    custom_fields_filters = get_plugin_setting('firmware_custom_fields_search_filters')

    fields = []
    for field_name, filters in custom_fields_filters.items():
        for filter in filters:
            fields.append(f"custom_field_data__{field_name}__{filter}")
    return fields


def get_countdevice(model,modelfield,field):
    """
    Return a Subquery suitable for annotating a child object count.
    """
    subquery = Subquery(
        model.objects.filter(
            **{modelfield: OuterRef('pk')}
        ).order_by().values(
            modelfield
        ).annotate(
            c=Count(field)
        ).values('c')
    )

    return Coalesce(subquery, 0)
