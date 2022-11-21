from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (CharField, IntegerField,
                                        ModelSerializer, SlugRelatedField,
                                        ValidationError, StringRelatedField)

from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


class SignupSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise ValidationError('Имя зарезервировано системой,'
                                  ' выберите другое')
        return value


class TokenSerializer(ModelSerializer):
    confirmation_code = CharField(max_length=50, required=True)
    username = CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


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
        fields = '__all__'


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
        fields = '__all__'


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            author=self.context['request'].user,
            title__id=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise ValidationError(
                'Вы уже оставляли отзыв на это произведении'
            )
        return data


class CommentSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True, required=False)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
