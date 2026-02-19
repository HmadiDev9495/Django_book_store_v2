from django.urls import path
from .api_views import (
    BookListView, BookCreateView, BookUpdateView, BookDeleteView,
    PublishedBookListView, MyBookListView, MyBookDetailView,
    BookImageUploadView, BookImageListView, BookImageDeleteView,
)

from book.views import *

urlpatterns = [
    path('book-view/', current_datetime),
    path('index', index, name='index'),
    path('book/insert/', book_insert, name='book_insert'),
    path('api/books/func/', book_list_api, name='book_list_api'),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/', books_list_page, name='books-list-page'),
    path('', home_page, name='home_page'),
    path('api/books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('api/books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('get-book/<str:price>', GetBookAPI.as_view()),
    path('api/books/published/', PublishedBookListView.as_view(), name='published-books'),
    path('api/books/my/', MyBookListView.as_view(), name='my-books'),
    path('api/books/my/<int:pk>/', MyBookDetailView.as_view(), name='my-book-detail'),
    path('api/books/<int:book_id>/images/', BookImageListView.as_view(), name='book-images-list'),
    path('api/books/<int:book_id>/images/upload/', BookImageUploadView.as_view(), name='book-image-upload'),
    path('api/books/images/<int:pk>/delete/', BookImageDeleteView.as_view(), name='book-image-delete'),
]