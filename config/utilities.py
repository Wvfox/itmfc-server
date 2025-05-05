
import os.path
from os.path import splitext
from uuid import uuid4
import cv2
from config.decorators import error_handler_basic

from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from config.settings import MEDIA_ROOT, BASE_DIR


class UUIDFileStorage(FileSystemStorage):
    """
    Creating a new unique name with uuid4.hex
    """
    @staticmethod
    def get_available_name(name, **kwargs):
        path, ext = splitext(name)
        delimiter = '/'
        if path.find('\\') != -1:
            delimiter = '\\'
        path = '/'.join(path.split(delimiter)[:-1])
        url = path + '/' + uuid4().hex + ext
        return url


def get_video_duration(path):
    # print(path)
    # create video capture object
    data = cv2.VideoCapture(path)

    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    # calculating duration of the video
    seconds = round(frames / fps)
    # video_time = datetime.timedelta(seconds=seconds)
    return seconds


def clear_dir_media():
    if os.path.exists(MEDIA_ROOT):
        for category in os.listdir(MEDIA_ROOT):
            for date in os.listdir(os.path.join(MEDIA_ROOT, category)):
                date_dir_path = os.path.join(MEDIA_ROOT, category, date)
                if not os.listdir(date_dir_path):
                    os.rmdir(date_dir_path)


@api_view(['GET'])
@parser_classes([JSONParser])
@error_handler_basic
def get_src_file(request, media_url: str):
    """Get file from MEDIA"""
    src = open((str(BASE_DIR) + '/' + media_url), 'rb')
    return FileResponse(src)



