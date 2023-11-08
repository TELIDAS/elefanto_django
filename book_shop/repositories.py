from django.db import models
from django.db.models import Avg

from book_shop.models import UserFavoritesBook


class BookRepository:
    def __init__(self, model):
        self.model = model

    def get_all_books(self):
        return self.model.objects.all()

    @staticmethod
    def prefetch_related_with_favorites(queryset, user):
        return queryset.prefetch_related(
            models.Prefetch(
                'userfavoritesbook_set',
                queryset=UserFavoritesBook.objects.filter(user=user),
                to_attr='user_favorites'
            )
        )

    def get_book_by_id(self, book_id):
        return self.model.objects.filter(id=book_id).annotate(
            avg_rating=Avg('reviews__rating')).prefetch_related(
            'reviews').first()


class ReviewRepository:
    def __init__(self, model):
        self.model = model

    def get_review_by_id(self, review_id):
        return self.model.objects.get(pk=review_id)

    def list_reviews_for_book(self, book_id):
        return self.model.objects.filter(book__id=book_id)


class GenreRepository:
    def __init__(self, model):
        self.model = model

    def get_genre_by_id(self, genre_id):
        return self.model.objects.get(pk=genre_id)

    def list_all_genres(self):
        return self.model.objects.all()
