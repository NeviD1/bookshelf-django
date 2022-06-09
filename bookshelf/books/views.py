import csv
import json

from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Author, Book


class BooksListWithMoreThanTwoAuthorsView(generic.ListView):

    def get_queryset(self):
        return Book.objects\
            .annotate(authors_count=Count('authors'))\
            .filter(authors_count__gte=2)\
            .prefetch_related('authors')

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [book.convert_to_dict() for book in queryset]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="books.csv"'

        writer = csv.DictWriter(response, fieldnames=['id', 'name', 'description', 'authors'])
        writer.writeheader()
        writer.writerows(data)

        return response


class BooksListByAuthorView(generic.ListView):

    def get_queryset(self):
        author_id = self.kwargs['author_id']
        author = get_object_or_404(Author, id=author_id)
        return Book.objects\
            .filter(authors=author)\
            .prefetch_related('authors')

    def get(self, requets, *args, **kwargs):
        queryset = self.get_queryset()
        data = [book.convert_to_dict() for book in queryset]
        return JsonResponse(data, status=200, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AuthorListCreateView(generic.View):

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            data = None
        if not isinstance(data, list) or any(not isinstance(name, str) for name in data):
            raise ValidationError('Data must be a list with strings - names of authors.')
        created_authors = []
        for name in set(data):
            author, created = Author.objects.get_or_create(name=name)
            if created:
                created_authors.append(name)
        return HttpResponse(f'Authors created: {created_authors}', status=200)
