import os.path

from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser

from config.decorators import error_handler_basic
from config.settings import MEDIA_ROOT
from config.utilities import get_video_duration, clear_dir_media
from .serializers import *


LOCATION_LIST = ['voskresensk', 'beloozerskiy']


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser])
@error_handler_basic
def clip_list(request):
    """
    List all(GET) clips, or create(POST) a new clip.
    """
    data = request.data

    if request.method == 'GET':
        clips = Clip.objects.all().filter(is_wrong=False)
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        serializer = ClipSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # get video
        clip = Clip.objects.get(id=serializer.data['id'])
        # write duration video
        clip.duration = get_video_duration(str(MEDIA_ROOT) + str(clip.media)) + 2
        for loc in LOCATION_LIST:
            clip.locations.create(name=loc)
        clip.save()
        return JsonResponse(ClipSerializer(clip).data, status=201)


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
@error_handler_basic
def clip_list_shuffle(request):
    """
    Shuffle list all(GET) clips.
    """
    if request.method == 'GET':
        clips = Clip.objects.all().filter(is_wrong=False).order_by('?')
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([MultiPartParser])
@error_handler_basic
def clip_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a clip.
    """
    clip = Clip.objects.get(pk=pk)
    data = request.data

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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

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
@error_handler_basic
def nonstop_location(request, location: str):
    if request.method == 'GET':
        locations = Location.objects.all().filter(name=location, is_nonstop=True)
        clips = []
        for loc in locations:
            if loc.clip_set.all().filter(is_wrong=False).exists():
                clips.append(loc.clip_set.all().first())
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT'])
@parser_classes([JSONParser])
@error_handler_basic
def clip_submit(request):
    if request.method == 'GET':
        clips = Clip.objects.all().filter(is_submit=False, is_wrong=False)
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['PUT'])
@parser_classes([JSONParser])
@error_handler_basic
def clip_check(request, pk: int):
    if request.method == 'PUT':
        clip = Clip.objects.get(pk=pk)
        clip.is_submit = True
        clip.save()
        serializer = ClipSerializer(clip)
        return JsonResponse(serializer.data, safe=False)


@api_view(['PUT'])
@parser_classes([JSONParser])
@error_handler_basic
def clip_wrong_check(request, pk: int):
    if request.method == 'PUT':
        clip = Clip.objects.get(pk=pk)
        clip.is_wrong = True
        clip.save()
        serializer = ClipSerializer(clip)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@parser_classes([JSONParser])
@error_handler_basic
def clip_wrong_list(request):
    if request.method == 'GET':
        clips = Clip.objects.all().filter(is_wrong=True)
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'POST'])
@parser_classes([JSONParser])
@error_handler_basic
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
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=201)


@api_view(['PUT'])
@parser_classes([JSONParser])
@error_handler_basic
def location_check(request, pk: int):
    if request.method == 'PUT':
        location = Location.objects.get(pk=pk)
        location.is_nonstop = False
        location.save()
        serializer = LocationSerializer(location)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT', 'DELETE'])
@parser_classes([JSONParser])
@error_handler_basic
def location_detail(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a location.
    """
    location = Location.objects.get(pk=pk)
    data = request.data

    if request.method == 'GET':
        serializer = LocationSerializer(location)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        serializer = LocationSerializer(location, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data)

    elif request.method == 'DELETE':
        location.delete()
        return HttpResponse(status=204)
