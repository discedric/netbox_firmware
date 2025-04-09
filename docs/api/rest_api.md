# REST API Documentation

The REST API provides endpoints for managing firmware and assignments programmatically. Below is a detailed explanation of the available endpoints.

## Endpoints

### Firmware
- **Endpoint**: `/api/plugins/firmware_management/firmware/`
- **Methods**: GET, POST, PUT, PATCH, DELETE
- **Description**: Manage firmware objects.

#### Example Request
```bash
curl -X GET "http://<netbox-url>/api/plugins/firmware_management/firmware/" \
     -H "Authorization: Token <your-token>"
```

#### Example Response
```json
[
  {
    "id": 1,
    "name": "Firmware v1.0",
    "status": "active",
    "manufacturer": "Example Manufacturer"
  }
]
```

### Firmware Assignments
- **Endpoint**: `/api/plugins/firmware_management/firmwareassignment/`
- **Methods**: GET, POST, PUT, PATCH, DELETE
- **Description**: Manage firmware assignments to devices, modules, or inventory items.

#### Example Request
```bash
curl -X POST "http://<netbox-url>/api/plugins/firmware_management/firmwareassignment/" \
     -H "Authorization: Token <your-token>" \
     -H "Content-Type: application/json" \
     -d '{"firmware": 1, "device": 2}'
```

#### Example Response
```json
{
  "id": 1,
  "firmware": "Firmware v1.0",
  "device": "Device A"
}
```

## Authentication
All API requests require an API token for authentication. Include the token in the `Authorization` header as follows:
```
Authorization: Token <your-token>
```