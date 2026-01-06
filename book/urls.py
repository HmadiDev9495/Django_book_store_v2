from django.urls import path
from .views import current_datetime, book_list_api , book_insert
from .api_views import BookListView , BookCreateView ,BookUpdateView , BookDeleteView
from .views import books_list_page ,  home_page, books_list_page

urlpatterns = [
    path('book-view/', current_datetime),
    path('book/insert/', book_insert, name='book_insert'),
    path('api/books/', book_list_api, name='book_list_api'),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/', books_list_page, name='books-list-page'),
    path('', home_page, name='home_page'),
    path('books/', books_list_page, name='books_list_page'),
    path('api/books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('api/books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
]