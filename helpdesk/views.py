from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes

from config.decorators import error_handler_basic, mfc_auth_token
from .serializers import *


'''---------------------------------------------------------------------
========================= Application request ==========================
---------------------------------------------------------------------'''


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def application_list(request):
    """
    List all(GET) application, or create(POST) a new application.
    """
    data = request.data

    if request.method == 'GET':
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = ApplicationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        if data.get('operator_username'):
            serializer.validated_data['operator'] = Operator.objects.get(
                username=data['operator_username']
            )
        if data.get('workstation_name'):
            serializer.validated_data['workstation'] = Workstation.objects.get(
                name_desktop=data['workstation_name']
            )
        serializer.save()
        return JsonResponse(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def application_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a application.
    """
    application = Application.objects.get(pk=pk)
    data = request.data

    if request.method == 'GET':
        serializer = ApplicationSerializer(application)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        if not data.get('category'):
            data['category'] = application.category
        # === Serializer ===
        serializer = ApplicationSerializer(application, data=data)
        serializer.is_valid(raise_exception=True)
        if data.get('operator_username'):
            serializer.validated_data['operator'] = Operator.objects.get(
                username=data['operator_username']
            )
        if data.get('workstation_name'):
            serializer.validated_data['workstation'] = Workstation.objects.get(
                name_desktop=data['workstation_name']
            )
        if data.get('executor_id'):
            serializer.validated_data['executor'] = Operator.objects.get(
                tg_id=data['executor_id']
            )
        if data.get('signer_id'):
            serializer.validated_data['signer'] = Operator.objects.get(
                tg_id=data['signer_id']
            )
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    elif request.method == 'DELETE':
        application.delete()
        return HttpResponse(status=204)


'''---------------------------------------------------------------------
=========================== Button request =============================
---------------------------------------------------------------------'''


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def button_list(request):
    """
    List all(GET) button, or create(POST) a new button.
    """
    data = request.data

    if request.method == 'GET':
        buttons = Button.objects.all()
        serializer = ButtonSerializer(buttons, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = ButtonSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def button_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a button.
    """
    button = Button.objects.get(pk=pk)
    data = request.data

    if request.method == 'GET':
        serializer = ButtonSerializer(button)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        if not data.get('title'):
            data['title'] = button.title
        # === Serializer ===
        serializer = ButtonSerializer(button, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)

    elif request.method == 'DELETE':
        button.delete()
        return HttpResponse(status=204)


@api_view(['GET'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def button_type(request, type_filter: str):
    if request.method == 'GET':
        buttons = Button.objects.filter(type=type_filter).all()
        serializer = ButtonSerializer(buttons, many=True)
        return JsonResponse(serializer.data, safe=False)
