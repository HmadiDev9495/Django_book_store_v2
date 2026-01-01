from django.urls import path
from .views import current_datetime, book_list_api , book_insert
urlpatterns = [
    path('book-view/', current_datetime),
    path('book/insert/', book_insert, name='book_insert'),
    path('api/books/', book_list_api, name='book_list_api'),
]