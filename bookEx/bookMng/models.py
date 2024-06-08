from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class MainMenu(models.Model):
    item = models.CharField(max_length=200, unique=True)
    link = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.item


class Book(models.Model):
    name = models.CharField(max_length=200)
    web = models.URLField(max_length=300)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    publishdate = models.DateField(auto_now=True)
    picture = models.FileField(upload_to='bookEx/static/uploads')
    pic_path = models.CharField(max_length=300, editable=False, blank=True)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    title = models.CharField(max_length=200)
    comment = models.CharField(max_length=2000)
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    book = models.CharField(max_length=200)
    commentdate = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    stars = models.IntegerField()
    review = models.TextField()
    username = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"Rating for {self.book.name}: {self.stars} stars"