from rest_framework import serializers
from rest_framework.serializers import (CharField,
                                        ModelSerializer,
                                        ValidationError)

from reviews.models import CustomUser, Category, Genre, Title


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
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title
