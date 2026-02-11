from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Book
from .forms import CreateBook
from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from book.user.permissions import IsAuthorOrReadOnly


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

def get_all_books(request):
    books = list(Book.objects.values())
    return JsonResponse(books, safe=False)

class BookAPI(APIView):
    def post(self, request):
        body = json.loads(request.body.decode('utf-8'))
        serializer = BookSerializer(data=body)
        if serializer.is_valid():
            book = serializer.save()
            return JsonResponse({'book_id': book.id})
        return JsonResponse({'error': 'Data format is not correct'}, status=400)

    def get(self, request):
        books = list(Book.objects.values())
        return JsonResponse(books, safe=False)

class BookGenericAPI(generics.ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

class GetBookAPI(generics.RetrieveDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    lookup_field = "price"
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

def index(request):
    return render(request, 'book/index.html')