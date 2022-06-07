from django.db import models


class Author(models.Model):
    name = models.CharField(verbose_name='ФИО', max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(verbose_name='Название', max_length=300)
    authors = models.ManyToManyField(Author)
    description = models.TextField(verbose_name='Описание', max_length=10000, null=True, blank=True)

    def __str__(self):
        return self.name
