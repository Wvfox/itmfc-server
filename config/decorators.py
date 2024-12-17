from sqlite3 import IntegrityError

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


def error_handler_basic(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ObjectDoesNotExist as ex:
            return JsonResponse({'Message': (str(ex))}, status=404)
        except IntegrityError as ex:
            return JsonResponse({'Message': (str(ex))}, status=406)
        except Exception as ex:
            return JsonResponse({'Message': (str(ex))}, status=400)
    return wrapper
