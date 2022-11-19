from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import (filters, mixins, permissions, status, views,
                            viewsets)
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, CustomUser, Genre, Review, Title
from .filters import TitleFilter
from .permissions import (IsAdminOrReadOnly, ListOrAdminModeratorOnly,
                          ReadOnlyOrIsAdminOrModeratorOrAuthor)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, SignupSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          TokenSerializer, UserSerializer)


class APISignup(views.APIView):
    permission_classes = [permissions.AllowAny]

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
            fail_silently=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateToken(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        username = serializer.validated_data['username']
        user = get_object_or_404(CustomUser, username=username)
        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
        return Response("Confirm code invalid",
                        status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReadOnlyOrIsAdminOrModeratorOrAuthor]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Review.objects.filter(title_id=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        serializer.save(author=self.request.user, title_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ReadOnlyOrIsAdminOrModeratorOrAuthor]

    def get_review(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, id=review_id, title=title_id)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ListOrAdminModeratorOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ListOrAdminModeratorOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('category')
    serializer_class = TitleSerializer
    permission_classes = [ListOrAdminModeratorOnly]
    pagination_class = LimitOffsetPagination
    filter_class = filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = ('username')

    @action(permission_classes=[permissions.IsAuthenticated],
            methods=['get', 'patch'],
            detail=False)
    def me(self, request):
        if request.method == 'GET':
            user = self.request.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)
        if request.method == 'PATCH':
            user = get_object_or_404(CustomUser, id=request.user.id)
            changed_data = self.request.data.copy()
            if ('role' in self.request.data and user.role == 'user'):
                changed_data['role'] = 'user'
            serializer = UserSerializer(user, data=changed_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=request.data, status=status.HTTP_400_BAD_REQUEST)
