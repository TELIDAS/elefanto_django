from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('review/', views.ReviewListView.as_view(), name='review-list'),
    path('review/create/', views.ReviewCreateView.as_view(), name='review-create'),
    path('favorite/create/', views.UserFavoritesBookCreateView.as_view(), name='favorite-create'),
    path('review/<int:pk>/', views.ReviewDetailView.as_view(), name='review-detail'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', obtain_auth_token, name='api_token_auth'),
]
