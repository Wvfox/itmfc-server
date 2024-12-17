from django.db import models


class Task(models.Model):
    STATUS_CHOICES = [
        ('w', 'Waiting'),
        ('p', 'Processing'),
        ('c', 'Complete')
    ]
    status = models.CharField('Status', max_length=1, choices=STATUS_CHOICES, default='w')
    action = models.CharField('Action', max_length=64, blank=True, null=True)
    command = models.TextField('Command', blank=True, null=True)
    updated_at = models.DateField('Date of updating', auto_now=True)
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['status']

    def __str__(self):
        return f'{self.pk} | {self.status}'
