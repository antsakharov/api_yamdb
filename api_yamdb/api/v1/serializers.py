
from django.shortcuts import get_object_or_404
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer, SlugRelatedField,
                                        ValidationError, StringRelatedField)

from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


class SignupSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    @staticmethod
    def validate_username(value):
        if value == 'me':
            raise ValidationError('Имя зарезервировано системой,'
                                  ' выберите другое')
        return value


class TokenSerializer(ModelSerializer):
    confirmation_code = CharField(max_length=50, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = IntegerField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleCreateSerializer(ModelSerializer):
    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True, required=False)
    score = IntegerField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (Review.objects.filter(title=title, author=author).exists()
                and request.method == 'POST'):
            raise ValidationError('Может оставить только один отзыв!')
        return data


class CommentSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
