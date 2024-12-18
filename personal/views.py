from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, parser_classes

from config.decorators import error_handler_basic, mfc_auth_token
from .serializers import *


'''---------------------------------------------------------------------
=========================== Operator request ===========================
---------------------------------------------------------------------'''


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def operator_list(request):
    """
    List all(GET) operators, or create(POST) a new operator.
    """
    data = request.data

    if request.method == 'GET':
        operators = Operator.objects.all()
        serializer = OperatorSerializer(operators, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = OperatorSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def operator_detail(request, pk=None, username=None, tg_id=None):
    """
    View(GET), update(PUT) or delete(DELETE) a operator.
    """
    if pk:
        operator = Operator.objects.get(pk=pk)
    elif username:
        operator = Operator.objects.get(username=username)
    elif tg_id:
        operator = Operator.objects.get(tg_id=tg_id)
    data = request.data

    if request.method == 'GET':
        serializer = OperatorSerializer(operator)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        if not data.get('username'):
            data['username'] = operator.username
        if not data.get('name'):
            data['name'] = operator.name
        # === Serializer ===
        serializer = OperatorSerializer(operator, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        operator.delete()
        return HttpResponse(status=204)


'''---------------------------------------------------------------------
=========================== Printer request ============================
---------------------------------------------------------------------'''


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def printer_list(request):
    """
    List all(GET) printers, or create(POST) a new printer.
    """
    data = request.data

    if request.method == 'GET':
        printers = Printer.objects.all()
        serializer = PrinterSerializer(printers, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = PrinterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def printer_detail(request, ip: str):
    """
    View(GET), update(PUT) or delete(DELETE) a printer.
    """
    printer = Printer.objects.get(ip_printer=ip)
    data = request.data

    if request.method == 'GET':
        serializer = PrinterSerializer(printer)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        if not data.get('ip_printer'):
            data['ip_printer'] = printer.ip_printer
        if not data.get('model_printer'):
            data['model_printer'] = printer.model_printer
        # === Serializer ===
        serializer = PrinterSerializer(printer, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        printer.delete()
        return HttpResponse(status=204)


'''---------------------------------------------------------------------
========================== Workstation request =========================
---------------------------------------------------------------------'''


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def workstation_list(request):
    """
    List all(GET) workstations, or create(POST) a new workstation.
    """
    data = request.data

    if request.method == 'GET':
        workstations = Workstation.objects.all()
        serializer = WorkstationSerializer(workstations, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = WorkstationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Add printer to workstation
        if data.get('ip_printer'):
            current_workstation = Workstation.objects.get(pk=serializer.data['id'])
            current_workstation.printers.add(Printer.objects.get(ip_printer=data['ip_printer']))
            current_workstation.save()
            return JsonResponse(WorkstationSerializer(current_workstation).data, status=201)
        return JsonResponse(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def workstation_detail(request, name: str):
    """
    View(GET), update(PUT) or delete(DELETE) a workstation.
    """
    workstation = Workstation.objects.get(name_desktop=name)
    data = request.data

    if request.method == 'GET':
        serializer = WorkstationSerializer(workstation)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        if not data.get('name_desktop'):
            data['name_desktop'] = workstation.name_desktop
        serializer = WorkstationSerializer(workstation, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        workstation.delete()
        return HttpResponse(status=204)


@api_view(['PUT', 'DELETE'])
@parser_classes([JSONParser])
@mfc_auth_token
@error_handler_basic
def workstation_printer(request, name: str, ip: str):
    """
    Add(PUT) or remove(DELETE) printer of workstation.
    """
    workstation = Workstation.objects.get(name_desktop=name)

    if request.method == 'PUT':
        workstation.printers.add(Printer.objects.get(ip_printer=ip))
        workstation.save()
        return JsonResponse(WorkstationSerializer(workstation).data)

    elif request.method == 'DELETE':
        workstation.printers.remove(Printer.objects.get(ip_printer=ip))
        workstation.save()
        return JsonResponse(WorkstationSerializer(workstation).data)
