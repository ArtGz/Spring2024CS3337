from django.test import TestCase
from bookMng.models import Book


class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(name='Django', web='https://www.google.com', price=5.99)
        Book.objects.create(name='Web', web='https://www.google.com', price=5.99, average_rating=4.3)

    def test_books_are_valid(self):
        djan = Book.objects.get(name="Django")
        web = Book.objects.get(name="Web")
        self.assertEqual(djan.web, 'https://www.google.com')
        self.assertEqual(web.price, 5.99)