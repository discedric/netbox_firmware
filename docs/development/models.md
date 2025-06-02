# 📦 Models: Firmware en FirmwareAssignment

Deze plugin bevat twee kernmodellen die de structuur vormen van de data-opslag:

---

## 📄 Firmware

Het `Firmware`-model definieert een unieke firmwareversie die je aan een device of module kan toewijzen.

### 🔑 Belangrijkste velden

| Veld           | Type                   | Uitleg                                          |
| -------------- | ---------------------- | ----------------------------------------------- |
| `name`         | CharField              | Naam van de firmwareversie                      |
| `description`  | TextField              | Uitleg over waarvoor de firmware dient          |
| `manufacturer` | ForeignKey             | De fabrikant van de firmware                    |
| `device_type`  | ForeignKey (optioneel) | Beperkt de firmware tot een bepaald toesteltype |
| `module_type`  | ForeignKey (optioneel) | Beperkt de firmware tot een bepaald moduletype  |
| `file`         | FileField (optioneel)  | Uploadbare bijlage zoals .bin of .pdf           |
| `status`       | CharField              | Keuze uit bijv. Concept, Actief, Verouderd      |

### 🧠 Validatie en filtering

* `device_type` en `module_type` zijn optioneel, maar helpen bij filtering.
* Firmware verschijnt enkel bij relevante types tijdens een assignment.

### 📎 Codevoorbeeld

```python
class Firmware(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='firmware/', blank=True, null=True)
    manufacturer = models.ForeignKey(
        to='dcim.Manufacturer',
        on_delete=models.PROTECT,
    )
    device_type = models.ForeignKey(...)
    module_type = models.ForeignKey(...)
    status = models.CharField(...)
```

---

## 🔗 FirmwareAssignment

Het `FirmwareAssignment`-model verbindt een `Firmware` aan een `Device` of `Module`.

### 🔑 Velden

| Veld            | Type                   | Uitleg                                |
| --------------- | ---------------------- | ------------------------------------- |
| `firmware`      | ForeignKey             | Verwijst naar een Firmware            |
| `device`        | ForeignKey (optioneel) | Waar de firmware is toegepast         |
| `module`        | ForeignKey (optioneel) | Alternatief voor device               |
| `patch_date`    | DateField              | Datum waarop de firmware is toegepast |
| `ticket_number` | CharField              | Interne referentie                    |
| `comment`       | TextField              | Extra uitleg                          |

### ⚖️ Validatie

De `clean()` methode zorgt ervoor dat je niet tegelijk een module én een device kan invullen.

```python
def clean(self):
    if self.device and self.module:
        raise ValidationError("Je mag slechts één van device/module invullen.")
    if not self.device and not self.module:
        raise ValidationError("Je moet minstens device of module invullen.")
```

---

## 📚 Meer info

* [Django Models](https://docs.djangoproject.com/en/stable/topics/db/models/)
* [NetBox Plugin Models](https://docs.netbox.dev/en/stable/plugins/models/)

⬅️ [Terug naar overzicht](./index.md)
