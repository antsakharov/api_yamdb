from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APISignup, CategoryViewSet, CommentViewSet, CreateToken,
                    CustomUserViewSet, GenreViewSet, ReviewViewSet,
                    TitleViewSet)

app_name = 'api'
router = DefaultRouter()

router.register(
    'users',
    CustomUserViewSet,
    basename='users'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

token_auth_urls = [
    path(
        'auth/signup/',
        APISignup.as_view(),
        name='signup'
    ),
    path(
        'auth/token/',
        CreateToken.as_view(),
        name='gain_token'
    ),
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(token_auth_urls)),
]
