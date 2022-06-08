from django.urls import path

from . import views

app_name = 'books'
urlpatterns = [
    path('books_with_more_than_two_authors/', views.BooksListWithMoreThanTwoAuthorsView.as_view()),
    path('author/<int:author_id>/books/', views.BooksListByAuthorView.as_view()),
    path('create_authors/', views.AuthorListCreateView.as_view()),
]
