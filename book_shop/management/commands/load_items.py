from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from book_shop.models import Genre, Author, Book, Review, UserFavoritesBook
import random
from datetime import timedelta, date

"""python manage.py load_items"""


class Command(BaseCommand):

    def handle(self, *args, **options):
        Genre.objects.all().delete()
        Author.objects.all().delete()
        Book.objects.all().delete()
        Review.objects.all().delete()
        UserFavoritesBook.objects.all().delete()

        genres = [Genre(name=f"Genre{index}") for index in range(1, 6)]
        Genre.objects.bulk_create(genres)

        authors = [Author(name=f"Author{index}") for index in range(1, 6)]
        Author.objects.bulk_create(authors)

        books = []
        for genre in Genre.objects.all():
            for author in Author.objects.all():
                for i in range(5):
                    books.append(Book(
                        title=f"{genre.name} Book{i + 1} by {author.name}",
                        genre=genre,
                        author=author,
                        description=f"Description for {genre.name} Book{i + 1} by {author.name}",
                        publication_date=date.today() - timedelta(days=random.randint(1, 1000))
                    ))
        Book.objects.bulk_create(books)

        reviews = []
        user = User.objects.first()
        for book in Book.objects.all():
            reviews.append(Review(
                book=book,
                author=user,
                rating=random.randint(1, 5),
                text=f"Review text for {book.title}"
            ))
        Review.objects.bulk_create(reviews)

        user_favorites = []
        for book in Book.objects.all()[:10]:
            user_favorites.append(UserFavoritesBook(
                user=user,
                book=book
            ))
        UserFavoritesBook.objects.bulk_create(user_favorites)

        self.stdout.write(self.style.SUCCESS('Добавлены мок данные для теста'))
