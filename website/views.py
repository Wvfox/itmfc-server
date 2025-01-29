from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import JSONParser

from config.decorators import error_handler_basic


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@error_handler_basic
def send_file_form(request):
    data = request.data

    if request.method == 'GET':
        print('test')
        return HttpResponse()

    elif request.method == 'POST':

        return HttpResponse()