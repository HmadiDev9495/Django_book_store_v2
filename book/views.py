from django.http import HttpResponse
import datetime
from django.http import JsonResponse
from .models import Book

def current_datetime(request):
    print('request method is', request.method)
    html = 'this is MFT'
    return HttpResponse(html)

def current_datetime2(request):
    print('request method is', request.method)
    html = 'this is MFT sec'
    return HttpResponse(html)

def book_list_api(request):
    books = Book.objects.all()
    data = list(books.values(
        'id',
        'name',
        'author',
        'published_date',
        'price',
        'currency',
        'category'
    ))

    return JsonResponse(data, safe=False)