from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import JSONParser
from django.core.mail import send_mail
from config.decorators import error_handler_basic


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@error_handler_basic
def send_file_form(request):
    data = request.data

    if request.method == 'GET':
        send_mail(
            subject='Вакансии',
            message='Тестовое сообщение',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS],
            fail_silently=False,
        )
        return HttpResponse()

    elif request.method == 'POST':
        send_mail(
            subject='Вакансии',
            message='Тестовое сообщение',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS]
        )
        return HttpResponse()
