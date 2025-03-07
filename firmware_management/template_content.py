from django.template import Template
from netbox.plugins import PluginTemplateExtension

from .models import Firmware
from .utils import query_located


WARRANTY_PROGRESSBAR = '''
{% with record.warranty_progress as wp %}
{% with record.warranty_remaining as wr %}
{% with settings.PLUGINS_CONFIG.netbox_inventory.firmware_warranty_expire_warning_days as wthresh %}

{% if wp is None and wr.days <= 0 %}
  <div class="progress" role="progressbar">
    <div class="progress-bar progress-bar-striped text-bg-danger" style="width:100%;">
      Expired {{ record.warranty_end|timesince|split:','|first }} ago
    </div>
  </div>
{% elif wp is None and wr.days > 0 %}
  <div class="progress" role="progressbar">
    <div class="progress-bar progress-bar-striped text-bg-{% if wthresh and wr.days < wthresh %}warning{% else %}success{% endif %}" style="width:100%;">
      {{ record.warranty_end|timeuntil|split:','|first }}
    </div>
  </div>
{% elif wp is None %}
    {{ ""|placeholder }}
{% else %}

<div
  class="progress"
  role="progressbar"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuenow="{% if wp < 0 %}0{% else %}{{ wp }}{% endif %}"
>
  <div
    class="progress-bar text-bg-{% if wp >= 100 %}danger{% elif wthresh and wr.days < wthresh %}warning{% else %}success{% endif %}"
    style="width: {% if wp < 0 %}0%{% else %}{{ wp }}%{% endif %};"
  ></div>
  {% if record.warranty_progress >= 100 %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-light w-100 h-100">Expired {{ record.warranty_end|timesince|split:','|first }} ago</span>
  {% elif record.warranty_progress >= 35 %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-body-emphasis w-100 h-100">{{ record.warranty_end|timeuntil|split:','|first }}</span>
  {% elif record.warranty_progress >= 0 %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-body-emphasis w-100 h-100">{{ record.warranty_end|timeuntil|split:','|first }}</span>
  {% else %}
    <span class="justify-content-center d-flex align-items-center position-absolute text-body-emphasis w-100 h-100">Starts in {{ record.warranty_start|timeuntil|split:','|first }}</span>
  {% endif %}
</div>

{% endif %}
{% endwith wthresh %}
{% endwith wr %}
{% endwith wp %}
'''

class FirmwareInfoExtension(PluginTemplateExtension):
    def left_page(self):
        object = self.context.get('object')
        firmware = Firmware.objects.filter(**{self.kind:object}).first()
        context = {'firmware': firmware}
        context['warranty_progressbar'] = Template(WARRANTY_PROGRESSBAR)
        return self.render('firmware_management/inc/firmware_info.html', extra_context=context)


class DeviceFirmwareInfo(FirmwareInfoExtension):
    models = ['name']
    kind = 'device'

class InventoryItemFirmwareInfo(FirmwareInfoExtension):
    models = ['dcim.inventory_item']
    kind = 'inventory_item'


class ManufacturerFirmwareCounts(PluginTemplateExtension):
    models = ['dcim.manufacturer']
    def right_page(self):
        object = self.context.get('object')
        user = self.context['request'].user
        count_device = Firmware.objects.restrict(user, 'view').filter(device_type__manufacturer=object).count()
        count_inventory_item = Firmware.objects.restrict(user, 'view').filter(inventory_item_type__manufacturer=object).count()
        context = {
            'firmware_stats': [
                {
                    'label': 'Device',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=device',
                    'count': count_device,
                },
                {
                    'label': 'Inventory Item',
                    'filter_field': 'manufacturer_id',
                    'extra_filter': '&kind=inventory_item',
                    'count': count_inventory_item,
                },
                {
                    'label': 'Total',
                    'filter_field': 'manufacturer_id',
                    'count': count_device + count_inventory_item,
                },
            ],
        }
        return self.render('firmware_management/inc/firmware_stats_counts.html', extra_context=context)

template_extensions = (
    DeviceFirmwareInfo,
    InventoryItemFirmwareInfo,
    ManufacturerFirmwareCounts,
)