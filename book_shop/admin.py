from django.contrib import admin
from .models import Genre, Author, Book, Review, UserFavoritesBook


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'genre', 'author', 'publication_date']
    list_filter = ['genre', 'author']
    search_fields = ['title', 'description']
    date_hierarchy = 'publication_date'
    raw_id_fields = ['genre', 'author']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'author', 'rating', 'text']
    list_filter = ['book', 'rating']
    search_fields = ['text', 'book__title']
    raw_id_fields = ['book', 'author']


@admin.register(UserFavoritesBook)
class UserFavoritesBookAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'added_at']
    list_filter = ['user', 'book']
    search_fields = ['book__title', 'user__username']
    raw_id_fields = ['user', 'book']
    date_hierarchy = 'added_at'
