from rest_framework import serializers
from .models import Genre, Author, Book, Review, UserFavoritesBook
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class BookListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    detail_url = serializers.HyperlinkedIdentityField(view_name='book-detail')

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author',
                  'description', 'publication_date', 'detail_url', 'is_favorite']
        depth = 1

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserFavoritesBook.objects.filter(user=user, book=obj).exists()
        return False


class BookDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    author = AuthorSerializer(read_only=True)
    is_favorite = serializers.SerializerMethodField()
    detail_url = serializers.HyperlinkedIdentityField(view_name='book-detail')
    avg_rating = serializers.FloatField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author',
                  'description', 'publication_date', 'detail_url', 'is_favorite',
                  'reviews', "avg_rating"]
        depth = 1

    def get_is_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return UserFavoritesBook.objects.filter(user=user, book=obj).exists()
        return False


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'book', 'author', 'rating', 'text']


class UserFavoritesBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFavoritesBook
        fields = ['id', 'user', 'book', 'added_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
