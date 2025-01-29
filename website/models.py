from django.db import models

from config.utilities import UUIDFileStorage


class Vacancy(models.Model):
    media = models.FileField(
        upload_to='vacancy',
        storage=UUIDFileStorage()
    )
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.pk
