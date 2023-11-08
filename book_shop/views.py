from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Book, Review
from .serializers import BookListSerializer, BookDetailSerializer, ReviewSerializer, UserFavoritesBookSerializer, \
    UserRegistrationSerializer, UserSerializer
from .repositories import BookRepository, ReviewRepository
from .services import BookService, ReviewService
from .filters import BookFilter
from rest_framework.authtoken.models import Token


class BookListView(generics.ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    service = BookService(BookRepository(Book))
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = BookFilter
    filterset_fields = ['genre', 'author']
    search_fields = ['title', 'description']
    ordering_fields = ['average_rating']

    def get_queryset(self):
        filters = {k: self.request.query_params[k] for k in self.request.query_params}

        user = self.request.user
        return self.service.list_books(filters=filters, user=user)


class BookDetailView(generics.RetrieveAPIView):
    serializer_class = BookDetailSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    service = BookService(BookRepository(Book))

    def get_object(self):
        book_id = self.kwargs.get('pk')
        return self.service.get_book_details(book_id=book_id)


class ReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    service = ReviewService(ReviewRepository(Review))

    def get_queryset(self):
        return self.service.list_reviews()


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    service = ReviewService(ReviewRepository(Review))


class ReviewDetailView(generics.RetrieveAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    service = ReviewService(ReviewRepository(Review))

    def get_object(self):
        review_id = self.kwargs.get('pk')
        return self.service.get_review_details(review_id=review_id)


class UserFavoritesBookCreateView(generics.CreateAPIView):
    serializer_class = UserFavoritesBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user).data,
            "token": token.key,
            "message": "User CrEated Successfully. Login with the token",
        }, status=status.HTTP_201_CREATED)
