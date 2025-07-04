from netbox.plugins import PluginMenu, PluginMenuItem, PluginMenuButton, get_plugin_config

### Firmware ###

firmware_items = (
    PluginMenuItem(
        link='plugins:netbox_firmware:firmware_list',
        link_text='Firmwares',
        permissions=["netbox_firmware.view_firmware"],
        buttons= [
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
                permissions=["netbox_firmware.add_firmware"],
            ),
        ],
    ),
    PluginMenuItem(
        link='plugins:netbox_firmware:firmwareassignment_list',
        link_text='Firmware Assignments',
        permissions=["netbox_firmware.view_firmwareassignment"],
        buttons= [
            PluginMenuButton(
                link='plugins:netbox_firmware:firmwareassignment_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=["netbox_firmware.add_firmwareassignment"],
            ),
            PluginMenuButton(
                link='plugins:netbox_firmware:firmwareassignment_bulk_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=["netbox_firmware.add_firmwareassignment"],
            ),
        ],
    ),
)


### BIOS ###

bios_items = (
    PluginMenuItem(
        link='plugins:netbox_firmware:bios_list',
        link_text='BIOS',
        permissions=["netbox_firmware.view_bios"],
        buttons= [
            PluginMenuButton(
                link='plugins:netbox_firmware:bios_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=["netbox_firmware.add_bios"],
            ),
            PluginMenuButton(
                link='plugins:netbox_firmware:bios_bulk_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=["netbox_firmware.add_bios"],
            ),
        ],
    ),
    PluginMenuItem(
        link='plugins:netbox_firmware:biosassignment_list',
        link_text='BIOS Assignments',
        permissions=["netbox_firmware.view_biosassignment"],
        buttons= [
            PluginMenuButton(
                link='plugins:netbox_firmware:biosassignment_add',
                title='Add',
                icon_class='mdi mdi-plus-thick',
                permissions=["netbox_firmware.add_biosassignment"],
            ),
            PluginMenuButton(
                link='plugins:netbox_firmware:biosassignment_bulk_import',
                title='Import',
                icon_class='mdi mdi-upload',
                permissions=["netbox_firmware.add_biosassignment"],
            ),
        ],
    ),
)

### -> Add new Menu Items above this line if needed.

### Menu ###


if get_plugin_config('netbox_firmware', 'top_level_menu'):
    menu = PluginMenu(
        label=f'Firmwares',
        groups=(
            ('Firmware', firmware_items),
            ('BIOS', bios_items),
        ),
        icon_class = 'mdi mdi-clipboard-text-multiple-outline'
    )
else:
    menu_items = firmware_items + bios_items