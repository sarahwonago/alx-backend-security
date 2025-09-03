from django.db import models


class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.ip_address} - {self.path} - {self.timestamp}"
