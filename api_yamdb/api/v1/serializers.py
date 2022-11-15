from rest_framework import serializers
from reviews.models import CustomUser


class SignupSerializer(serializers.Serializer):
    """Сериалазер без модели, для полей username и email."""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$', max_length=150)
    email = serializers.EmailField()

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Имя зарезервировано системой, выберите другое')
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+$', max_length=150,)
    confirmation_code = serializers.CharField(max_length=50, required=True)


class UserSerializer(serializers.ModelSerializer):
    """Сериалазер для модели User."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
