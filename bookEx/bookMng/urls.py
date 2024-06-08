from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('aboutUs', views.aboutUs, name='aboutUs'),
    path('book_detail/<int:book_id>', views.book_detail, name='book_detail'),
    path('book_delete/<int:book_id>', views.book_delete, name='book_delete'),
    path('postbook', views.postbook, name='postbook'),
    path('displaybooks', views.displaybooks, name='displaybooks'),
    path('searchbooks', views.searchbooks, name='searchbooks'),
    path('api/books/<str:book_name>', views.getbook, name='getbook'),
    path('mybooks', views.mybooks, name='mybooks'),
    path('comments', views.comments, name='comments'),
    path('postcommentpost', views.postcommentpost, name="postcommentpost"),
    path('book_detail/postcomment/<int:book_id>', views.postcomment, name="postcomment"),
    path('comment_detail/<int:comment_id>', views.comment_detail, name='comment_detail'),
    path('favorites', views.favorites, name='favorites'),
    path('rating/<int:book_id>', views.rating, name='rating'),
    path('postrating', views.postrating, name='postrating'),
    path('delete_rating/<int:rating_id>/', views.delete_rating, name='delete_rating'),
    path('book_detail/comment_delete/<int:book_id>/<int:comment_id>', views.comment_delete, name='comment_delete'),
]

