import os.path
import random
from os.path import splitext

from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser


from config.settings import MEDIA_ROOT, MEDIA_URL
from config.utilities import get_video_duration, clear_dir_media
from .serializers import *


LOCATION_LIST = ['voskresensk', 'beloozerskiy']


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])
def clip_list(request):
    """
    List all(GET) clips, or create(POST) a new clip.
    """
    data = request.data
    if request.method == 'GET':
        clips = Clip.objects.all()
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        _mutable = data._mutable
        data._mutable = True
        if data.get('expiration_date'):
            day, month, year = data['expiration_date'].split('.')
            data['expiration_date'] = f'{year}-{month}-{day}'
        data._mutable = _mutable
        serializer = ClipSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                # get video
                clip = Clip.objects.get(id=serializer.data['id'])
                # write duration video
                clip.duration = get_video_duration(str(MEDIA_ROOT) + str(clip.media))
                for loc in LOCATION_LIST:
                    clip.locations.create(name=loc)
                clip.save()
                return JsonResponse(ClipSerializer(clip).data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError as ex:
            print(ex)
            return HttpResponse(status=406)


# # convert video (bad quality)
# path, ext = splitext(str(clip.media))
# moviepy.VideoFileClip(clip.media.path).write_videofile(f'{MEDIA_URL}{path}.webm')
# # rewrite path in database
# clip.media = f'{path}.webm'
# # delete old video
# if os.path.exists(f'{MEDIA_URL}{path}{ext}'):
#     os.remove(f'{MEDIA_URL}{path}{ext}')
# add location


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def clip_list_shuffle(request):
    """
    Shuffle list all(GET) clips.
    """
    if request.method == 'GET':
        clips = Clip.objects.all().order_by('?')
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
def clip_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a clip.
    """
    try:
        clip = Clip.objects.get(pk=pk)
        data = request.data
    except Clip.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ClipSerializer(clip)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        _mutable = data._mutable
        data._mutable = True
        if not data.get('media'):
            data['media'] = clip.media
        data._mutable = _mutable
        serializer = ClipSerializer(clip, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)

    elif request.method == 'DELETE':
        if clip.media:
            if os.path.exists(clip.media.path):
                os.remove(clip.media.path)
        for loc in clip.locations.all():
            loc.delete()
        clip.delete()
        clear_dir_media()
        return HttpResponse(status=204)


@api_view(['GET'])
@parser_classes([JSONParser])
def nonstop_location(request, location: str):
    if request.method == 'GET':
        locations = Location.objects.all().filter(name=location, is_nonstop=True)
        # category = Subcategory.objects.get(pk=pk).category_set.all().first()
        clips = []
        for loc in locations:
            clips.append(loc.clip_set.all().first())
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT'])
@parser_classes([JSONParser])
def clip_submit(request):
    if request.method == 'GET':
        clips = Clip.objects.all().filter(is_submit=False)
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['PUT'])
@parser_classes([JSONParser])
def clip_check(request, pk: int):
    if request.method == 'PUT':
        clip = Clip.objects.get(pk=pk)
        clip.is_submit = True
        clip.save()
        serializer = ClipSerializer(clip)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
def location_list(request):
    """
    List all(GET) locations, or create(POST) a new location.
    """
    data = request.data
    if request.method == 'GET':
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = LocationSerializer(data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError as ex:
            print(ex)
            return HttpResponse(status=406)


@api_view(['PUT'])
@parser_classes([JSONParser])
def location_check(request, pk: int):
    if request.method == 'PUT':
        location = Location.objects.get(pk=pk)
        location.is_nonstop = False
        location.save()
        serializer = LocationSerializer(location)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
def location_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a location.
    """
    try:
        location = Location.objects.get(pk=pk)
        data = request.data
    except Location.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = LocationSerializer(location, data=data)
        try:
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        except IntegrityError:
            return HttpResponse(status=406)

    elif request.method == 'DELETE':
        location.delete()
        return HttpResponse(status=204)
