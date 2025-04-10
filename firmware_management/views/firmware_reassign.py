from django.urls import reverse
from django.views.generic.edit import FormView
from ..forms.reassign import FirmwareDeviceReassignForm, FirmwareModuleReassignForm, FirmwareInventoryItemReassignForm
from dcim.models import Device, Module, InventoryItem

__all__ = (
    'FirmwareDeviceReassignView',
    'FirmwareModuleReassignView',
)

class FirmwareDeviceReassignView(FormView):
    queryset = Device.objects.all()
    template_name = 'firmware_management/firmware_reassign.html'
    form_class = FirmwareDeviceReassignForm

    def get_initial(self):
        """
        Pre-fill the form with the device instance if available.
        """
        device_id = self.kwargs.get('device_id')
        device = Device.objects.get(pk=device_id)
        return {
            'device': device,
        }

    def form_valid(self, form):
        """
        Process the form and save the reassignment.
        """
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the device detail page after successful reassignment.
        """
        return reverse('dcim:device', kwargs={'pk': self.kwargs.get('device_id')})
    
class FirmwareModuleReassignView(FormView):
    queryset = Module.objects.all()
    template_name = 'firmware_management/firmware_reassign.html'
    form_class = FirmwareModuleReassignForm
    
    def get_initial(self):
        """
        Pre-fill the form with the module instance if available.
        """
        module_id = self.kwargs.get('module_id')
        module = Module.objects.get(pk=module_id)
        return {
            'module': module,
        }

    def form_valid(self, form):
        """
        Process the form and save the reassignment.
        """
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        """
        Redirect to the module detail page after successful reassignment.
        """
        return reverse('dcim:module', kwargs={'pk': self.kwargs.get('module_id')})