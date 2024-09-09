from django.db import models
from django.urls import reverse


class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255, blank=True, null=True)
    named_url = models.CharField(max_length=255, blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_url(self):
        """Возвращает URL для пункта меню."""
        return self.url
