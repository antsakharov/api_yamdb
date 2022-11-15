from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import CustomUser

from .permissions import IsAdminOrReadOnly
from .serializers import SignupSerializer, TokenSerializer, UserSerializer


class APISignup(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        user = CustomUser.objects.create(username=username, email=email)
        token = default_token_generator.make_token(user)
        send_mail(
            subject='Ваш код для получения api-токена.',
            message=f'Код: {token}',
            from_email='test@gmail.com',
            recipient_list=[user.email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateToken(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        username = serializer.validated_data['username']
        user = get_object_or_404(CustomUser, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
        return Response("Confirm code invalid", status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    pass


class GenreViewSet(viewsets.ModelViewSet):
    pass


class CategoryViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = ('username')

    @action(methods=['get', 'patch'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method == 'GET':
            user = self.request.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)

        if request.method == 'PATCH':
            user = get_object_or_404(CustomUser, id=request.user.id)
            fixed_data = self.request.data.copy()
            if ('role' in self.request.data and user.role == 'user'):
                fixed_data['role'] = 'user'
            serializer = UserSerializer(user, data=fixed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)
