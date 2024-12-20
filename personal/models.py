from django.db import models


class Operator(models.Model):
    username = models.SlugField('Username', max_length=64, unique=True, blank=True, null=True)
    name = models.CharField('Name', max_length=128)
    tag = models.CharField('Tag', max_length=64, unique=True, blank=True, null=True)
    tg_id = models.BigIntegerField('Tg user id', unique=True, blank=True, null=True)
    birthday = models.DateField('Birthday', max_length=32, blank=True, null=True)
    is_head = models.BooleanField('Head', default=False)
    is_admin = models.BooleanField('System administrator', default=False)
    departament = models.CharField('Departament', max_length=64, blank=True, null=True)
    date_ecp = models.DateField('Date end ECP', max_length=32, blank=True, null=True)
    updated_at = models.DateField('Date of updating', auto_now=True)
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


class History(models.Model):
    source = models.CharField(max_length=64)
    info = models.TextField()
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.pk} | {self.source}'


class Printer(models.Model):
    ip_printer = models.CharField('IP-address printer', max_length=32, unique=True)
    model_printer = models.CharField('Model printer', max_length=32)
    history = models.ManyToManyField(History, blank=True)
    updated_at = models.DateField('Date of updating', auto_now=True)
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['ip_printer']

    def __str__(self):
        return self.ip_printer


class Workstation(models.Model):
    name_desktop = models.SlugField('Name desktop', max_length=32, unique=True)
    ip_desktop = models.CharField('IP-address desktop', max_length=32, unique=True, blank=True, null=True)
    mac_desktop = models.CharField('MAC-address desktop', max_length=32, unique=True, blank=True, null=True)
    printers = models.ManyToManyField(Printer, blank=True)
    ip_assistant = models.CharField('IP-address assistant', max_length=32, unique=True, blank=True, null=True)
    updated_at = models.DateField('Date of updating', auto_now=True)
    created_at = models.DateField('Date of creation', auto_now_add=True)

    class Meta:
        ordering = ['name_desktop']

    def __str__(self):
        return self.name_desktop


