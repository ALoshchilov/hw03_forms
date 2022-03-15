from django.views.generic.edit import CreateView
from .forms import BookForm


class BookView(CreateView):
    form_class = BookForm
