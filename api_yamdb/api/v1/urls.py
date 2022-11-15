from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CommentViewSet,
                    ReviewViewSet,
                    GenreViewSet,
                    CategoryViewSet,
                    TitleViewSet,
                    CustomUserViewSet,)

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

urlpatterns = [
    path('', include(router.urls)),
    #path('', include('djoser.urls')),
    #path('', include('djoser.urls.jwt')),
]
