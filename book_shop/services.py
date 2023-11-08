from django.db.models import Q


class BookService:
    def __init__(self, repository):
        self.repository = repository

    def list_books(self, filters=None, user=None):
        queryset = self.repository.get_all_books()

        if filters:
            start_date = filters.pop('start_date', None)
            end_date = filters.pop('end_date', None)

            if start_date and end_date:
                date_filter = Q(publication_date__gte=start_date) & Q(publication_date__lte=end_date)
                queryset = queryset.filter(date_filter)

            if filters:
                queryset = queryset.filter(**filters)

        if user and user.is_authenticated:
            queryset = self.repository.prefetch_related_with_favorites(queryset, user)

        return queryset

    def get_book_details(self, book_id):
        return self.repository.get_book_by_id(book_id)

    def add_book_to_favorites(self, book, user):
        user.favorites.add(book)
        return book


class ReviewService:
    def __init__(self, repository):
        self.repository = repository

    def get_review_details(self, review_id):
        return self.repository.get_review_by_id(review_id)

    def list_reviews(self, book_id=None):
        if book_id:
            return self.repository.list_reviews_for_book(book_id)
        else:
            return self.repository.model.objects.all()


class GenreService:
    def __init__(self, repository):
        self.repository = repository

    def get_genre_details(self, genre_id):
        return self.repository.get_genre_by_id(genre_id)

    def list_genres(self):
        return self.repository.list_all_genres()
