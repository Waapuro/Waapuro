from django.db import models


class SiteConfig(models.Model):
    """SiteConfig"""

    def __str__(self):
        return self.key

    key = models.CharField("KEY", unique=True, max_length=128, help_text="Key")
    value = models.CharField("VALUE", max_length=128, null=True, help_text="VALUE")
    help_text = models.CharField("Help Text", max_length=256, null=True, help_text="Help Text")

    class Meta:
        permissions = [
            ("can_read_SiteConfigs".lower(), "Can read SiteConfigs info"),
            ("can_write_SiteConfigs".lower(), "Can write SiteConfigs info"),
        ]
        verbose_name = "SiteConfig"
        verbose_name_plural = "SiteConfigs"
