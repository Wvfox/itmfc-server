import datetime
import os.path
import requests
# import boto3
# from botocore.config import Config

from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser

from config.decorators import error_handler_basic, mfc_auth_token
from config.settings import MEDIA_ROOT, BASE_DIR
from config.utilities import clear_dir_media, get_video_duration, decrypt_aes
from .serializers import *


LOCATION_LIST = ['voskresensk', 'beloozerskiy']


@api_view(['GET'])
@parser_classes([JSONParser])
def init_media_s3(request):
    for clip in Clip.objects.all().filter(is_wrong=False):
        file_name = clip.media.url.split('/')[-1]
        dir_list = clip.media.url[1::].split('/')[:-1]

        layer_first = dir_list[0]
        if not os.path.exists(layer_first):
            os.makedirs(layer_first)
        layer_second = dir_list[0] + '\\' + dir_list[1]
        if not os.path.exists(layer_second):
            os.makedirs(layer_second)
        layer_third = dir_list[0] + '\\' + dir_list[1] + '\\' + dir_list[2]
        if not os.path.exists(layer_third):
            os.makedirs(layer_third)

        with open(clip.media.url[1::], 'wb') as file:
            file.write(requests.get('https://s3.twcstorage.ru/ca061599-n1app' + clip.media.url).content)
    return HttpResponse()


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
        key = decrypt_aes(data['cypher'])
        if key != os.environ.get("UPLOAD_TOKEN"):
            return JsonResponse({'Message': 'Failed authorization'}, status=403)
        serializer = ClipSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        local_path = serializer.data['media']
        full_path = f'{BASE_DIR}{local_path}'
        # boto3.client(
        #     's3',
        #     aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
        #     aws_secret_access_key=os.environ.get("S3_SECRET_KEY"),
        #     endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
        #     config=Config(signature_version='s3')
        # ).upload_file(
        #     full_path,
        #     'ca061599-n1app',
        #     local_path[1::]
        # )
        # get video
        clip = Clip.objects.get(id=serializer.data['id'])
        # write duration video
        clip.duration = get_video_duration(str(MEDIA_ROOT) + str(clip.media)) + 2

        for loc in LOCATION_LIST:
            clip.locations.create(name=loc)
        clip.save()
        return JsonResponse(ClipSerializer(clip).data, status=201)


@api_view(['GET'])
@parser_classes([JSONParser])
@error_handler_basic
def clip_list_shuffle(request):
    """
    Shuffle list all(GET) clips.
    """
    if request.method == 'GET':
        clips = Clip.objects.all().filter(
            is_wrong=False,
            expiration_date__gte=datetime.datetime.today()
        ).order_by('?')
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@parser_classes([JSONParser])
@error_handler_basic
def clip_list_expiration(request):
    """
    Shuffle list all(GET) clips.
    """
    if request.method == 'GET':
        clips = Clip.objects.all().filter(
            is_wrong=False,
            expiration_date__lt=datetime.datetime.today()
        )
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['GET', 'PUT'])
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
#
#     elif request.method == 'PUT':
#         key = decrypt_aes(data['cypher'])
#         if key != os.environ.get("UPLOAD_TOKEN"):
#             return JsonResponse({'Message': 'Failed authorization'}, status=403)
#         _mutable = data._mutable
#         data._mutable = True
#         if not data.get('media'):
#             data['media'] = clip.media
#         data._mutable = _mutable
#         serializer = ClipSerializer(clip, data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return JsonResponse(serializer.data)



@api_view(['DELETE'])
@parser_classes([MultiPartParser])
@mfc_auth_token
@error_handler_basic
def clip_delete(request, pk: int):
    """
    View(GET), update(PUT) or delete(DELETE) a clip.
    """
    clip = Clip.objects.get(pk=pk)

    if request.method == 'DELETE':
        if clip.media:
            if os.path.exists(clip.media.path):
                os.remove(clip.media.path)
        for loc in clip.locations.all():
            loc.delete()
        clip.delete()
        clear_dir_media()
        return HttpResponse(status=204)


@api_view(['POST'])
@parser_classes([MultiPartParser])
@error_handler_basic
def clip_upload_s3(request):
    data = request.data

    if request.method == 'POST':
        # key = decrypt_aes(data['cypher'])
        # if key != os.environ.get("UPLOAD_TOKEN"):
        #     return JsonResponse({'Message': 'Failed authorization'}, status=403)
        serializer = ClipSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        local_path = serializer.data['media']
        full_path = f'{BASE_DIR}{local_path}'
        s3_client.upload_file(
            full_path,
            'ca061599-n1app',
            local_path[1::]
        )
        if os.path.exists(full_path):
            os.remove(full_path)
        return JsonResponse({'message': 'success'}, status=201)


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


@api_view(['GET'])
@parser_classes([JSONParser])
@error_handler_basic
def clip_submit(request):
    if request.method == 'GET':
        clips = Clip.objects.all().filter(is_submit=False, is_wrong=False)
        serializer = ClipSerializer(clips, many=True)
        return JsonResponse(serializer.data, safe=False)


@api_view(['PUT'])
@parser_classes([JSONParser])
@mfc_auth_token
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
# @mfc_auth_token
@error_handler_basic
def clip_wrong_check(request, pk: int):
    if request.method == 'PUT':
        # clip = Clip.objects.get(pk=pk)
        # clip.is_wrong = True
        # clip.save()
        # serializer = ClipSerializer(clip)
        # return JsonResponse(serializer.data, safe=False)
        return HttpResponse()


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
@mfc_auth_token
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
@mfc_auth_token
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
@mfc_auth_token
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
