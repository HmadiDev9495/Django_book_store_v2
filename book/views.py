from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book
from .forms import CreateBook
from django.shortcuts import render

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


@csrf_exempt
def book_insert(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            form = CreateBook(data)

            if form.is_valid():
                book = form.save()
                return JsonResponse({
                    "status": "success",
                    "message": "Book added successfully",
                    "book_id": book.id
                }, status=201)
            else:
                return JsonResponse({
                    "status": "error",
                    "errors": form.errors
                }, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)

def books_list_page(request):
    books = Book.objects.all().order_by('-created_at')
    return render(request, 'book/books.html', {'books': books})

def home_page(request):
    return render(request, 'book/home.html')