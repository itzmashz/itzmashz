from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .utilities import logger as system_logger
from .decorators import auth_required

@auth_required('admin', 'adminx')
def index(request):
  system_logger.info(f"{request.method}: {request.path}\n\t Request Headers: {request.headers}")
  return JsonResponse({"message": "Hello, world!", "rpath": request.path, "rmethod": request.method, "rbody": request.body.decode('utf-8')})
