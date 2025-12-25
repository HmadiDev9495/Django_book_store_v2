from django.urls import path
from .views import current_datetime, current_datetime2
from .views import current_datetime, current_datetime2, book_list_api
urlpatterns = [
    path('book-view/', current_datetime),
    path('book-view2/', current_datetime2),
    path('api/books/', book_list_api, name='book_list_api'),
]