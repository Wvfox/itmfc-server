import threading
from datetime import date

from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from task.serializers import *


@api_view(['GET'])
def check(request, hostname, user):
    if not Task.objects.all().filter(
            name_desktop=hostname,
            login_user=user,
            action='clear',
            created_at=date.today()
    ).exists():
        Task.objects.create(
            name_desktop=hostname,
            login_user=user,
            action='clear'
        )
        return HttpResponse(status=201)
    return HttpResponse(status=200)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def task_list(request):
    """
    List all(GET) tasks, or create(POST) a new task.
    """
    data = request.data
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def task_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a task.
    """
    try:
        task = Task.objects.get(pk=pk)
        data = request.data
    except Task.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)

    elif request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=204)


@api_view(['PUT'])
def task_processing(request, pk):
    task = Task.objects.get(pk=pk)
    task.status = 'p'
    task.save()
    serializer = TaskSerializer(task)
    return JsonResponse(serializer.data)


@api_view(['PUT'])
def task_complete(request, pk):
    task = Task.objects.get(pk=pk)
    task.status = 'c'
    task.save()
    serializer = TaskSerializer(task)
    return JsonResponse(serializer.data)
