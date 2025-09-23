### This Template code is needed to make the firmware compatible devicetypes and moduletypes likefied.
### It will aslo show a max of 3. Once you have more than 3, if will show you the amount and use the side page to show you all.

# FIRMWARE_DEVICE_TYPES = """
# {% load i18n %}
# {% if value.count > 3 %}
#   <a href="{% url 'dcim:devicetype_list' %}?firmware_id={{ record.pk }}">{{ value.count }} Device Types</a>
# {% else %}
#   {% for devicetype in value.all %}
#     <a href="{{ devicetype.get_absolute_url }}">{{ devicetype.model }}</a><br />
#   {% endfor %}
# {% endif %}
# """




### This Template code is needed to show all the firmware compatible devicetypes and moduletypes + make them likefied.


SHOW_LINKED_DEVICE_TYPES = """
{% load i18n %}
{% for devicetype in value.all %}
  <a href="{{ devicetype.get_absolute_url }}">{{ devicetype }}</a><br />
{% endfor %}
"""


SHOW_LINKED_MODULE_TYPES = """
{% load i18n %}
{% for moduletype in value.all %}
  <a href="{{ moduletype.get_absolute_url }}">{{ moduletype }}</a><br />
{% endfor %}
"""
