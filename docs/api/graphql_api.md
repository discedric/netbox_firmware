# GraphQL API Documentation

The GraphQL API provides a flexible way to query and mutate data related to firmware and assignments. Below is a detailed explanation of the available queries and mutations.

## Queries

### Firmware
- **Query**: Retrieve firmware details.

#### Example Query
```graphql
query {
  firmware {
    id
    name
    status
    manufacturer {
      name
    }
  }
}
```

#### Example Response
```json
{
  "data": {
    "firmware": [
      {
        "id": 1,
        "name": "Firmware v1.0",
        "status": "active",
        "manufacturer": {
          "name": "Example Manufacturer"
        }
      }
    ]
  }
}
```

### Firmware Assignments
- **Query**: Retrieve firmware assignment details.

#### Example Query
```graphql
query {
  firmwareAssignment {
    id
    firmware {
      name
    }
    device {
      name
    }
  }
}
```

#### Example Response
```json
{
  "data": {
    "firmwareAssignment": [
      {
        "id": 1,
        "firmware": {
          "name": "Firmware v1.0"
        },
        "device": {
          "name": "Device A"
        }
      }
    ]
  }
}
```

## Mutations

### Create Firmware
- **Mutation**: Add a new firmware object.

#### Example Mutation
```graphql
mutation {
  createFirmware(input: {
    name: "Firmware v2.0",
    status: "active",
    manufacturer: 1
  }) {
    firmware {
      id
      name
    }
  }
}
```

#### Example Response
```json
{
  "data": {
    "createFirmware": {
      "firmware": {
        "id": 2,
        "name": "Firmware v2.0"
      }
    }
  }
}
```