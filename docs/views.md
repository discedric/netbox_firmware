# Views Documentation

The `views` module contains view classes for handling CRUD operations, bulk actions, and custom views for firmware and BIOS objects. These views define the logic for interacting with the plugin's data.

## Key Views

### FirmwareView
- **Purpose**: Displays details of a firmware object.
- **Type**: `ObjectView`

### FirmwareListView
- **Purpose**: Displays a list of firmware objects.
- **Type**: `ObjectListView`
- **Features**: Supports filtering and sorting.

### FirmwareAssignmentEditView
- **Purpose**: Handles creating and editing firmware assignments.
- **Type**: `ObjectEditView`

### Bulk Views
- **Examples**: `FirmwareBulkImportView`, `FirmwareAssignmentBulkEditView`
- **Purpose**: Handle bulk operations like importing, editing, and deleting records.

## Usage
These views are registered with URL patterns and linked to templates to provide a complete user interface for managing firmware and assignments.