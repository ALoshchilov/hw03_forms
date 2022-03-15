from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        # Форма для работы с моделью Book
        model = Book
        fields = ('name', 'isbn', 'pages')
