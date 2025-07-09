from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from rest_framework import permissions, viewsets

from bookworld.serializers import UserSerializer, GroupSerializer, BookSerializer, AuthorSerializer, PublisherSerializer, TagSerializer
from bookworld.models import Book, Author, Publisher, Tag
import logging
import datetime
from django.conf import settings

def get_logger_format_with_extd(*args):
  logger_format = "%(asctime)s %(levelname)s %(message)s for"
  for keys in args:
    logger_format += f" {keys}=%({keys})s"
  return logger_format

logging.basicConfig(
  filename=(settings.BASE_DIR/"djangosh/logs/books.log").as_posix(),
  filemode="a+",
  format=get_logger_format_with_extd(  ),
  level=logging.ERROR
)
logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
      print("get request found")
      logger.error("get request found username: {username}, email: {email}, request: {request}".format(username=request.user.username, email=request.user.email, request=request))
      return super().list(request, *args, **kwargs)

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]

class PublisherViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows publishers to be viewed or edited.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tags to be viewed or edited.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
