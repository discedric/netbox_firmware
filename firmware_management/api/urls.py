from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'firmware_management'

router = NetBoxRouter()

# firmware
router.register('firmware', views.FirmwareViewSet)
router.register('firmware-assignment', views.FirmwareAssigmentViewSet)

urlpatterns = router.urls