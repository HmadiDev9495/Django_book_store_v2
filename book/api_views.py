import json
from django.views.generic import ListView, CreateView , UpdateView , DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Book
from .forms import CreateBook


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
            'publisher', 'description', 'created_at'
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

        form = self.form_class(data, instance=self.get_object())  # instance = کتاب فعلی

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