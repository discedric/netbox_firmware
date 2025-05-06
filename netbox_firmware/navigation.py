from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

firmware_buttons = [
    PluginMenuButton(
        link='plugins:netbox_firmware:firmware_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["netbox_firmware.add_firmware"],
    ),
    PluginMenuButton(
        link='plugins:netbox_firmware:firmware_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["netbox_firmware.import_firmware"],
    ),
]
firmware_assignments_buttons = [
    PluginMenuButton(
        link='plugins:netbox_firmware:firmwareassignment_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        permissions=["netbox_firmware.add_firmware_assignment"],
    ),
    PluginMenuButton(
        link='plugins:netbox_firmware:firmwareassignment_bulk_import',
        title='Import',
        icon_class='mdi mdi-upload',
        permissions=["netbox_firmware.aimport_firmware_assignment"],
    ),
]
firmware_items = (
    PluginMenuItem(
        link='plugins:netbox_firmware:firmware_list',
        link_text='Firmwares',
        permissions=["netbox_firmware.view_firmware"],
        buttons= firmware_buttons,
    ),
    PluginMenuItem(
        link='plugins:netbox_firmware:firmwareassignment_list',
        link_text='Firmware Assignments',
        permissions=["netbox_firmware.view_firmware_assignment"],
        buttons= firmware_assignments_buttons,
    ),
)

if get_plugin_config('netbox_firmware', 'top_level_menu'):
    menu = PluginMenu(
        label=f'Firmwares',
        groups=(
            ('Firmware', firmware_items),
        ),
        icon_class = 'mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = firmware_items