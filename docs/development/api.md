# 🌐 API-integratie

De plugin maakt gebruik van de Django REST Framework om automatisch API-endpoints aan te bieden. Hierdoor zijn firmware en toewijzingen makkelijk bruikbaar via scripts of externe tools.

---

## 🔗 Beschikbare endpoints

Na installatie zijn er 2 hoofdendpoints beschikbaar:

| Endpoint                             | Doel                                  |
| ------------------------------------ | ------------------------------------- |
| `/api/plugins/firmware/firmwares/`   | Beheer van firmware-objecten          |
| `/api/plugins/firmware/assignments/` | Beheer van toewijzingen (assignments) |

Je kan:

* Gegevens opvragen (GET)
* Nieuwe entries toevoegen (POST)
* Wijzigingen aanbrengen (PUT/PATCH)
* Items verwijderen (DELETE)

---

## 🔐 Authenticatie

De API gebruikt dezelfde token-authenticatie als NetBox zelf:

```bash
curl -H "Authorization: Token <your_token>" https://netbox.local/api/plugins/firmware/firmwares/
```

---

## 🧰 Voorbeelden

### 🔍 Voorbeeld: lijst van firmwares ophalen

```bash
http GET https://netbox.local/api/plugins/firmware/firmwares/ "Authorization: Token <token>"
```

### ➕ Voorbeeld: nieuwe firmware aanmaken

```json
POST /api/plugins/firmware/firmwares/
{
  "name": "HP iLO 2.77",
  "status": "active",
  "manufacturer": 2
}
```

### 🛠️ Voorbeeld: firmware toewijzen

```json
POST /api/plugins/firmware/assignments/
{
  "firmware": 1,
  "device": 5,
  "patch_date": "2024-11-13",
  "ticket_number": "CHG12345"
}
```

---

## 📦 Technische structuur

De API is gedefinieerd in deze bestanden:

| Bestand              | Rol                                      |
| -------------------- | ---------------------------------------- |
| `api/serializers.py` | Zet modellen om naar JSON-formaat        |
| `api/viewsets.py`    | Definieert hoe querysets verwerkt worden |
| `api/urls.py`        | Koppelt URL’s aan viewsets               |

De viewsets erven van NetBox’ `NetBoxModelViewSet`, zodat filtering, browsable API en permissies automatisch meewerken.

---

## 🔗 Bronnen

* [DRF](https://www.django-rest-framework.org/)
* [NetBox API](https://docs.netbox.dev/en/stable/api/)

⬅️ [Terug naar overzicht](./index.md)
