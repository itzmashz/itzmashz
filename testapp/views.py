from test.test_long import BASE
from django.shortcuts import render
import uuid
from requests.auth import HTTPBasicAuth
from django.http import JsonResponse
import base64
from djangosh.utilities import get_logger
from django.template import loader
from rest_framework import status

logger = get_logger('testapp/logs/request.log')

def get_token(request, *args, **kwargs):
  auth = HTTPBasicAuth('admin', 'admin')

  response = None
  credential = f"{auth.username}:{auth.password}"
  auth_header = f"Basic {base64.b64encode(bytes(credential, 'utf-8')).decode('utf-8')}"
  if request.method=='GET' and request.headers.get('Authorization')==auth_header:
    token = uuid.uuid4().hex
    response = JsonResponse({'id_token': token}, status=200)
  else:
    response = JsonResponse({'error': 'Request processed but Auth not valid!'}, status=400)

  logger.info(f"Request received: {request.method} {request.path} \n\tRequest Headers: {request.headers} \n\tRequest Body: {request.body} \n\tInstalled Auth: {(auth.username, auth.password)}\n\tResponse: {response.status_code}")
  return response


def reset_password(request, *args, **kwargs):
  if request.method == 'POST':
    new_password = request.POST.get('new_password')
    retyped_password = request.POST.get('retyped_password')
    if new_password == retyped_password:
      # Send email with reset password link
      logger.info(f"Accepted# Request for reset password: ({(new_password, retyped_password)})")
      return JsonResponse({'message': 'Request for reset password accepted'}, status=status.HTTP_202_ACCEPTED)
    else:
      logger.info(f"Failed# Request for reset password: ({(new_password, retyped_password)})")
      return JsonResponse({'message': 'Request for reset password failed'}, status=status.HTTP_400_BAD_REQUEST)
  elif request.method == 'GET':
    template = loader.get_template('testapp/_reset_password.html')
    context = {'title': 'Reset Password'}
    return JsonResponse({'data': template.render(context, request)}, status=status.HTTP_200_OK)
  else:
    logger.info(f"Failed# Request for reset password: ({request.method})")
    return JsonResponse({'message': 'Request for reset password failed'}, status=status.HTTP_400_BAD_REQUEST)
