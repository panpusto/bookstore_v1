from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from books.models import Book, Review


class BookTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='testuser1',
            password='testpass123',
            email='testuser1@email.com',
        )

        cls.special_permission = Permission.objects.get(
            codename="special_status"
        )

        cls.book = Book.objects.create(
            title="Hobbit",
            author="J.R.R. Tolkien",
            price="30.00"
        )

        cls.review = Review.objects.create(
            author=cls.user,
            book=cls.book,
            review="What an amazing book!"
        )

    def test_book_listing(self):
        self.assertEqual(f"{self.book.title}", "Hobbit")
        self.assertEqual(f"{self.book.author}", "J.R.R. Tolkien")
        self.assertEqual(f"{self.book.price}", "30.00")

    def test_book_list_view_for_logged_in_user(self):
        self.client.login(email="testuser1@email.com", password="testpass123")
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hobbit")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_list_view_for_logged_out_user(self):
        self.client.logout()
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, "%s?next=/books/" % (reverse("account_login"))
        )
        response = self.client.get(
            "%s?next=/books/" % (reverse("account_login"))
        )
        self.assertContains(response, "Log In")

    def test_book_detail_view_with_permissions(self):
        self.client.login(email="testuser1@email.com", password="testpass123")
        self.user.user_permissions.add(self.special_permission)
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Hobbit")
        self.assertContains(response, "What an amazing book!")
        self.assertTemplateUsed(response, "books/book_detail.html")
