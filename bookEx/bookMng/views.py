from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from json import dumps
# Create your views here.
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
# Models
from .models import MainMenu
from .models import Book
from .models import Comment
from .models import Rating

# Forms
from .forms import BookForm, SearchForm
from .forms import CommentForm

from django.shortcuts import redirect

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from django.db.models import Avg

import json
from django.http import JsonResponse
from django.template.loader import render_to_string

from .forms import RatingForm


def index(request):
    if not request.user.is_anonymous:
        return HttpResponseRedirect('/home')
    return render(request,
                  'bookMng/index.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


def home(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    return render(request,
                  'bookMng/home.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )


def postbook(request):
    submitted = False
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            try:
                book.username = request.user
            except Exception:
                pass
            book.save()
            return HttpResponseRedirect('/postbook?submitted=True')
    else:
        form = BookForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/postbook.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                  }
                  )


def displaybooks(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    books = Book.objects.all()
    for b in books:
        b.pic_path = b.picture.url[14:]
    return render(request,
                  'bookMng/displaybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )


class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)


def book_detail(request, book_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    book = Book.objects.get(id=book_id)
    book.pic_path = book.picture.url[14:]
    comments = Comment.objects.filter(book=book.name)
    average_rating = book.rating_set.aggregate(Avg('stars'))['stars__avg']
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book,
                      'comments': comments,
                      'average_rating': average_rating
                  }
                  )


def mybooks(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    books = Book.objects.filter(username=request.user)
    for book in books:
        book.pic_path = book.picture.url[14:]
        book.average_rating = book.rating_set.aggregate(Avg('stars'))['stars__avg']
    return render(request,
                  'bookMng/mybooks.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books
                  }
                  )

def book_delete(request, book_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    book = Book.objects.get(id=book_id)
    if book.username != request.user or book is None:
        return HttpResponseRedirect('/mybooks')
    book.delete()
    return render(request,
                  'bookMng/book_delete.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'book': book
                  }
                  )

def comment_delete(request, comment_id, book_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect(f'/book_detail/{book_id}')

def getbook(request, book_name):
    books = Book.objects.filter(name__contains=book_name)
    return HttpResponse(
        dumps(list(books.values_list('picture', 'name', 'id'))),
        content_type='application/json'
    )


def searchbooks(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    submitted = False
    books = []
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            url = '/searchbooks?'
            for field in SearchForm.base_fields:
                value = request.POST.get(field, '')
                url += f'{(value != "" and field + "=" + value + "&") or ""}'
            return HttpResponseRedirect(url)

    else:
        form = SearchForm()
        if any(field in SearchForm.base_fields for field in request.GET):
            submitted = True
            kwargs = {}
            for field in request.GET:
                kwargs[field] = request.GET[field]
            books = Book.objects.filter(**kwargs)

        for b in books:
            b.pic_path = b.picture.url[14:]

    return render(request,
                  'bookMng/searchbooks.html',
                  {
                      'form': form,
                      'books': books,
                      'searchEmpty': len(books) == 0,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                  })


def comments(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    commentlist = Comment.objects.all()

    return render(request,
                  'bookMng/comments.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'commentlist': commentlist,
                  })


def postcomment(request, book_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    book = Book.objects.get(id=book_id)
    submitted = False
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            comment = form.save(commit=False)
            try:
                comment.username = request.user
                comment.book = book.name
            except Exception:
                pass
            comment.save()
            return HttpResponseRedirect(f'/book_detail/{book_id}')
    else:
        form = CommentForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'bookMng/postcomment.html',
                  {
                      'form': form,
                      'item_list': MainMenu.objects.all(),
                      'submitted': submitted,
                      'book': book
                  })


def postcommentpost(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    submitted = False
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            comment = form.save(commit=False)
            try:
                comment.username = request.user
            except Exception:
                pass
            comment.save()
            return HttpResponseRedirect('/postcommentpost?submitted=True')
    else:
        form = CommentForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request,
                  'bookMng/book_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'comments': comments
                  }
                  )


def comment_detail(request, comment_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    comment = Comment.objects.get(id=comment_id)

    return render(request,
                  'bookMng/comment_detail.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'comment': comment,
                  })

def aboutUs(request):
    return render(request,
                  'bookMng/aboutUs.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

def favorites(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    return render(request,
                  'bookMng/favorites.html',
                  {
                      'item_list': MainMenu.objects.all()
                  }
                  )

def rating(request, book_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    book = Book.objects.get(id=book_id)
    ratings = book.rating_set.all()
    average_rating = ratings.aggregate(Avg('stars'))['stars__avg']

    if request.method == 'POST':
        rating_value = request.POST.get('stars')
        review_text = request.POST.get('review')
        Rating.objects.create(book=book, stars=rating_value, review=review_text)
        ratings = book.rating_set.all()
        average_rating = ratings.aggregate(Avg('stars'))['stars__avg']

    return render(request, 'bookMng/rating.html', {'book': book, 'ratings': ratings, 'average_rating': average_rating})


def delete_rating(request, rating_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    if request.method == 'POST':
        rating = Rating.objects.get(id=rating_id)
        if rating.username == request.user:
            rating.delete()

        return redirect('postrating')



def postrating(request):
    if request.user.is_anonymous:
        return HttpResponseRedirect(reverse_lazy('index'))
    books = Book.objects.all()
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            stars = form.cleaned_data['stars']
            review = form.cleaned_data['review']
            book = Book.objects.get(id=book_id)
            Rating.objects.create(book=book, stars=stars, review=review, username=request.user)
            return redirect('postrating')

    for book in books:
        book.pic_path = book.picture.url[14:]
        book.average_rating = Book.objects.filter(name=book.name).aggregate(Avg('rating__stars'))['rating__stars__avg']
        book.ratings = book.rating_set.all()

    form = RatingForm()
    return render(request,
                  'bookMng/postrating.html',
                  {
                      'item_list': MainMenu.objects.all(),
                      'books': books,
                      'form': form
                  }
                )