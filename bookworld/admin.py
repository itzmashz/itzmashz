from django.contrib import admin
from bookworld.models import Book, Author, Publisher, Tag

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Tag)

# Register your models here.
