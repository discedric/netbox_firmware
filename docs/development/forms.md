# Forms en Validatie in de NetBox Firmware Plugin

## Waarom forms?

Forms worden gebruikt om invoer van gebruikers te valideren en te structureren, bv. bij het toevoegen of aanpassen van firmware of assignments.

## Locatie

De forms staan in `forms.py`.

## Belangrijkste functionaliteiten

- Validatie via `clean()` methodes
- Dynamische keuzevelden afhankelijk van device_type/module_type
- Custom widgets voor betere UX

## Voorbeeld validatie in `FirmwareAssignmentForm`:

```python
def clean(self):
    cleaned_data = super().clean()
    device = cleaned_data.get("device")
    module = cleaned_data.get("module")
    if device and module:
        raise ValidationError("Je mag slechts één van device of module invullen.")
    if not device and not module:
        raise ValidationError("Je moet een device of module invullen.")
    return cleaned_data
´´´
