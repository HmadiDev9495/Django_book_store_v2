from django.urls import path
from .api_views import BookListView, BookCreateView, BookUpdateView, BookDeleteView
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
]