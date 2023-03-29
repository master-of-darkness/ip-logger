from django.db import models


# Create your models here.
class Loggers(models.Model):
    id = models.AutoField(primary_key=True)
    victim_url = models.CharField(max_length=10)
    admin_url = models.CharField(max_length=10)
    admin_username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    type = models.CharField(max_length=4)
    asset = models.TextField(blank=True)


class catched(models.Model):
    ip = models.GenericIPAddressField()
    admin_url_connected = models.CharField(max_length=10, null=False)
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    languages = models.CharField(max_length=128)
    catched_at = models.DateTimeField(auto_now_add=True, blank=False)
    user_agent = models.CharField(max_length=128)
    OS = models.CharField(max_length=128)
    browser = models.CharField(max_length=128)


