from django.db import models

class SoftwareLicense(models.Model):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=100, blank=True, null=True)
    application_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.version or 'N/A'}"