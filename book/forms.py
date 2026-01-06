from django import forms
from .models import Book

class CreateBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = False
        self.fields['currency'].required = False
        self.fields['category'].required = False