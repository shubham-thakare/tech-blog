from django.db import models


class WebsiteSettings(models.Model):
    under_maintenance = models.BooleanField(null=False, default=False)

    def __str__(self):
        return "Website Settings"

    class Meta:
        verbose_name_plural = "WebsiteSettings"
