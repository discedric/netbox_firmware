# 🖼️ Views en Templates

De plugin maakt gebruik van de NetBox UI-helpers en standaard `ViewSet`-structuren om alle gegevens correct te tonen. Er is geen aangepaste HTML of JavaScript geschreven — alles is gebaseerd op bestaande NetBox-componenten.

---

## 🧭 Navigatiestructuur

Na installatie verschijnen twee menu-items:

* **Firmware**: toont een lijst van alle firmwareversies
* **Firmware Assignments**: lijst met alle firmwaretoewijzingen

Elk item leidt naar een standaardlijstweergave (list view) en detailpagina (detail view).

---

## 🔁 Overzicht views

| View                         | Type       | Beschrijving                |
| ---------------------------- | ---------- | --------------------------- |
| `FirmwareListView`           | ListView   | Lijst met filters bovenaan  |
| `FirmwareView`               | DetailView | Detailpagina met tabellen   |
| `FirmwareAssignmentListView` | ListView   | Lijst van toewijzingen      |
| `FirmwareAssignmentView`     | DetailView | Detailpagina per toewijzing |

Deze views gebruiken NetBox’s `GenericUIViewSet` met automatisch gegenereerde tabellen en breadcrumbs.

---

## 📂 Templates

De templates worden gegenereerd op basis van de modelstructuur en `NetBoxModelViewSet`. Hierdoor is manuele aanpassing meestal overbodig.

Als je een template wil overschrijven, kan je dat doen via:

```plaintext
<plugin_name>/templates/<app_label>/<model>_*.html
```

Voorbeeld:

```plaintext
firmware/templates/firmware/firmware_list.html
```

Maar in deze plugin is dat **niet** gedaan.

---

## 🧩 Extra functies

De plugin bevat een kleine uitbreiding via `get_extra_actions()`:

* De knop "Assign firmware" op een device detailpagina leidt naar een formulier dat vooraf is ingevuld met dat device.
* Dit is geïmplementeerd via een aangepaste URL en view die `CreateView` overerft en contextuele initialisatie uitvoert.

Voorbeeld:

```python
class AssignFirmwareToDeviceView(CreateView):
    def get_initial(self):
        return {'device': self.kwargs['device_pk']}
```

---

## 📚 Bronnen

* [NetBox plugins: Views](https://docs.netbox.dev/en/stable/plugins/views/)
* [Django Generic Views](https://docs.djangoproject.com/en/stable/ref/class-based-views/)

⬅️ [Terug naar overzicht](./index.md)
