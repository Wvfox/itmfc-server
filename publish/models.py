from django.db import models

from config.utilities import UUIDFileStorage


class Location(models.Model):
    name = models.CharField(max_length=64)
    is_nonstop = models.BooleanField(default=True)
    updated_at = models.DateField('Date of updating', auto_now=True)
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Clip(models.Model):
    name = models.CharField(max_length=64)
    media = models.FileField(
        upload_to='publish/%d-%m-%Y',
        storage=UUIDFileStorage()
    )
    expiration_date = models.DateField(blank=True, null=True)
    duration = models.PositiveSmallIntegerField(blank=True, null=True)
    is_submit = models.BooleanField(default=False)
    updated_at = models.DateField('Date of updating', auto_now=True)
    locations = models.ManyToManyField(Location, blank=True)
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


