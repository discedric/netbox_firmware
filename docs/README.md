# Firmware Management Plugin Documentation

## Firmware Management Plugin Documentation

### Overview
The Firmware Management plugin for NetBox provides tools for managing firmware and BIOS assignments across devices, modules, and inventory items. It includes features for tracking firmware versions, assigning firmware, and managing lifecycle statuses.

### Features
- Manage firmware and BIOS files.
- Assign firmware to devices, modules, and inventory items.
- Track firmware lifecycle statuses (e.g., Active, Deprecated, Beta, Archived).
- Bulk import and edit firmware and assignments.
- Integration with NetBox's filtering and search capabilities.
- GraphQL and REST API support for automation.

### Documentation Structure

The documentation for the Firmware Management plugin is organized into the following sections:

- **API**: Details about REST and GraphQL APIs.
- **Forms**: Information about form classes for firmware and BIOS objects.
- **Models**: Details about the database schema for firmware and BIOS objects.
- **Tables**: Definitions for displaying firmware and BIOS data in tabular format.
- **Templates**: HTML templates for rendering firmware and BIOS-related views.
- **Views**: View classes for CRUD operations and custom views.
- **Navigation**: Menu items and navigation buttons for firmware features.
- **URLs**: URL patterns for routing firmware-related endpoints.
- **Utils**: Utility functions and helpers for the plugin.
- **Template Content**: Reusable template extensions and components.

Each section is documented in its respective folder or file for clarity and ease of navigation.

## Installation

1. Clone the repository into the NetBox plugins directory:
   ```bash
   git clone <repository-url> /opt/netbox/netbox/netbox/plugins/firmware_management
   ```

2. Add the plugin to the `PLUGINS` configuration in `netbox/configuration.py`:
   ```python
   PLUGINS = [
       'firmware_management',
   ]
   
   PLUGINS_CONFIG = {
       'firmware_management': {
           'top_level_menu': True,
           'used_status_name': 'used',
           'used_additional_status_names': [],
           'asset_warranty_expire_warning_days': 90,
       },
   }
   ```

3. Install the required dependencies:
   ```bash
   pip install -r /opt/netbox/netbox/netbox/plugins/firmware_management/requirements.txt
   ```

4. Run database migrations:
   ```bash
   python3 manage.py migrate
   ```

5. Restart the NetBox service:
   ```bash
   sudo systemctl restart netbox
   ```

## Usage

### Managing Firmware
1. Navigate to the **Firmwares** section in the NetBox UI.
2. Add a new firmware by providing details such as name, file, status, and associated hardware type.
3. Use the filtering options to search for specific firmware.

### Assigning Firmware
1. Navigate to the **Firmware Assignments** section.
2. Assign firmware to devices, modules, or inventory items.
3. Track patch dates, ticket numbers, and comments for each assignment.

### Bulk Operations
- Use the **Bulk Import** feature to upload multiple firmware or assignments via CSV files.
- Use the **Bulk Edit** feature to update multiple records simultaneously.

## API Reference

### REST API
- **Firmware**: `/api/plugins/firmware_management/firmware/`
- **Firmware Assignments**: `/api/plugins/firmware_management/firmwareassignment/`

### GraphQL
- Query firmware and assignments using the GraphQL endpoint:
  ```graphql
  query {
      firmware {
          id
          name
          status
      }
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

## Development

### Running Tests
Run the following command to execute tests:
```bash
python3 manage.py test firmware_management
```

### Contributing
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed descriptions of your changes.

### Forms
The `forms` module contains form classes for creating, editing, and bulk operations on firmware and BIOS objects. It includes forms for reassigning firmware, importing data, and filtering objects.

### Models
The `models` module defines the database schema for firmware and BIOS objects, including their relationships with hardware types like devices, modules, and inventory items.

### Tables
The `tables` module provides table definitions for displaying firmware and BIOS data in tabular format within the NetBox UI.

### Templates
The `templates` directory contains HTML templates for rendering firmware and BIOS-related views, including forms, lists, and detail pages.

### Views
The `views` module contains view classes for handling CRUD operations, bulk actions, and custom views for firmware and BIOS objects.

### Navigation
The `navigation` module defines menu items and navigation buttons for accessing firmware and BIOS-related features in the NetBox UI.

### URLs
The `urls` module maps URL patterns to views, enabling routing for firmware and BIOS-related endpoints.

### Utils
The `utils` module contains utility functions and helpers used across the plugin, such as tag management and data validation.

### Template Content
The `template_content` module provides reusable template extensions and components for rendering firmware-related information in the NetBox UI.

## License
This plugin is licensed under the MIT License. See the LICENSE file for details.