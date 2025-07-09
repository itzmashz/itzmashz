
from .utilities import logger
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
import base64

class PermissionError(Exception):
  def __init__(self, message):
    self.message = message
    logger.error(message)

def auth_required(username, password):
  def decorator(func):
    def wrapper(request, *args, **kwargs):
      logger.info(
        (f"Checking authorization for user {username}"
          f"\n\tFrom: {(request.META.get('REMOTE_ADDR', None), request.META.get('REMOTE_HOST', None), request.META.get('REMOTE_USER', None), request.META.get('REMOTE_PORT', None))}"
          f"\n\tRequest Method: {request.method}"
          f"\n\tRequest Path: {request.path}"
          f"\n\tRequest Headers: {request.headers}"
          f"\n\tRequest Body: {request.body}"

        )
      )
      auth = HTTPBasicAuth(username, password)
      credential = f"{auth.username}:{auth.password}"
      auth_header = f"Basic {base64.b64encode(bytes(credential, 'utf-8')).decode('utf-8')}"

      if request.headers.get('Authorization') == auth_header:
        return func(request, *args, **kwargs)
      else:
        logger.error(f"Unauthorized access attempt by {username}")
        PermissionError(f"Unauthorized: {request.headers['Credentials'] if 'Credentials' in request.headers else 'No credentials provided'}")
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    return wrapper
  return decorator
