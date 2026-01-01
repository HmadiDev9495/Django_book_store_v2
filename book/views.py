from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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



@csrf_exempt
def book_insert(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            if not data.get('name'):
                return JsonResponse({"status": "error", "message": "Name is required"}, status=400)

            book = Book.objects.create(
                name=data.get('name'),
                author=data.get('author', ''),
                published_date=data.get('published_date'),
                price=data.get('price'),
                currency=data.get('currency'),
                category=data.get('category'),
                page_count=data.get('page_count'),
                publisher=data.get('publisher', ''),
                description=data.get('description', '')
            )

            return JsonResponse({
                "status": "success",
                "message": "Book added successfully",
                "book_id": book.id
            }, status=201)

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Only POST allowed"}, status=405)