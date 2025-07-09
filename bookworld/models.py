from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField('Author', related_name='books')
    publisher = models.ForeignKey('Publisher', related_name='books', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='books')

    def __str__(self):
      return self.title


class Author(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
      return self.name

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
      return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
      return self.name
