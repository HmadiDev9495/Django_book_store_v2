import json
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Book, ImageBook
from .forms import CreateBook
from .serializers import (
    BookSerializer, BookCreateSerializer, BookUpdateSerializer,
    ImageBookSerializer, ImageBookUploadSerializer
)
from .permissions import IsOwnerOrReadOnly, IsPublisher


@method_decorator(csrf_exempt, name='dispatch')
class BookCreateView(CreateView):
    model = Book
    form_class = CreateBook

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"},
                status=400
            )

        form = self.form_class(data)

        if form.is_valid():
            book = form.save()
            return JsonResponse({
                "status": "success",
                "message": "Book added successfully",
                "book_id": book.id,
                "book_name": book.name
            }, status=201)
        else:
            return JsonResponse({
                "status": "error",
                "errors": form.errors
            }, status=400)

    def form_invalid(self, form):
        return JsonResponse({
            "status": "error",
            "errors": form.errors
        }, status=400)

    def get(self, request, *args, **kwargs):
        return JsonResponse(
            {"status": "error", "message": "GET not allowed on this endpoint"},
            status=405
        )


class BookListView(ListView):
    model = Book

    def render_to_response(self, context, **response_kwargs):
        books = list(self.get_queryset().values(
            'id', 'name', 'author', 'published_date',
            'price', 'currency', 'category', 'page_count',
            'publisher_name', 'description', 'created_at'
        ))
        return JsonResponse(books, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    form_class = CreateBook

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

        form = self.form_class(data, instance=self.get_object())

        if form.is_valid():
            book = form.save()
            return JsonResponse({
                "status": "success",
                "message": "Book updated successfully",
                "book_id": book.id,
                "book_name": book.name
            }, status=200)
        else:
            return JsonResponse({
                "status": "error",
                "errors": form.errors
            }, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class BookDeleteView(DeleteView):
    model = Book

    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        book.delete()
        return JsonResponse({
            "status": "success",
            "message": "Book deleted successfully",
            "book_id": kwargs['pk']
        }, status=200)

class PublishedBookListView(generics.ListAPIView):

    serializer_class = BookSerializer
    permission_classes = []

    def get_queryset(self):
        return Book.objects.filter(is_published=True).select_related('publisher').prefetch_related('images')

class MyBookListView(generics.ListCreateAPIView):

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(publisher=self.request.user).prefetch_related('images')

    def create(self, request, *args, **kwargs):
        serializer = BookCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book = serializer.save(publisher=request.user)

        return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)

class MyBookDetailView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly , IsPublisher]

    def get_queryset(self):

        return Book.objects.filter(publisher=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = BookUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(BookSerializer(instance).data)

class BookImageUploadView(generics.CreateAPIView):

    serializer_class = ImageBookUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        book = get_object_or_404(Book, id=self.kwargs['book_id'], publisher=self.request.user)
        serializer.save(book=book)


class BookImageListView(generics.ListAPIView):

    serializer_class = ImageBookSerializer
    permission_classes = []

    def get_queryset(self):
        book_id = self.kwargs['book_id']
        return ImageBook.objects.filter(book_id=book_id)


class BookImageDeleteView(generics.DestroyAPIView):
    serializer_class = ImageBookSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return ImageBook.objects.filter(book__publisher=self.request.user)

    def get_object(self):
        image = get_object_or_404(ImageBook, id=self.kwargs['pk'])
        if image.book.publisher != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("فقط ناشر می‌تونه این عکس رو حذف کنه")
        return image