from django.urls import path, include
from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_firmware'

router = NetBoxRouter()
router.register(r'firmware', views.FirmwareViewSet)
router.register(r'firmware-assignment', views.FirmwareAssigmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]