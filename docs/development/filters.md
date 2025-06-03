# Filters in the NetBox Firmware Plugin

## What are filters?

Filters allow you to limit lists in the UI to the records you are interested in. In this plugin, you can filter by manufacturer, firmware status, or device/module type.

## Where can you find the filters?

Filters are used in the lists of:

- Firmware (list of firmware versions)
- FirmwareAssignments (assignments)

You can find these under `Plugins > Firmware` in NetBox.

## How are filters implemented?

The filters are defined in `filters.py` in the plugin folder.

### Example of a filter class:

```python
class FirmwareFilterSet(NetBoxModelFilterSet):
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label='Manufacturer',
    )
    status = django_filters.MultipleChoiceFilter(
        choices=StatusChoices,
        label='Status',
    )