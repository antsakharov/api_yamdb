from rest_framework.serializers import (CharField,
                                        ModelSerializer,
                                        ValidationError)
from reviews.models import CustomUser


class SignupSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    def validate_username(self, value):
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
