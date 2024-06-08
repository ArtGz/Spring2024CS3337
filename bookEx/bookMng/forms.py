from django import forms
from django.forms import ModelForm
from .models import Book
from .models import Comment
from .models import Rating


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class SearchForm(ModelForm):
    name__contains = forms.CharField(label="Name", max_length=200, required=False)
    price__gte = forms.DecimalField(label="Min Price", decimal_places=2, max_digits=8, required=False)
    price__lte = forms.DecimalField(label="Max Price", decimal_places=2, max_digits=8, required=False)

    class Meta:
        model = Book
        fields = [
            'name__contains',
            'price__gte',
            'price__lte',
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'title',
            'comment',
        ]

class RatingForm(forms.ModelForm):
    book_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Rating
        fields = ['book_id', 'stars', 'review']

