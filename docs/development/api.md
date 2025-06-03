
# 🌐 API Integration

The plugin uses Django REST Framework to automatically provide API endpoints. This makes firmware and assignments easily accessible via scripts or external tools.

---


## 🔗 Available endpoints

After installation, 2 main endpoints are available:

| Endpoint                             | Purpose                               |
| ------------------------------------ | ------------------------------------- |
| `/api/plugins/firmware/firmwares/`   | Manage firmware objects               |
| `/api/plugins/firmware/assignments/` | Manage assignments                    |

You can:

- Retrieve data (GET)
- Add new entries (POST)
- Make changes (PUT/PATCH)
- Delete items (DELETE)

---


## 🔐 Authentication

The API uses the same token authentication as NetBox itself:

```bash
curl -H "Authorization: Token <your_token>" https://netbox.local/api/plugins/firmware/firmwares/
```

---


## 🧰 Examples

### 🔍 Example: retrieve list of firmwares

```bash
http GET https://netbox.local/api/plugins/firmware/firmwares/ "Authorization: Token <token>"
```

### ➕ Example: create new firmware

```json
POST /api/plugins/firmware/firmwares/
{
  "name": "HP iLO 2.77",
  "status": "active",
  "manufacturer": 2
}
```

### 🛠️ Example: assign firmware

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


## 📦 Technical structure

The API is defined in these files:

| File                 | Role                                     |
| -------------------- | ---------------------------------------- |
| `api/serializers.py` | Converts models to JSON format           |
| `api/viewsets.py`    | Defines how querysets are processed      |
| `api/urls.py`        | Links URLs to viewsets                   |

The viewsets inherit from NetBox’s `NetBoxModelViewSet`, so filtering, browsable API, and permissions work automatically.

---


## 🔗 Resources

- [DRF](https://www.django-rest-framework.org/)
- [NetBox API](https://docs.netbox.dev/en/stable/api/)

⬅️ [Back to overview](./index.md)
