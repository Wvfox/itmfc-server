from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import MultiPartParser
from django.core.mail import send_mail
from config.decorators import error_handler_basic

from .serializers import *


@api_view(['POST'])
@parser_classes([MultiPartParser])
@error_handler_basic
def send_vacancy(request):
    data = request.data

    if request.method == 'POST':
        serializer = VacancySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        url = serializer.data['media']
        send_mail(
            subject='Вакансии - резюме',
            message=f'Резюме можно просмотреть по ссылке ниже:\n'
                    f'https://api.itmfc.ru/api/file/{url}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS],
            fail_silently=False,
        )
        return JsonResponse(serializer.data, status=201)
