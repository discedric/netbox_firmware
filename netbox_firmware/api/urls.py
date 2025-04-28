from django.urls import path, include
from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_firmware'

router = NetBoxRouter()
router.register(r'firmware', views.FirmwareViewSet)
router.register(r'firmware-assignment', views.FirmwareAssigmentViewSet)

router.register(r'bios', views.BiosViewSet)
router.register(r'bios-assignment', views.BiosAssigmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]