# Filters in de NetBox Firmware Plugin

## Wat zijn filters?

Filters zorgen ervoor dat je lijsten in de UI kan beperken tot de records die je interessant vindt. In deze plugin kan je bijvoorbeeld filteren op fabrikant, status van firmware of type device/module.

## Waar vind je de filters?

Filters worden gebruikt in de lijsten van:

- Firmware (lijst van firmwareversies)
- FirmwareAssignments (toewijzingen)

Deze vind je onder `Plugins > Firmware` in NetBox.

## Hoe zijn filters geïmplementeerd?

De filters staan in `filters.py` in de pluginfolder.

### Voorbeeld van een filterclass:

```python
class FirmwareFilterSet(NetBoxModelFilterSet):
    manufacturer_id = django_filters.ModelMultipleChoiceFilter(
        field_name='manufacturer',
        queryset=Manufacturer.objects.all(),
        label='Fabrikant',
    )
    status = django_filters.MultipleChoiceFilter(
        choices=StatusChoices,
        label='Status',
    )
