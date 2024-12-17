from django.db import models

from personal.models import Workstation, Operator


class Application(models.Model):
    category = models.CharField('Category', max_length=64)
    user_name = models.CharField('User name', max_length=64, blank=True, null=True)
    user_tag = models.CharField('Tag name', max_length=64, blank=True, null=True)
    user_location = models.CharField('Location', max_length=32, blank=True, null=True)
    operator = models.ForeignKey(
        Operator,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    workstation = models.ForeignKey(
        Workstation,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    description = models.TextField('Description', default='', blank=True)
    # screenshot = models.ImageField(
    #     upload_to='screenshot_application/%d-%m-%Y',
    #     storage=UUIDFileStorage(),
    #     blank=True,
    #     null=True,
    # )
    screenshot_url = models.TextField(
        'Screenshot',
        default='',
        blank=True,
    )
    executor = models.ForeignKey(
        Operator,
        related_name='Executor',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    # cancel | new | waiting | process | complete
    status = models.CharField(
        'Status',
        max_length=32,
        default='new'
    )
    updated_at = models.DateField('Date of updating', auto_now=True)
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.category
